// src/pages/api/run-python.js
import { exec } from 'child_process';

export default function handler(req, res) {
    exec('python3 nasa_v2.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`exec error: ${error}`);
            return res.status(500).json({ error: stderr });
        }
        res.status(200).json({ output: stdout });
    });
}
