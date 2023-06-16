import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from math import radians
import requests

# Load data
data_tourism = pd.read_csv('tourism_with_id.csv')

# Filter data for Yogyakarta city
data_yogyakarta = data_tourism[data_tourism['City'] == 'Yogyakarta']

# Get user input
user_budget = float(input("Masukkan budget Anda: "))
user_category = input("Masukkan kategori tempat wisata: ")

# Filter data based on user input
data_filtered = data_yogyakarta[(data_yogyakarta['Price'] <= user_budget) & (data_yogyakarta['Category'] == user_category)]

# Get current location
response = requests.get('http://ip-api.com/json')
data = response.json()
latitude = data['lat']
longitude = data['lon']

# Calculate distances from current location
def calculate_distance(lat, lon):
    current_lat = radians(latitude)  # Current location latitude
    current_lon = radians(longitude)  # Current location longitude
    point_lat = radians(lat)
    point_lon = radians(lon)
    distance = haversine_distances([[current_lat, current_lon], [point_lat, point_lon]])[1][0] * 6371  # Earth radius in kilometers
    return distance

data_filtered['distance_from_current'] = data_filtered.apply(lambda row: calculate_distance(row['Lat'], row['Long']), axis=1)

# Sort by distance from current location
data_filtered = data_filtered.sort_values('distance_from_current')

# Print recommendations
print("Rekomendasi tempat wisata di Yogyakarta berdasarkan budget dan kategori:")
for i, row in data_filtered.head(5).iterrows():
    print("Tempat Wisata:", row['Place_Name'])
    print("Kategori:", row['Category'])
    print("Harga Tiket:", row['Price'])
    print("Estimasi Jarak dari Lokasi Terkini:", round(row['distance_from_current'], 2), "kilometer")
    print("---------")
