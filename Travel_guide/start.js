const express = require('express');
const { spawn } = require('child_process');
const app = express();
const bodyParser = require('body-parser');

app.use(express.static('public'));
app.use(bodyParser.json());

let clients = [];

// SSE endpoint for receiving messages
app.get('/api/chat', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');

    clients.push(res);

    req.on('close', () => {
        clients = clients.filter(client => client !== res);
    });
});

// Initialize Python process
const pythonProcess = spawn('python', ['trail.py']);

// Handle Python process output
pythonProcess.stdout.on('data', (data) => {
    const response = data.toString();
    clients.forEach(client => {
        client.write(`data: ${JSON.stringify({ response })}\n\n`);
    });
});

// Handle messages from frontend
app.post('/api/chat', (req, res) => {
    const message = req.body.message;
    pythonProcess.stdin.write(message + '\n');
    res.json({ status: 'success' });
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`Python Error: ${data}`);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
