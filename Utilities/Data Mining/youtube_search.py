#!/usr/bin/python

from apiclient.discovery import build
from oauth2client.tools import argparser
import pandas as pd
import json
import requests
import os

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "YOUR API KEY HERE"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        part="id,snippet",
        maxResults=options.max_results
    ).execute()

    videos = []
    titles = []
    urls = []
    viewCounts = []

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append(search_result["id"]["videoId"])
            titles.append(search_result["snippet"]["title"])
            urls.append("youtube.com/watch?v=" + search_result["id"]["videoId"])

    videolinks = "%2C+".join(videos)

    url = "https://www.googleapis.com/youtube/v3/videos?part=statistics&id=" + videolinks + "&key=" + DEVELOPER_KEY
    response = requests.get(url)

    json_data = json.loads(response.text)
    for data in json_data["items"]:
        viewCounts.append(int(data["statistics"]["viewCount"]))

    df = pd.DataFrame(
        {'Title': titles,
         'URL': urls,
         'View Count': viewCounts
         })

    df = df.set_index("Title")
    df = df.sort_values(by="View Count", ascending=False)
    file_path = os.path.dirname(os.path.realpath(__file__))
    df.to_csv(file_path + "\\bullying_urls.csv", sep=',')
    print("Done")

if __name__ == "__main__":
    search = input("Search terms:")
    result_size = input("How many videos to obtain?")
    argparser.add_argument("--q", help="Search term", default=search)
    argparser.add_argument("--max-results", help="Max results", default=result_size)
    args = argparser.parse_args()

    youtube_search(args)
