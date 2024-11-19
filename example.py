# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os
import youtube_dl

import google_auth_oauthlib.flow
import googleapiclient.discovery


scopes = ["https://www.googleapis.com/auth/youtube.readonly"] 

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "/home/Marco/Projects/Interests_extraction/api_keys/client_secret_1030788119864-j1depr7vbhq1d0500ld1dqe13idcctku.apps.googleusercontent.com.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
    )

    request = youtube.video().

    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()
    exit()