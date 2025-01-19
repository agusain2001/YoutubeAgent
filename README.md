# YouTube Data Scraper and AI Integration

This project integrates a YouTube data scraper with an AI-powered processing agent. The system fetches video data from YouTube using the YouTube Data API and processes it using an AI agent to extract meaningful insights. The backend is built using Node.js, and Python handles the scraping logic.

## Features

- Fetch YouTube video data based on keywords.
- Extract details like video URL, title, description, channel, keywords, views, likes, and comments.
- Process scraped data using an AI agent for further insights.
- Expose an easy-to-use API for clients.

---

## Project Structure

```
project/
├── app.js                 # Main backend application file
├── routes.js              # Additional API routes
├── youtubeAgent.js        # AI-integrated YouTube agent
├── scraper/               # Python scraper module
│   ├── youtube_scraper.py # Python scraper logic
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Environment variables for scraper
├── node_modules/          # Node.js dependencies
├── package.json           # Node.js dependencies and scripts
├── .env                   # Environment variables for the backend
└── README.md              # Documentation
```

---

## Prerequisites

### **Backend**
- Node.js (v18 or above)
- npm (Node Package Manager)

### **Scraper**
- Python (v3.8 or above)
- pip (Python Package Manager)

---

## Installation

### Clone the Repository
```bash
git clone <repository-url>
cd project
```

### Backend Setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Create a `.env` file in the root directory and add the following:
   ```env
   PORT=3000
   GEMINI_API_KEY=your_google_gemini_api_key
   ```

### Scraper Setup

1. Navigate to the `scraper` directory:
   ```bash
   cd scraper
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file inside the `scraper` folder and add:
   ```env
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

---

## How to Run the Project

### Step 1: Start the Backend
```bash
node app.js
```
This will start the backend server at `http://localhost:3000`.

### Step 2: Make API Calls
- Use Postman, curl, or any HTTP client to send POST requests to the backend.

Example Request:
```http
POST /youtube
Content-Type: application/json

{
  "keyword": "machine learning",
  "maxResults": 5
}
```

Example Response:
```json
{
  "success": true,
  "data": [
    {
      "Video URL": "https://www.youtube.com/watch?v=12345",
      "Title": "Introduction to Machine Learning",
      "Description": "Learn about ML basics...",
      "Channel Title": "Tech Channel",
      "Keyword Tags": ["machine learning", "AI"],
      "Category ID": "27",
      "Published At": "2024-11-25T12:00:00Z",
      "Duration": "PT10M5S",
      "View Count": "50000",
      "Like Count": "1000",
      "Comment Count": "150"
    }
  ]
}
```

---

## How It Works

### 1. **youtubeAgent.js**
This file integrates with Google Gemini AI to process the scraped YouTube data.

**Main Functionality**:
- `fetchAndProcess(keyword, maxResults)`:
  - Calls the Python scraper to fetch raw video data based on the given keyword.
  - Sends the scraped data to Google Gemini AI for processing.
  - Returns processed data to the backend.

**Key Sections**:
```javascript
const axios = require("axios");

class YoutubeAgent {
  constructor() {
    this.apiKey = process.env.GEMINI_API_KEY;
    this.endpoint = "https://gemini-api-endpoint.example.com"; // Replace with the actual endpoint
  }

  async fetchAndProcess(keyword, maxResults) {
    // Call the Python scraper
    const scrapedData = await callPythonScraper(keyword, maxResults);

    // Process data using Gemini AI
    const response = await axios.post(`${this.endpoint}/process`, {
      data: scrapedData,
      apiKey: this.apiKey
    });

    return response.data;
  }
}

module.exports = YoutubeAgent;
```

---

### 2. **youtube_scraper.py**
This Python script interacts with the YouTube Data API to scrape video data.

**Key Sections**:
```python
def youtube_api_scrape(keyword, max_results=10):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    all_videos = []

    # API Call to search videos
    search_request = youtube.search().list(
        part="id,snippet",
        q=keyword,
        type="video",
        maxResults=max_results,
    )
    search_response = search_request.execute()

    for item in search_response.get("items", []):
        video_id = item["id"]["videoId"]
        video_details_request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id,
        )
        video_details_response = video_details_request.execute()

        # Append video details to the result list
        video_data = { ... }
        all_videos.append(video_data)

    return all_videos
```

---

## API Endpoints

### POST `/youtube`
**Request**:
```json
{
  "keyword": "machine learning",
  "maxResults": 5
}
```

**Response**:
```json
{
  "success": true,
  "data": [...]
}
```

---

## Error Handling

- If the YouTube Data API key is invalid or missing, you will see:
  ```json
  {
    "error": "YOUTUBE_API_KEY is not set in the .env file."
  }
  ```
- If the Gemini AI endpoint is unavailable, you will see:
  ```json
  {
    "error": "Error processing data with Gemini."
  }
  ```

---

## Future Enhancements

- Add caching for frequently searched keywords.
- Integrate additional AI models for more complex video analysis.
- Develop a frontend interface for end-users.

---

## Author
Developed by [Your Name]. Feel free to contribute or report issues via GitHub!

