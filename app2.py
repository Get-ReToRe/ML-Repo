import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import haversine_distances
from math import radians

# Load data
data_tourism = pd.read_csv('tourism_with_id.csv')

# Filter data for Yogyakarta city
data_yogyakarta = data_tourism[data_tourism['City'] == 'Yogyakarta']

# Get user input
user_budget = float(input("Masukkan budget Anda: "))
user_category = input("Masukkan kategori tempat wisata: ")

# Filter data based on user input
data_filtered = data_yogyakarta[(data_yogyakarta['Price'] <= user_budget) & (data_yogyakarta['Category'] == user_category)]

# Calculate distances from Tugu Yogyakarta
def calculate_distance(lat, lon):
    tugu_lat = radians(-7.7829)  # Tugu Yogyakarta latitude
    tugu_lon = radians(110.3671)  # Tugu Yogyakarta longitude
    point_lat = radians(lat)
    point_lon = radians(lon)
    distance = haversine_distances([[tugu_lat, tugu_lon], [point_lat, point_lon]])[1][0] * 6371  # Earth radius in kilometers
    return distance

data_filtered['distance_from_tugu'] = data_filtered.apply(lambda row: calculate_distance(row['Lat'], row['Long']), axis=1)

# Sort by distance from Tugu Yogyakarta
data_filtered = data_filtered.sort_values('distance_from_tugu')

# Print recommendations
print("Rekomendasi tempat wisata di Yogyakarta berdasarkan budget dan kategori:")
for i, row in data_filtered.iterrows():
    print("Tempat Wisata:", row['Place_Name'])
    print("Kategori:", row['Category'])
    print("Harga Tiket:", row['Price'])
    print("Estimasi Jarak dari Tugu Yogyakarta:", round(row['distance_from_tugu'], 2), "kilometer")
    print("---------")
