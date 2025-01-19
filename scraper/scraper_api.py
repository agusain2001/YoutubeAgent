from flask import Flask, request, jsonify
from youtube_scraper import youtube_api_scrape  # Import your scraper function

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        keyword = data.get('keyword')
        max_results = data.get('max_results', 10)

        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400

        videos = youtube_api_scrape(keyword, max_results)
        return jsonify(videos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)  # Run the API on port 5000
