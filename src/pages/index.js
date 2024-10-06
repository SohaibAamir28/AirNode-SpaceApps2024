// src/pages/index.js
import React from 'react';

const Home = () => {
    return (
        <div style={{ width: '100%', height: '100vh', margin: 0, padding: 0 }}>
            <h1>Air Quality Dashboard</h1>
            <iframe
                src="/pollution_animated_heatmap_daily.html" // Path to your HTML file in the public folder
                style={{ width: '100%', height: '90%', border: 'none' }}
                title="Air Quality Heatmap"
            />
        </div>
    );
};

export default Home;
