import os

import yt_dlp
import re

import google_auth_oauthlib.flow
import googleapiclient.discovery

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
LIMIT = 25000 # Word Limit; Multiply by .75 to translate this into tokens (roughly)
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "/home/Marco/Projects/Interests_extraction/api_keys/client_secret_1030788119864-j1depr7vbhq1d0500ld1dqe13idcctku.apps.googleusercontent.com.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
	client_secrets_file, scopes)
credentials = flow.run_local_server()

youtube = googleapiclient.discovery.build(
	api_service_name, api_version, credentials=credentials)

"""
  Downloads subs for a given youtube video, given its video id
  video_id (str): the video id of the YouTube video of interest
  
  return (int): the error code given by yt_dlp 
"""
def download_subs(video_id: str) -> int:
  url = "https://www.youtube.com/watch?v=" + video_id

  ydl_opts = {
    'writeautomaticsub': True,
    'subtitlesformat': 'vtt',
    'skip_download': True,
    'outtmpl': '/tmp/' + video_id
  }

  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ret_code = ydl.download([url]) 

    if ret_code != 0:
      return ret_code
  
  return 0

""" 
  Retrieves the subs of a given video and returns it as a string
"""
def get_captions(video_id: str) -> str:
  if download_subs(video_id) != 0:
    raise Exception("Unable to download the subs for a video")
  subs = extract_text_from_vtt("/tmp/" + video_id + ".en.vtt" )

  return subs

"""
  Extracts the text content from a VTT (Web Video Text Tracks) file.

  Parameters:
      file_path (str): The path to the VTT file.
      
  Returns:
      str: A string containing the extracted text content.
"""
def extract_text_from_vtt(file_path) -> str:
    extracted_text = []

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            # Skip empty lines, metadata lines, and timestamp lines
            if not line or line.startswith("WEBVTT") or "-->" in line:
                continue
            # Add non-empty text lines to the output
            extracted_text.append(extract_text_no_timestamps(line))
    
    return "\n".join(extracted_text)[:LIMIT]

"""
  Extracts semantic content from a string by removing timestamp and formatting tags.

  Parameters:
      input_text (str): The input string containing timestamps and tags.
      
  Returns:
      str: Cleaned text without timestamps and tags.
"""
def extract_text_no_timestamps(input_text):
    # Regex pattern to match timestamps and <c> tags
    pattern = r"<\d{2}:\d{2}:\d{2}\.\d{3}>|<\/?c>"
    # Replace matches with an empty string
    cleaned_text = re.sub(pattern, "", input_text)
    # Strip extra whitespace
    return cleaned_text.strip()

def get_user_subscriptions(credentials) -> list:
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

  subscriptions = []

  pageToken = ""
  while True:
    request = youtube.subscriptions().list(
        part="snippet,contentDetails",
        maxResults=50,
        pageToken=pageToken,
        mine=True
    )
    response = request.execute()
    items = response["items"]

    for item in items:
      subscriptions.append({
        "title": item["snippet"]["title"],
        "description": item["snippet"]["description"],
        "channelId": item["snippet"]["channelId"]
      })
    
    if "nextPageToken" in response:
      pageToken = response["nextPageToken"]
    else:
      break
  
  return subscriptions

def get_n_videos(channel_id: str, credentials, limit: int  = 5) -> list:
  videos = []

  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

  request = youtube. playlistItems().list(
    part="snippet",
    playlistId="UU"+channel_id[2:]
  )
  response = request.execute()

  items = response["items"]
  for item in items:
    videos.append({
      "videoId": item["snippet"]["resourceId"]["videoId"],
      "title": item["snippet"]["title"]
    })

  return videos
if __name__ == "__main__":
  subscriptions = []  
  subscriptions = get_user_subscriptions(credentials=credentials)
  videos = get_n_videos("UCINw3QY4ru79oarGS1jjzpA", credentials=credentials)
  for vid in videos:
    print(f"VideoID : {vid["videoId"]:15}  | Title: {vid["title"]}")
  for sub in subscriptions:
    print(f"Channel Name: {sub["title"]:25} | Channel ID: {sub["channelId"]:15} | Description: {sub["description"]}")
