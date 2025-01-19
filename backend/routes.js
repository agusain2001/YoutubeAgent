const express = require('express');
const { spawn } = require('child_process');
const router = express.Router();

router.post('/scrape', (req, res) => {
    const { keyword, maxResults } = req.body;

    if (!keyword) {
        return res.status(400).json({ error: 'Keyword is required' });
    }

    const pythonProcess = spawn('python', ['./scraper/youtube_scraper.py', keyword, maxResults || 10]);

    let output = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            console.error(`Python script exited with code ${code}:`, errorOutput);
            return res.status(500).json({ error: 'Failed to execute scraper.' });
        }

        try {
            const result = JSON.parse(output); // Parse JSON output from Python
            res.json(result);
        } catch (err) {
            console.error('Error parsing Python output:', err.message);
            res.status(500).json({ error: 'Invalid data from scraper.' });
        }
    });
});

module.exports = router;
