import folium
from folium.plugins import HeatMap

# Sensor locations (latitude and longitude)
sensor_locations = [
    (49.897577778812305, 10.87877203473033),
    (49.89183297858489, 10.883784739544547),
    (49.89283979482464, 10.888173536975806),
    (49.89109459614897, 10.882917323748906),
    (49.890596012268006, 10.888991342449053)
] #Safectory Office, Sandstraßem, Gabelmann, Domkranz, Touristeninformation

# Counter values (number of people at each sensor location)
counterswithonlyreal = [132, 36, 159, 38, 20] #Safectory Office, Sandstraßem, Gabelmann, Domkranz, Touristeninformation
counterswithspoof = [139, 108, 252, 133, 152]
# Create a base map
m = folium.Map(location=sensor_locations[0], zoom_start=14)

# Add markers for sensor locations with counter values in popup
for (lat, lon), count in zip(sensor_locations, counters):
    folium.Marker([lat, lon], popup=f'People Count: {count}').add_to(m)

# Prepare data for the heatmap
heatmap_data = [[lat, lon, count] for (lat, lon), count in zip(sensor_locations, counters)]

# Create a heatmap layer
HeatMap(heatmap_data).add_to(m)

# Save the map to an HTML file
m.save('heatmap.html')