const axios = require("axios");
const { spawn } = require("child_process");

class YoutubeAgent {
  constructor() {
    this.geminiApiKey = process.env.GEMINI_API_KEY; // API Key for Google Gemini
    this.geminiEndpoint = "https://gemini-api-endpoint.example.com/summarize"; // Replace with the actual endpoint
  }

  /**
   * Fetch data from the YouTube scraper.
   * @param {string} keyword - The keyword for YouTube search.
   * @param {number} maxResults - Maximum number of videos to fetch.
   * @returns {Promise<Array>} - Raw YouTube data from the scraper.
   */
  async fetchYoutubeData(keyword, maxResults) {
    return new Promise((resolve, reject) => {
      const scraperProcess = spawn("python", ["./scraper/youtube_scraper.py", keyword, maxResults]);

      let output = "";
      let error = "";

      scraperProcess.stdout.on("data", (data) => {
        output += data.toString();
      });

      scraperProcess.stderr.on("data", (data) => {
        error += data.toString();
      });

      scraperProcess.on("close", (code) => {
        if (code === 0) {
          try {
            const parsedData = JSON.parse(output);
            resolve(parsedData);
          } catch (err) {
            reject(`Error parsing scraper output: ${err}`);
          }
        } else {
          reject(`Scraper error: ${error}`);
        }
      });
    });
  }

  /**
   * Process data using Google Gemini AI.
   * @param {Array} youtubeData - The raw YouTube data to process.
   * @returns {Promise<Array>} - AI-processed data.
   */
  async processWithAI(youtubeData) {
    try {
      const response = await axios.post(this.geminiEndpoint, {
        data: youtubeData,
        apiKey: this.geminiApiKey,
      });

      return response.data;
    } catch (error) {
      console.error("Error processing data with Google Gemini:", error.message);
      throw error;
    }
  }

  /**
   * Fetch and process YouTube data using both scraper and AI.
   * @param {string} keyword - The keyword for YouTube search.
   * @param {number} maxResults - Maximum number of videos to fetch.
   * @returns {Promise<Array>} - Final processed data.
   */
  async fetchAndProcess(keyword, maxResults = 10) {
    try {
      // Step 1: Fetch raw data from the scraper
      const youtubeData = await this.fetchYoutubeData(keyword, maxResults);

      // Step 2: Process the data using AI
      const aiProcessedData = await this.processWithAI(youtubeData);

      return aiProcessedData;
    } catch (error) {
      console.error("Error in YouTube Agent:", error.message);
      throw error;
    }
  }
}

module.exports = YoutubeAgent;
