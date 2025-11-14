import geopandas as gpd
import matplotlib.pyplot as plt
import psycopg2
import logging

# Set up logging
logging.basicConfig(
    filename='plot_data.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Database connection parameters
db_params = {
    'dbname': 'galamsey_db',
    'user': 'ecologshit',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

try:
    # Connect to the PostGIS database
    logging.info("Connecting to PostGIS database...")
    conn = psycopg2.connect(
        dbname=db_params['dbname'],
        user=db_params['user'],
        password=db_params['password'],
        host=db_params['host'],
        port=db_params['port']
    )
    logging.info("Database connection established")

    # Read data from PostGIS using geopandas with a psycopg2 connection
    logging.info("Reading water_quality data...")
    water_quality = gpd.read_postgis("SELECT * FROM water_quality", conn, geom_col='geom')
    logging.info(f"Loaded {len(water_quality)} rows from water_quality")

    logging.info("Reading rivers data...")
    rivers = gpd.read_postgis("SELECT * FROM rivers", conn, geom_col='geom')
    logging.info(f"Loaded {len(rivers)} rows from rivers")

    logging.info("Reading landuse data...")
    landuse = gpd.read_postgis("SELECT * FROM landuse WHERE landuse IN ('quarry', 'industrial', 'wasteland', 'brownfield', 'construction', 'dump')", conn, geom_col='geom')
    logging.info(f"Loaded {len(landuse)} rows from landuse")

    # Plot
    logging.info("Generating plot...")
    fig, ax = plt.subplots(figsize=(10, 10))
    rivers.plot(ax=ax, color='blue', linewidth=1, label='Rivers')
    landuse.plot(ax=ax, color='green', linewidth=2, label='Land Use (Mining-Related)')
    water_quality.plot(ax=ax, color='red', markersize=water_quality['mercury']*1000, label='Water Quality (Mercury)')
    plt.legend()
    plt.title("Water Quality, Rivers, and Mining-Related Land Use in Pra River Basin")
    plt.savefig("galamsey_map.png")
    plt.show()
    logging.info("Plot saved as galamsey_map.png")

except Exception as e:
    logging.error(f"An error occurred: {str(e)}")
    raise

finally:
    # Close the connection
    if 'conn' in locals():
        conn.close()
    logging.info("Database connection closed")

logging.info("Visualization complete!")
