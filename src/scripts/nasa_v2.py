# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 18:03:05 2024

@author: Kayalvili
"""

import pandas as pd
import folium
from folium.plugins import HeatMapWithTime
import json

# Load your dataset
file_path = r'C:\Users\Kayalvili\OneDrive\Desktop\NASAchallenge\Air_quality_data.csv'  # Replace with your actual file path
data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Remove rows with NA or 0 in the 'Timestamp' column
data = data.dropna(subset=['Timestamp'])  # Remove rows where Timestamp is NA
data = data[data['Timestamp'] != '0']     # Remove rows where Timestamp is '0'

only_date = lambda x: str(x).split(' ')[0]

data['Timestamp'] = data['Timestamp'].apply(only_date)

# Function to handle multiple date formats and convert them to a consistent format '%d-%m-%Y'
def convert_to_datetime(timestamp):
    # Try converting using the first format
    try:
        return pd.to_datetime(timestamp, format='%m/%d/%Y')
    except (ValueError, TypeError):
        # If it fails, try the second format
        try:
            return pd.to_datetime(timestamp, format='%d-%m-%Y')
        except (ValueError, TypeError):
            return pd.to_datetime(timestamp, errors='coerce')  # Handle other cases and errors

# Apply the function to the 'Timestamp' column
data['Timestamp'] = data['Timestamp'].apply(convert_to_datetime)

# Drop rows with missing latitude, longitude, or PM2.5 values
data = data.dropna(subset=['Latitude', 'Longitude', 'PM2.5 (µg/m³)'])

# Extract day and month for grouping and display
data['Date'] = data['Timestamp'].dt.date
data['Month'] = data['Timestamp'].dt.strftime('%B %Y')  # Format as "Month Year"

data['PM2.5 (µg/m³)'] = data['PM2.5 (µg/m³)'].astype(float)

# Group data by City and Date
grouped = data.groupby('Date')

# Prepare heatmap data, pollutant values, and city names for each day
heat_data_per_day = []
city_pollutant_values_per_day = []
time_index = []

for date, group in grouped:
    heat_data_per_day.append([[row['Latitude'], row['Longitude'], row['PM2.5 (µg/m³)']] for index, row in group.iterrows()])
    
    # Prepare a sorted list of city, pollutant name, and value for each city (sorted by city name)
    city_pollutant_values_per_day.append(
        sorted([[row['City'], row['PM2.5 (µg/m³)']] for index, row in group.iterrows()])
    )
    time_index.append(group['Month'].values[0])  # Store the month for each day

# Create a base map centered around India with zoom level 4 to cover the entire country
india_map = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

# Define a gradient from green (low) to red (high)
gradient = {0.2: 'green', 0.4: 'yellow', 0.6: 'orange', 1: 'red'}

# Create a HeatMapWithTime layer with daily data and time_index to show the month
HeatMapWithTime(
    heat_data_per_day,
    index=time_index,  # Display the month on the map
    radius=25,
    gradient=gradient,
    max_opacity=0.8,
    min_opacity=0.8,
    use_local_extrema=True,min_speed = 2.5,
).add_to(india_map)

# Use json.dumps() to serialize Python lists into JSON format for safe inclusion in JavaScript
time_index_json = json.dumps(time_index)
city_pollutant_values_json = json.dumps(city_pollutant_values_per_day)

# # Inject custom HTML and CSS to split the screen into two sections: map and the info box
# title_html = '''
#              <style>
#              .container {
#                  display: flex;
#                  justify-content: space-between;
#                  height: 100vh;
#              }
#              .map-container {
#                  width: 60%;
#                  height: 100%;
#              }
#              .info-container {
#                  width: 40%;
#                  padding: 20px;
#                  background-color: white;
#                  overflow-y: auto;
#                  border-right: 1px solid black;
#              }
#              .city-list {
#                  display: flex;
#                  flex-direction: column;
#                  gap: 5px;
#              }
#              .city-row {
#                  display: flex;
#                  justify-content: space-between;
#                  align-items: center;
#                  padding: 8px;
#                  border-radius: 5px;
#                  color: white;
#                  font-weight: bold;
#              }
#              .city-name {
#                  flex: 1;
#              }
#              .pm-value {
#                  background-color: black;
#                  padding: 5px 10px;
#                  border-radius: 5px;
#              }
#              .low {
#                  background-color: green;
#              }
#              .moderate {
#                  background-color: yellow;
#              }
#              .high {
#                  background-color: red;
#              }
#              </style>
#              <div class="container">
#                  <div class="info-container">
#                      <h4>Current Month: <span id="month_label">{ time_index[0] }</span></h4>
#                      <div class="city-list" id="city_pollutant_list">
#                          ''' + ''.join(f'<div class="city-row {{get_pm_class({value})}}"><div class="city-name">{city}</div><div class="pm-value">{value} µg/m³</div></div>' for city, value in city_pollutant_values_per_day[0]) + '''
#                      </div>
#                  </div>
#                  <div class="map-container" id="map"></div>
#              </div>
#              <script>
#                  var month_label = document.getElementById("month_label");
#                  var city_pollutant_list = document.getElementById("city_pollutant_list");
#                  var time_index = ''' + time_index_json + ''';
#                  var city_pollutant_values = ''' + city_pollutant_values_json + ''';

#                  // Function to determine class based on PM2.5 value
#                  function get_pm_class(value) {
#                      if (value <= 50) {
#                          return "low";
#                      } else if (value <= 100) {
#                          return "moderate";
#                      } else {
#                          return "high";
#                      }
#                  }

#                  // Function to update the city list and month based on the slider value
#                  function updateLabels() {
#                      var slider = document.querySelector('.leaflet-control-timecontrol-slider');
                     
#                      slider.addEventListener('input', function() {
#                          var index = parseInt(slider.value, 10);
#                          month_label.innerText = time_index[index];  // Update the displayed month

#                          city_pollutant_list.innerHTML = city_pollutant_values[index].map(function(row) {
#                              return '<div class="city-row ' + get_pm_class(row[1]) + '"><div class="city-name">' + row[0] + '</div><div class="pm-value">' + row[1].toFixed(2) + ' µg/m³</div></div>';
#                          }).join('');
#                      });
#                  }

#                  window.onload = function() {
#                      updateLabels();
#                  };
#              </script>
#              '''
# india_map.get_root().html.add_child(folium.Element(title_html))


# Save the map to an HTML file
india_map.save(r'C:\Users\Kayalvili\OneDrive\Desktop\NASAchallenge\pollution_animated_heatmap_daily.html')

# Display the map in a Jupyter notebook (optional)
print(india_map)