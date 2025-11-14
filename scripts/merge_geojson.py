import json
import glob
import os

# Function to merge GeoJSON files
def merge_geojson_files(file_pattern, output_file):
    # Initialize an empty FeatureCollection
    merged = {"type": "FeatureCollection", "features": []}
    
    # Find all files matching the pattern (e.g., landuse_region_*.geojson)
    files = glob.glob(file_pattern)
    for file in files:
        with open(file, "r") as f:
            data = json.load(f)
            # Extend the features list with features from this file
            merged["features"].extend(data["features"])
    
    # Save the merged GeoJSON to the output file
    with open(output_file, "w") as f:
        json.dump(merged, f)
    print(f"Merged data saved to {output_file}")

# Merge landuse files
merge_geojson_files("data/landuse_region_*.geojson", "data/landuse_merged.geojson")

# Merge rivers files
merge_geojson_files("data/rivers_region_*.geojson", "data/rivers_merged.geojson")
