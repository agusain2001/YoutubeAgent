const express = require("express");
const routes = require("./routes");
const YoutubeAgent = require("./youtubeAgent"); // Import YoutubeAgent
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());

// Routes
app.use("/api", routes);

// YouTube Agent Route
app.post("/youtube", async (req, res) => {
  const { keyword, maxResults } = req.body;

  try {
    const youtubeAgent = new YoutubeAgent(); // Create an instance of YoutubeAgent
    const result = await youtubeAgent.fetchAndProcess(keyword, maxResults || 10); // Call fetchAndProcess with the keyword and maxResults
    res.json({ success: true, data: result }); // Send the AI-processed data back to the client
  } catch (error) {
    console.error("Error processing request:", error.message);
    res.status(500).json({ success: false, error: error.message }); // Handle errors
  }
});

// Start Server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
