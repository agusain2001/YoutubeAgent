import os
import sys
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API key from environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

if not YOUTUBE_API_KEY:
    print(json.dumps({"error": "YOUTUBE_API_KEY is not set in the .env file"}))
    sys.exit(1)

def youtube_api_scrape(keyword, max_results=10):
    """
    Fetches YouTube video data based on a keyword.
    Args:
        keyword (str): Search term for fetching videos.
        max_results (int): Maximum number of videos to fetch.
    Returns:
        list: A list of dictionaries containing video data.
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    all_videos = []

    try:
        search_request = youtube.search().list(
            part="id,snippet",
            q=keyword,
            type="video",
            maxResults=max_results,
        )
        search_response = search_request.execute()

        for item in search_response.get("items", []):
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]

                # Fetch video details
                video_details_request = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=video_id,
                )
                video_details_response = video_details_request.execute()

                if video_details_response.get("items"):
                    video = video_details_response["items"][0]
                    video_data = {
                        "Video URL": f"https://www.youtube.com/watch?v={video_id}",
                        "Title": video["snippet"]["title"],
                        "Description": video["snippet"]["description"],
                        "Channel Title": video["snippet"]["channelTitle"],
                        "Keyword Tags": video["snippet"].get("tags", []),
                        "Category ID": video["snippet"].get("categoryId"),
                        "Published At": video["snippet"]["publishedAt"],
                        "Duration": video["contentDetails"]["duration"],
                        "View Count": video["statistics"].get("viewCount", 0),
                        "Like Count": video["statistics"].get("likeCount", 0),
                        "Comment Count": video["statistics"].get("commentCount", 0),
                    }
                    all_videos.append(video_data)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    return all_videos

if __name__ == "__main__":
    # Check for the keyword argument
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Keyword argument is required"}))
        sys.exit(1)

    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10

    try:
        videos = youtube_api_scrape(keyword, max_results)
        # Print the output as JSON
        print(json.dumps(videos, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
