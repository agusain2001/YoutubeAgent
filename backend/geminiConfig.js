require('dotenv').config();

const geminiConfig = {
  name: 'gemini',
  apiKey: process.env.GEMINI_API_KEY,
  projectId: process.env.GOOGLE_PROJECT_ID,
  region: process.env.GOOGLE_REGION
};
if (!GEMINI_API_KEY) {
    throw new Error('GEMINI_API_KEY is not set in the environment variables.');
  }
  
module.exports = geminiConfig;
