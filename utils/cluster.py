import folium
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from utils.constant import LABEL_COLOR, popup_html_item, popup_center_item
from pyproj import Geod
import numpy as np

def find_centroids(cls_df, n_clusters=3):
    scaler = MinMaxScaler()
    X = scaler.fit_transform(cls_df.iloc[:,0:2])
    weight = cls_df.iloc[:,2].values

    kmeans = KMeans(n_clusters = n_clusters, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
    wt_kmeansclus = kmeans.fit(X,sample_weight=weight)
    labels = kmeans.predict(X,sample_weight=weight)
    centroids = kmeans.cluster_centers_.reshape(-1, 2)
    
    return scaler, centroids, labels

def calculate_distance(pt1, pt2):
    
    g = Geod(ellps='WGS84')
    # 2D distance in meters with longitude, latitude of the points
    azimuth1, azimuth2, distance_2d = g.inv(pt1[1], pt1[0], pt2[1], pt2[0])
    return round((distance_2d / 1000.0), 2)

def normalize_sizes(sizes):
    min_size = min(sizes)
    max_size = max(sizes)
    normalized_sizes = [(size - min_size) / (max_size - min_size) for size in sizes]
    return normalized_sizes 

def generate_map(df_stateonly, weight_attr, n_clusters=3):
    
    dims = ["province_lat", "province_long", weight_attr]
    cls_df = df_stateonly[dims]
    
    scaler, centroids, labels = find_centroids(cls_df, n_clusters=n_clusters)
    df_stateonly['labels'] = labels
    
    zooming = 30 # In case of using normalization, the numbers will be pretty small; therefore, we should multiply
             # the normalized figures with a number for enlarging it 
             
    # Sample data: latitude, longitude, size, and labels of each point
    sizes = normalize_sizes(df_stateonly[weight_attr])
    
    
    latitude = df_stateonly['province_lat']
    longitude = df_stateonly['province_long']
    labels = df_stateonly['labels']
    
    # addtional information
    state_province_name = df_stateonly["state_province_name"]
    product_count = df_stateonly["product_count"]
    total_sale = df_stateonly["total_sale"]
    average_order_sale = df_stateonly["average_order_sale"]
    order_count = df_stateonly["order_count"]
    total_discount = df_stateonly["total_discount"]

    # Create a Folium Map centered at an initial location
    m = folium.Map(location=[latitude.mean(), longitude.mean()], zoom_start=4)
    cluster_centers = scaler.inverse_transform(centroids)
    
    for idx, center in enumerate(cluster_centers):
        folium.Marker(location=center, icon=folium.Icon(color=LABEL_COLOR[idx], icon='home'), popup=popup_center_item(center[0], center[1], idx)).add_to(m)

    # Plot points on the map with different colors based on labels
    for lat, lon, size, label, state_province_name, product_count, average_order_sale, total_sale, order_count, total_discount in zip(latitude, longitude, sizes, labels, state_province_name, product_count, average_order_sale, total_sale, order_count, total_discount):
        radius = (size * zooming) + 1.0
        distance = calculate_distance(cluster_centers[label], [lat, lon])
        popup_text = popup_html_item(lat, lon, labels, state_province_name, product_count, average_order_sale, total_sale, order_count, total_discount, distance)
        
        
        folium.CircleMarker(location=[lat, lon],
                            radius=radius,
                            color=LABEL_COLOR[label], 
                            fill=True, fill_color=LABEL_COLOR[label], 
                            fill_opacity=0.6, 
                            popup=popup_text).add_to(m)
        
        # folium.Marker(
        #     location=[lat, lon],
        #     icon=folium.Icon()
        # ).add_to(m)

    # Plot cluster centers as markers
    
    return m
