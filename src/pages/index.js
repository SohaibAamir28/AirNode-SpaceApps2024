import Head from 'next/head';
import Layout from '@components/Layout';
import Section from '@components/Section';
import Container from '@components/Container';
import Map from '@components/Map';
import { useState } from 'react';
import styles from '@styles/Home.module.scss';

const DEFAULT_CENTER = [19.0760, 72.8777]; // Center on Mumbai

const cityLocations = [
  { 
    name: 'Mumbai', 
    position: [19.0760, 72.8777], 
    description: 'Diwali Festivities in Mumbai: Bright lights, firecrackers, and celebrations. Air Quality Stats: AQI: 150, Main Pollutant: PM2.5, Level: Unhealthy. Updated an hour ago.',
  },
  { 
    name: 'Hyderabad', 
    position: [17.3850, 78.4867], 
    description: 'Diwali in Hyderabad: Grand celebrations with traditional sweets and lights. Air Quality Stats: AQI: 130, Main Pollutant: PM2.5, Level: Unhealthy for Sensitive Groups. Updated 2 hours ago.',
  },
  { 
    name: 'Chennai', 
    position: [13.0827, 80.2707], 
    description: 'Chennai celebrates Diwali with a mix of traditional and modern fireworks. Air Quality Stats: AQI: 120, Main Pollutant: PM2.5, Level: Moderate. Updated 3 hours ago.',
  }
];

export default function Home() {
  const [selectedCity, setSelectedCity] = useState(null);

  return (
    <Layout>
      <Head>
        <title>AirNode NASA (AQaIFSoCM)</title>
        <meta name="description" content="Create mapping apps with Next.js Leaflet Starter" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <Section>
        <Container>
          <h1 className={styles.title}>
            AirNode Air Quality and Impacting Factors Storytelling on Community Mapping
          </h1>

          <Map className={styles.homeMap} width="800" height="400" center={DEFAULT_CENTER} zoom={5}>
            {({ TileLayer, Marker, Popup }) => (
              <>
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution="&copy; <a href=&quot;http://osm.org/copyright&quot;>OpenStreetMap</a> contributors"
                />
                {/* Loop through city locations and display markers */}
                {cityLocations.map(city => (
                  <Marker 
                    position={city.position} 
                    key={city.name} 
                    onClick={() => setSelectedCity(city.name)} 
                  >
                    <Popup>
                      <strong>{city.name}</strong> <br />
                      {city.description.split('Air Quality Stats:')[0]} {/* Display description without stats */}
                    </Popup>
                  </Marker>
                ))}
              </>
            )}
          </Map>

          {/* Display live data for selected city */}
          {selectedCity && (
            <div className={styles.cardContainer}>
              <div className={styles.card}>
                <h2>{selectedCity}</h2>
                <p>{cityLocations.find(city => city.name === selectedCity).description}</p>
              </div>
            </div>
          )}
        </Container>
      </Section>
    </Layout>
  );
}
