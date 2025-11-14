import pandas as pd
import psycopg2
from shapely.geometry import Point
from shapely.wkt import dumps

# Database connection parameters
db_params = {
    'dbname': 'galamsey_db',
    'user': 'ecologshit',
    'password': '',
    'host': 'localhost',
    'port': '5432'
}

# Input file
input_file = "data/pra_water_quality_cleaned.csv"

# Read the cleaned CSV
print(f"Reading cleaned data from {input_file}...")
df = pd.read_csv(input_file)

# Create a geometry column using shapely Point objects, then convert to WKT strings
print("Creating geometry column from latitude and longitude...")
df['geom'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
df['geom'] = df['geom'].apply(lambda x: dumps(x))

# Drop latitude and longitude columns (optional, since geometry is now in 'geom')
df = df.drop(['latitude', 'longitude'], axis=1)

# Connect to the PostGIS database
print("Connecting to PostGIS database...")
conn = psycopg2.connect(
    dbname=db_params['dbname'],
    user=db_params['user'],
    password=db_params['password'],
    host=db_params['host'],
    port=db_params['port']
)
cur = conn.cursor()

# Drop the table if it exists and create a new one with a PostGIS geometry column
print("Creating table 'water_quality' with PostGIS geometry column...")
cur.execute("DROP TABLE IF EXISTS water_quality;")
cur.execute("""
    CREATE TABLE water_quality (
        location TEXT,
        mercury FLOAT,
        turbidity FLOAT,
        arsenic FLOAT,
        lead FLOAT,
        date TIMESTAMP,
        geom GEOMETRY(POINT, 4326)
    );
""")
conn.commit()

# Insert the data into PostGIS
print("Loading data into PostGIS table 'water_quality'...")
for index, row in df.iterrows():
    cur.execute("""
        INSERT INTO water_quality (location, mercury, turbidity, arsenic, lead, date, geom)
        VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326));
    """, (
        row['location'],
        row['mercury'],
        row['turbidity'],
        row['arsenic'],
        row['lead'],
        row['date'],
        row['geom']
    ))
conn.commit()

# Close the connection
cur.close()
conn.close()

print("Data loading complete!")
