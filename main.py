from youtube_transcript_api import YouTubeTranscriptApi

link = (input("Enter the youtube link: "))
video_id = ""
if 'v=' in link:
    start = link.find('v=') + 2
    video_id = link[start: start+11]

print(video_id)
transcript = ""
try:
    fetched_transcript = YouTubeTranscriptApi().fetch(video_id)
    for snip in fetched_transcript:
        transcript += snip.text + " "
except Exception as v:
    print("video_id is not accepted\n", v)

print(len(transcript))
print(transcript)