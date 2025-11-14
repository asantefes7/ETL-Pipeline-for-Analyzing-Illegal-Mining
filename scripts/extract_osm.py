import overpy
import time
import json

# Initialize Overpass API
api = overpy.Overpass()

# Create a 4x4 grid of smaller bounding boxes for Ghana
lon_steps = [-3.5, -2.25, -1.0, 0.25, 1.5]  # 4 splits across longitude
lat_steps = [4.5, 6.25, 8.0, 9.75, 11.5]    # 4 splits across latitude
bounding_boxes = []
for i in range(len(lon_steps) - 1):
    for j in range(len(lat_steps) - 1):
        bounding_boxes.append((
            lon_steps[i], lat_steps[j],  # min_lon, min_lat
            lon_steps[i + 1], lat_steps[j + 1]  # max_lon, max_lat
        ))

# Function to convert Overpass result to GeoJSON (simplified)
def convert_to_geojson(result, data_type):
    features = []
    for way in result.ways:
        if data_type == "landuse" and "landuse" in way.tags:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[float(n.lon), float(n.lat)] for n in way.nodes]
                },
                "properties": {"landuse": way.tags.get("landuse")}
            }
            features.append(feature)
        elif data_type == "rivers" and "waterway" in way.tags:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[float(n.lon), float(n.lat)] for n in way.nodes]
                },
                "properties": {"waterway": way.tags.get("waterway")}
            }
            features.append(feature)
    return json.dumps({"type": "FeatureCollection", "features": features})

# Query each region for landuse and rivers separately
for i, (min_lon, min_lat, max_lon, max_lat) in enumerate(bounding_boxes):
    print(f"Querying region {i+1}...")
    
    # Query for landuse
    landuse_query = f"""
    [out:json][timeout:60];
    way["landuse"]({min_lat},{min_lon},{max_lat},{max_lon});
    out body;
    >;
    out skel qt;
    """
    retries = 3
    for attempt in range(retries):
        try:
            print(f"Querying landuse for region {i+1}, attempt {attempt+1}...")
            result = api.query(landuse_query)
            with open(f"data/landuse_region_{i+1}.geojson", "w") as f:
                f.write(convert_to_geojson(result, "landuse"))
            print(f"Landuse data for region {i+1} saved.")
            break
        except Exception as e:
            print(f"Error querying landuse for region {i+1}: {e}")
            if attempt < retries - 1:
                print("Retrying after 60 seconds...")
                time.sleep(60)
            else:
                print(f"Failed to query landuse for region {i+1} after {retries} attempts.")
    
    # Query for rivers
    rivers_query = f"""
    [out:json][timeout:60];
    way["waterway"="river"]({min_lat},{min_lon},{max_lat},{max_lon});
    out body;
    >;
    out skel qt;
    """
    for attempt in range(retries):
        try:
            print(f"Querying rivers for region {i+1}, attempt {attempt+1}...")
            result = api.query(rivers_query)
            with open(f"data/rivers_region_{i+1}.geojson", "w") as f:
                f.write(convert_to_geojson(result, "rivers"))
            print(f"Rivers data for region {i+1} saved.")
            break
        except Exception as e:
            print(f"Error querying rivers for region {i+1}: {e}")
            if attempt < retries - 1:
                print("Retrying after 60 seconds...")
                time.sleep(60)
            else:
                print(f"Failed to query rivers for region {i+1} after {retries} attempts.")
    
    time.sleep(10)  # Delay between regions to avoid rate limits
