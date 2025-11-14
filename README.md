# ETL-Pipeline-for-Analyzing-Illegal-Mining
This project developed an ETL pipeline to analyze the environmental impact of galamsey (illegal gold mining) in Ghana’s Pra River Basin.
The pipeline extracts geospatial data from OpenStreetMap (OSM) and mocked water quality data, transforms it to map affected areas and quantify pollution (focusing on mercury), and loads it into a PostgreSQL/PostGIS database for analysis. The goal was to provide actionable insights into galamsey’s toll on regions like Ashanti (Kumasi) and Western (Sekondi), supporting regulatory efforts and public awareness through visualizations.

## Technology and Tool Stacks
o Python: You used pandas, geopandas, and osmnx as planned (e.g., extract_osm.py, clean_pollution.py). 
o Airflow: Used to orchestrate the pipeline (http://localhost:8080/dags/galamsey_etl/grid). 
o PostgreSQL/PostGIS: Used for storage, with screenshots (water_quality_count.png, etc.) as proof.
o Visualization: matplotlib for galamsey_map.png, Looker Studio for the dashboard (Bubble Map, Bar Chart). 
o Monitoring: Not implemented (Prometheus/Grafana were optional). 

## Approach & Methodology 

2.1 Data Import 
o Extracted OSM geospatial data (rivers, land use like construction and industrial) for the Pra River Basin using osmnx in extract_osm.py.
o Used mocked water quality data (pra_water_quality.csv) with metrics like mercury, arsenic, lead, and turbidity for locations including Kumasi, Sekondi, and Twifo Praso, due to challenges accessing OpenAQ and Ghana EPA data.

2.2 Data Transformation 
o Cleaned the water quality data using clean_pollution.py, producing pra_water_quality_cleaned.csv.
o Calculated distances between water quality points and rivers (dist_river) and land use (dist_landuse) using geopandas.
Created galamsey_analysis.csv with enriched data, including a GeoLocation field (CONCAT(Latitude, ", ", Longitude)) for mapping 

2.3 Data Loading 
o Loaded the data into PostgreSQL/PostGIS with tables for water quality and geospatial features.
o Used psycopg2 for batch inserts, with screenshots (water_quality_count.png, rivers_count.png, landuse_count.png, water_quality_stats.png) confirming the database contents (see screenshots/ folder). 

2.4 Data Analysis & Visualization 
o Static Map: Generated galamsey_map.png using matplotlib to show water quality points and mining areas (see screenshots/ folder).
o Interactive Dashboard: Built in Looker Studio https://lookerstudio.google.com/reporting/0ad889a5-4aa3-42ed-be2b-2ebf0349de11
o Bubble Map: Plots Kumasi and Sekondi (filtered by landuse: construction, industrial) with bubbles sized and colored by mercury levels.
Bar Chart: Compares average mercury levels (Kumasi: 0.05 ppm, Sekondi: 0.03 ppm).
Screenshot: dashboard_screenshot.png (see screenshots/ folder).

## Key Findings  
Kumasi (mercury: 0.05 ppm) and Sekondi (mercury: 0.03 ppm) are near industrial and construction areas, suggesting a link between mining-related land use and water pollution. Kumasi is ~1.55 km from an industrial area, while Sekondi is ~0.9 km from an industrial area and ~2.15 km from a construction area.

Twifo Praso (mercury: 0.07 ppm) is ~0.76 km from a river but has no associated land use, indicating possible direct pollution from galamsey into the river.
The Pra River Basin is at risk of mercury contamination, with higher levels near mining-related areas, highlighting the need for stricter regulations. 


