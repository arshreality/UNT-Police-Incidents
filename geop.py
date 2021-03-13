import pandas as pd
import geopandas as gpd

df = pd.read_csv('incidents.csv')
print(df['Location'])
print(df['Latitude'])
print(df['Longitude'])
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
print(gdf.head())
