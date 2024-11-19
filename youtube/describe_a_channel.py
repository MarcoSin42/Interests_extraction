import ollama
from get_title_and_caption import get_captions

import google.generativeai as genai
import yt_dlp
from enum import Enum

gemini_key = open("/home/Marco/Projects/Interests_extraction/api_keys/gemini_api_key.txt").readline()
client_secrets_file = "/home/Marco/Projects/Interests_extraction/api_keys/client_secret_1030788119864-j1depr7vbhq1d0500ld1dqe13idcctku.apps.googleusercontent.com.json"


""" Uses an LLM model to describe a YouTube channel given a channel id
    channel_id (str) : The channel of interest
    limit (int): How many Videos to look at
"""
def llm_describe_channel(channel_id: str, limit: int  = 15):
    return None


def llm_describe_video(video_id: str):
    prompt:str  =  """
    You are given the title, description, and captions of a YouTube video.  Categorize this video using as few words as possible (ideally 1-3), for example, if a video is describing the tastes and rating a video game, categorize the video as being "gaming".  If possible, try to sub-categorize it, continuing with the earlier example, if the video is predominatly about the game "Factorio", then you should sub-categorize it as Factorio.
    YouTube's automated captioning system is somewhat imperfect and therefore you should be tolerant of any transcription errors it may make (mostly with regards to spelling and not semantic content) .  In addition, provide a list of top 5 possibly related categories.  You should always prioritize the captions and descriptions over the title and simply use the title to help affirm your determination.  Ignore any sponsored content contained within the caption and description unless the video is explicitly entirely about a sponsor's product.  
    Many YouTube videos have a clickbait title, so you should weight it somewhat less in making your determination, however, the title is likely still relevant though it may be relevant in an unexpected way.
    
    Your response MUST be in the following form:

    Category: [How'd you categorize this video.  Use 5 words at most and make your best effort to make it 1 word.]
    Sub-category: [What sub-category you believe it falls under, this should be more specific than the category you've provided.  Reply N/A if you are unsure.]
    Related categories: [Top 5 related categories]
    Reason: [Why you categorized it this way]
    \n
    """
    title = ""
    captions = get_captions(video_id)
    description = ""

    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info("https://youtu.be/" + video_id, download=False)
        description = info_dict.get("description", None)
        title = info_dict.get("title", None)
    
    prompt += "The title is: " + title + "\n"
    prompt + "The description is: " + description + "\n" 
    prompt += "The captions are: " + captions

    model = genai.GenerativeModel("gemini-1.5-flash")
    genai.configure(api_key=gemini_key)
    response = model.generate_content(prompt)

    return  response



if __name__ == "__main__":
    response = llm_describe_video("rcQ0YQXGhpI")

    print(response)