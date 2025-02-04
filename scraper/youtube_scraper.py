import os
import sys
import json
import chromadb
from googleapiclient.discovery import build
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# API key from environment variables
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    sys.exit("Error: YOUTUBE_API_KEY is not set in the .env file")

# Initialize embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./chromadb_store")
collection = chroma_client.get_or_create_collection(name="youtube_videos")

def youtube_api_scrape(keyword, max_results=10):
    """
    Fetches YouTube video data based on a keyword and stores it in ChromaDB.
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    
    try:
        search_request = youtube.search().list(
            part="id,snippet", q=keyword, type="video", maxResults=max_results
        )
        search_response = search_request.execute()

        for item in search_response.get("items", []):
            if item["id"]["kind"] == "youtube#video":
                video_id = item["id"]["videoId"]
                
                # Fetch video details
                video_details_request = youtube.videos().list(
                    part="snippet,contentDetails,statistics", id=video_id
                )
                video_details_response = video_details_request.execute()
                
                if video_details_response.get("items"):
                    video = video_details_response["items"][0]
                    video_data = {
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "title": video["snippet"]["title"],
                        "description": video["snippet"]["description"],
                        "channel": video["snippet"]["channelTitle"],
                        "tags": video["snippet"].get("tags", []),
                        "category": video["snippet"].get("categoryId"),
                        "published": video["snippet"]["publishedAt"],
                        "duration": video["contentDetails"]["duration"],
                        "views": video["statistics"].get("viewCount", 0),
                        "likes": video["statistics"].get("likeCount", 0),
                        "comments": video["statistics"].get("commentCount", 0),
                    }
                    
                    # Convert textual data to embeddings
                    text_data = f"{video_data['title']} {video_data['description']}"
                    embedding = embedding_model.encode(text_data).tolist()
                    
                    # Store data in ChromaDB
                    collection.add(
                        ids=[video_id],
                        embeddings=[embedding],
                        metadatas=[video_data]
                    )
    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Error: Keyword argument is required")
    
    keyword = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    youtube_api_scrape(keyword, max_results)
