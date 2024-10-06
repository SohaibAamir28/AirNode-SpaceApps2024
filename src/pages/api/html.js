// src/pages/api/html.js
import fs from 'fs';
import path from 'path';

export default function handler(req, res) {
    const htmlPath = path.join(process.cwd(), 'public', 'pollution_animated_heatmap_daily.html');
    fs.readFile(htmlPath, 'utf8', (err, data) => {
        if (err) {
            res.status(500).json({ error: 'Error reading file' });
            return;
        }
        res.status(200).send(data);
    });
}
