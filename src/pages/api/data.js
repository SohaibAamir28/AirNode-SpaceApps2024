// src/pages/api/data.js
import fs from 'fs';
import path from 'path';
import xlsx from 'xlsx';

export default function handler(req, res) {
    const filePath = path.join(process.cwd(), 'public', 'Air quality data 1.xlsx');
    const workbook = xlsx.readFile(filePath);
    const sheetName = workbook.SheetNames[0];
    const sheet = workbook.Sheets[sheetName];
    const jsonData = xlsx.utils.sheet_to_json(sheet);

    res.status(200).json(jsonData);
}
