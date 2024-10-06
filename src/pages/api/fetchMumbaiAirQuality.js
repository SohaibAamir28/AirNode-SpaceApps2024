import axios from 'axios';
import cheerio from 'cheerio';

export default async function handler(req, res) {
  try {
    const response = await axios.get('https://www.iqair.com/india/maharashtra/mumbai');
    const html = response.data;
    const $ = cheerio.load(html);

    const airQualityStats = {
      aqi: $('.aqi-value').text().trim(),
      mainPollutant: $('.main-pollutant').text().trim(),
      level: $('.aqi-level').text().trim(),
      time: $('.aqi-time').text().trim(),
      characteristics: {
        type: 'Reference grade',
        owner: 'Unknown Governmental Organization',
        measures: 'PM2.5 µg/m³',
        reporting: `Updated ${$('.aqi-time').text().trim()}`,
        since: '10/11/2016',
        provider: 'AirNow',
      },
    };

    res.status(200).json(airQualityStats);
  } catch (error) {
    console.error('Error fetching air quality data:', error);
    res.status(500).json({ error: 'Failed to fetch air quality data' });
  }
}
