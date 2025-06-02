import json
import logging
import fiona
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
pd.options.mode.chained_assignment = None

def read_data(mode: str, input_data: str, encoding: str = "UTF-8"):
    try:
        logging.info("Read file use gdf [START]")
        if mode == "1":  # New
            gdf = input_data
        else:
            gdf: gpd.GeoDataFrame = gpd.read_file(input_data, encoding=encoding, engine='pyogrio', use_arrow=True)
        return gdf

    except Exception as e:
        logging.error(f"Error: {e} [FAIL]")
        try:
            collection = list(fiona.open(input_data, "r"))
            df1 = pd.DataFrame(collection)

            # Check Geometry
            def isvalid(geom):
                try:
                    shape(geom)
                    return 1
                except ValueError:
                    return 0

            df1["isvalid"] = df1["geometry"].apply(lambda x: isvalid(x))
            df1 = df1[df1["isvalid"] == 1]
            collection = json.loads(df1.to_json(orient="records"))

            # Convert to geodataframe
            gdf = gpd.GeoDataFrame.from_features(collection)
            gdf.set_crs("EPSG:4326")
            return gdf
        except Exception as e:
            logging.error(f"Error: {e} [FAIL]")
            return gpd.GeoDataFrame()
