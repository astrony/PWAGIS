from rtree import index
import geopandas as gpd
import pandas as pd
from shapely.geometry import MultiPoint, MultiPolygon, MultiLineString, LineString, Point
import logging
import sys
import os
import json
import csv
from pwagis.topology_check.lib.read_file import read_data
from pwagis.topology_check.lib.result import result_json


def point_snap(input: gpd.GeoDataFrame, _overlay: gpd.GeoDataFrame, value: str = False) -> None:
    logging.info('Start processing point_snap [START]')
    try:
        if value:
            value_st = 'true'
            value_sp = 'false'
        else:
            value_st = 'false'
            value_sp = 'true'
            
        # select only the columns geometry
        # convert crs
        _input = input.to_crs('EPSG:32647')
        _overlay = _overlay.to_crs('EPSG:32647')
        # buffer _overlay
        _overlay['geometry'] = _overlay.buffer(0.01)
        _overlay = _overlay[['geometry']]
        # Spatial join to identify points inside polygons
        try:
            joined_data = gpd.sjoin(_input, _overlay, how='left', predicate='within')
        except Exception as e:
            print("sjoin",e)
            joined_data = gpd.sjoin(_input, _overlay, how='left', op='within')
        
        # If index_right is NaN, point is outside polygon, otherwise inside
        joined_data['topo_point_snap'] = joined_data['index_right'].isna()
        
        # Convert boolean values to string 'true' and 'false'
        joined_data['topo_point_snap'] = joined_data['topo_point_snap'].map({True: value_st, False: value_sp})
        
        try :
            joined_data = joined_data.drop(columns=['index_right'])
        except Exception as e:
            logging.error(f'Error: {e}')

        joined_data = joined_data.to_crs('EPSG:4326')
        
        return joined_data
        
    except Exception as e:
        logging.error(f'Error in point_snap processing: {e}')
        _input['topo_point_snap'] = f'error: {e}'
        return _input
    
def point_out_region(input: gpd.GeoDataFrame, _overlay: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Log message with info level
    logging.info('Start processing point_out_region [START]')
    
    try:
        # select only the columns geometry
        _overlay = _overlay[['geometry']]
        # Spatial join to identify points inside polygons
        try:
            # new version
            joined_data = gpd.sjoin(input, _overlay, how='left', predicate='within')
        except Exception as e:
            print("sjoin",e)
            # old version
            joined_data = gpd.sjoin(input, _overlay, how='left', op='within')
        
        # If index_right is NaN, point is outside polygon, otherwise inside
        joined_data['topo_point_outregion'] = joined_data['index_right'].isna()
        
        # Convert boolean values to string 'true' and 'false'
        joined_data['topo_point_outregion'] = joined_data['topo_point_outregion'].map({True: 'true', False: 'false'})
        
        try :
            joined_data = joined_data.drop(columns=['index_right'])
        except Exception as e:
            print(e)

        try:
            # ตรวจสอบว่าคอลัมน์ 'x' และ 'y' มีอยู่ใน DataFrame หรือไม่
            if 'x' in joined_data.columns and 'y' in joined_data.columns:
                # ลบคอลัมน์ 'x' และ 'y' ออกจาก DataFrame
                joined_data = joined_data.drop(columns=['x', 'y'])
                logging.info("Successfully dropped columns 'x' and 'y' from DataFrame.")
            else:
                logging.error("Columns 'x' and 'y' not found in DataFrame.")
        except Exception as e:
            print("An error occurred:", e)
        return joined_data
        
    except Exception as e:
        logging.error(f'Error in point_in_polygon processing: {e}')
        input['topo_point_outregion'] = f'error: {e}'
        return input

def point_multipart(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing point_multipart [START]')
    
    try :
        # ตรวจสอบประเภทเรขาคณิตและอัปเดตคอลัมน์ "aaa"
        input['topo_multipoint'] = input['geometry'].apply(lambda geom: 'true' if isinstance(geom, MultiPoint) else 'false')
        return input
    
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_multipoint'] = f'error: {e}'
        return input
            
def point_duplicates(input: gpd.GeoDataFrame, column: str = False) -> None:
    # Log message with info level
    logging.info('Start processing point_duplicates [START]')
    
    try :
        if not column:
            input['point_duplicates_ids'] = range(1, len(input) + 1)
        else:
            input['point_duplicates_ids'] = input[column]
            
        input['x'] = input['geometry'].x
        input['y'] = input['geometry'].y
        duplicates = input[input.duplicated(subset='geometry', keep=False)]

        # รวมรายการ ID ที่ซ้ำกันในรายการละติจูดและลองจิจูด
        duplicate_ids = duplicates.groupby(['x', 'y'])['point_duplicates_ids'].apply(list).reset_index()
        
        # เพิ่มคอลัมน์ใหม่ใน DataFrame หลัก
        input['point_duplicates'] = input.apply(lambda row: duplicate_ids[(duplicate_ids['x'] == row['x']) & (duplicate_ids['y'] == row['y'])]['point_duplicates_ids'].tolist(), axis=1)
        input['point_duplicates'] = input['point_duplicates'].apply(lambda x: x if x else 'false')
        input['point_duplicates'] = input['point_duplicates'].astype(str)
        
        # อัปเดตคอลัมน์ topo_point_duplicates2 ตามเงื่อนไขที่กำหนด
        input.loc[input['point_duplicates'] == 'false', 'topo_point_duplicates'] = 'false'
        input.loc[input['point_duplicates'] != 'false', 'topo_point_duplicates'] = 'true'

        # ถ้า point_duplicates เป็น 'false' ให้ point_duplicates_ids เป็น null
        input.loc[input['point_duplicates'] == 'false', 'point_duplicates_ids'] = None
        try:
            # ตรวจสอบว่าคอลัมน์ 'x' และ 'y' มีอยู่ใน DataFrame หรือไม่
            if 'x' in input.columns and 'y' in input.columns:
                # ลบคอลัมน์ 'x' และ 'y' ออกจาก DataFrame
                input = input.drop(columns=['x', 'y'])
                logging.info("Successfully dropped columns 'x' and 'y' from DataFrame.")
            else:
                logging.error("Columns 'x' and 'y' not found in DataFrame.")
        except Exception as e:
            print("An error occurred:", e)

        return input
    
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_point_duplicates'] = f'error: {e}'
        return input

def line_short(input: gpd.GeoDataFrame, distance: float) -> None:
    
    # Log message with info level
    logging.info('Start processing line_short [START]')
    try :
        input.to_crs(epsg=3857, inplace=True)
        # สร้างคอลัมน์ 'shortlen' และกำหนดค่าเป็น True หรือ False ตามความยาว
        input['topo_line_shortlen'] = input.length <= distance
        input.to_crs(epsg=4326, inplace=True)
        input['topo_line_shortlen'] = input['topo_line_shortlen'].map({True: 'true', False: 'false'})
        return input
    
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_shortlen'] = f'error: {e}'
        return input

def line_duplicates(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing line_duplicates [START]')
    try:
        logging.info('Read file use gdf [START]')
        # Identify and mark duplicates
        logging.info('Processing Duplicate line [START]')
        input['topo_line_duplicates'] = input.duplicated(subset='geometry', keep=False)
        input['topo_line_duplicates'] = input['topo_line_duplicates'].map({True: 'true', False: 'false'})
        return input
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_duplicates'] = f'error: {e}'
        return input

def line_outregion(input: gpd.GeoDataFrame, _overlay: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Log message with info level
    logging.info('Start processing line_outregion [START]')
    
    try:
        # select only the columns geometry
        _overlay = _overlay[['geometry']]
        # Spatial join to identify points inside polygons
        try:
            # new version
            joined_data = gpd.sjoin(input, _overlay, how='left', predicate='intersects')
        except Exception as e:
            print("sjoin",e)
            # old version
            joined_data = gpd.sjoin(input, _overlay, how='left', op='intersects')
        
        # If index_right is NaN, point is outside polygon, otherwise inside
        joined_data['topo_line_outregion'] = joined_data['index_right'].isna()
        
        # Convert boolean values to string 'true' and 'false'
        joined_data['topo_line_outregion'] = joined_data['topo_line_outregion'].map({True: 'true', False: 'false'})
        
        try :
            joined_data = joined_data.drop(columns=['index_right'])
        except Exception as e:
            print(e)

        try:
            # ตรวจสอบว่าคอลัมน์ 'x' และ 'y' มีอยู่ใน DataFrame หรือไม่
            if 'x' in joined_data.columns and 'y' in joined_data.columns:
                # ลบคอลัมน์ 'x' และ 'y' ออกจาก DataFrame
                joined_data = joined_data.drop(columns=['x', 'y'])
                logging.info("Successfully dropped columns 'x' and 'y' from DataFrame.")
            else:
                logging.error("Columns 'x' and 'y' not found in DataFrame.")
        except Exception as e:
            print("An error occurred:", e)
        return joined_data
    
    except Exception as e:
        logging.error(f'Error in line_out_region processing: {e}')
        input['topo_line_outregion'] = f'error: {e}'
        return input

def line_multipart(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing line_multipart [START]')
    
    try :
        # ตรวจสอบประเภทเรขาคณิตและอัปเดตคอลัมน์ "aaa"
        input['topo_multiline'] = input['geometry'].apply(lambda geom: 'true' if isinstance(geom, MultiLineString) else 'false')
        return input
    
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_multiline'] = f'error: {e}'
        return input

def line_invalid(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing line_invalid [START]')
    
    try:
        # Identify and mark invalid polygons
        input['ไม่ถูกค้องtopo_line_invalid'] = input['geometry'].is_valid.map({True: 'false', False: 'true'})
        return input
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['ไม่ๆๆtopo_line_invalid'] = f'error: {e}'
        return input

def is_self_intersect(line):
    """
    ตรวจสอบว่าเส้นท่อมีส่วนใด ๆ ที่หักงอและทับซ้อนตัวเองหรือไม่
    """
    return not line.is_simple

def get_self_intersecting_parts(line):
    """
    ดึงส่วนที่ทับซ้อนตัวเองของเส้นท่อ
    """
    return line.intersection(line)

def line_self_intersect(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing line_self_intersect [START]')
    try:
        # สร้างคอลัมน์ 'topo_line_selfintersect' และกำหนดค่าเริ่มต้นเป็น 'false'
        input['topo_line_selfintersect'] = 'false'

        # ตรวจสอบการตัดกันของเส้นรูปทรงเหลี่ยมแต่ละเส้น
        for index, row in input.iterrows():
            # ตรวจสอบว่าเส้นรูปทรงเหลี่ยมมีการตัดกันหรือไม่
            if not row['geometry'].is_simple:
                # หากมีการตัดกัน กำหนดค่าในคอลัมน์ 'topo_line_selfintersect' เป็น 'true'
                input.at[index, 'topo_line_selfintersect'] = 'true'
        return input
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_selfintersect'] = f'error: {e}'
        return input

def line_duplicate_node(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing line_duplicate_node [START]')
    
    try:
        input['topo_line_duplicate_node'] = 'false'
        # Check if the line has duplicate nodes
        for index, row in input.iterrows():
            geom = row.geometry
            if isinstance(geom, (LineString, MultiLineString)):
                coords = []
                if isinstance(geom, LineString):
                    coords = geom.coords
                elif isinstance(geom, MultiLineString):
                    for part in geom.geoms:
                        coords.extend(part.coords)
                # Check if the line has duplicate nodes
                if len(coords) != len(set(coords)):
                    # If there are duplicate nodes, set the value in the 'topo_line_duplicate_node' column to 'true'
                    input.at[index, 'topo_line_duplicate_node'] = 'true'
        
        return input
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_duplicate_node'] = f'error: {e}'
        return input

def line_nonconect(input: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Log message with info level
    logging.info('Start processing line_not_connect [START]')
    try:
        gdf_copy = input.copy(deep=True)

        try:
            gdf_sj = gpd.sjoin(input, gdf_copy, how='inner', predicate='intersects')
        except Exception as e:
            logging.error(f'Error spatial join : {e} [FAIL]')
            gdf_sj = gpd.sjoin(input, gdf_copy, how='inner', op='intersects')

        # Value counts of intersections
        gdf_sj_vc = gdf_sj['PIPE_ID_left'].value_counts()

        # Intersection mask for lines with more than one intersection
        int_mask = gdf_sj_vc.ge(2)

        # Add the intersection mask to gdf_sj as 'intersects' column
        gdf_sj['topo_line_not_connect'] = gdf_sj['PIPE_ID_left'].map(int_mask)

        # Filter non-intersecting lines
        gdf_no_intersect = gdf_sj.loc[gdf_sj['topo_line_not_connect'] == False]
        gdf_no_intersect['topo_line_not_connect'] = "true"

        # join column topo_line_not_connect the original gdf with the non-intersecting lines
        gdf_pipe = pd.merge(input, gdf_no_intersect[['PIPE_ID_left', 'topo_line_not_connect']], how='left', left_on='PIPE_ID', right_on='PIPE_ID_left')
        gdf_pipe.drop(columns='PIPE_ID_left', inplace=True)
        
        logging.info('Processing line_not_connect [END]')
        return gdf_pipe
    
    except Exception as e:
        # Log message with error level
        # error message line
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
        print(msg)
        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_not_connect'] = f'error: {e}'
        return input

def check_overshoot(input: gpd.GeoDataFrame, batch_gdf: gpd.GeoDataFrame, distance: float) -> None:
    for idx, row in batch_gdf.iterrows():
        line1 = row['geometry']
        for _, inner_row in batch_gdf.iterrows():
            if idx != inner_row.name:
                line2 = inner_row['geometry']
                if line1.intersects(line2) and line1.length < distance:
                    input.at[idx, 'topo_line_overshoot'] = "true"
                    break

def line_overshoot(input: gpd.GeoDataFrame, distance: float = 0.5) -> None:
    # Log message with info level
    logging.info('Start processing line_overshoot [START]')
    try:
        # to crs 3857
        input.to_crs(epsg=32647, inplace=True)

        # สร้างคอลัมน์ 'overlap' และกำหนดค่าเริ่มต้นเป็น False
        input['topo_line_overshoot'] = "false"

        # แบ่งข้อมูลเป็นชุดข้อมูลขนาดเล็ก ๆ ครั้งละ 100 แถว
        batch_size = 1000
        num_batches = (len(input) + batch_size - 1) // batch_size

        # ตรวจสอบการทับซ้อนของเส้นทางและอัปเดตคอลัมน์ 'overlap' ตามเงื่อนไข
        for batch_index in range(num_batches):
            start_index = batch_index * batch_size
            end_index = min((batch_index + 1) * batch_size, len(input))
            
            # เลือกชุดข้อมูลที่จะประมวลผลในรอบนี้
            batch_gdf = input.iloc[start_index:end_index]
            
            # print("topo_line_overshoot :",start_index,end_index)
            
            check_overshoot(input, batch_gdf, distance)

        # to crs 4326
        input.to_crs(epsg=4326, inplace=True)
        return input
    
    except Exception as e:
        # Log message with error level
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
        print(msg)
        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_overshoot'] = f'error: {e}'
        return input
    
def check_distance_to_others(gdf, current_idx, point, distance_threshold):
    for idx, row in gdf.iterrows():
        if idx != current_idx:
            distance = row.geometry.distance(point)
            if 0 < distance <= distance_threshold and row.geometry.intersects(point):
                return "true"
    return "false"

def line_undershoot(input: gpd.GeoDataFrame, distance: float = 0.05) -> gpd.GeoDataFrame:  # 5 cm = 0.05 meters
    # Log message with info level
    logging.info('Start processing line_undershoot [START]')
    try:
        # Convert CRS to EPSG:32647
        try:
            _input = input.to_crs(epsg=32647)
        except Exception as e:
            print(e)
            _input = input.to_crs(epsg=32647, inplace=True)

        # Create a new column to store the results
        _input['topo_line_undershoot'] = "false"

        # Define chunk size for processing
        chunk_size = 1000
        start_index = 0
        end_index = chunk_size

        while start_index < len(_input):
            # Slice GeoDataFrame to process in chunks
            subset_gdf = _input.iloc[start_index:end_index]
            
            logging.info(f"Processing chunk: {start_index} to {end_index}")

            # Iterate over each row in the subset GeoDataFrame
            for idx, row in subset_gdf.iterrows():
                # Process the geometry to find the last node
                geom = row.geometry
                last_points = []
                if isinstance(geom, LineString):
                    last_points = [geom.coords[-1]]
                elif isinstance(geom, MultiLineString):
                    for part in geom.geoms:
                        last_points.append(part.coords[-1])
                
                far_from_others = "false"
                for last_point in last_points:
                    last_node = Point(last_point)
                    # Check the distance from the last node to other lines <= 5 cm and > 0 cm
                    far_from_others = check_distance_to_others(subset_gdf, idx, last_node, distance)
                    if far_from_others == "true":
                        break

                # Update the new column with the result
                _input.at[idx, 'topo_line_undershoot'] = far_from_others

            # Update indices for the next chunk
            start_index += chunk_size
            end_index += chunk_size

        # Convert CRS back to EPSG:4326
        try:
            _input = input.to_crs(epsg=4326)
        except Exception as e:
            print(e)
            _input = input.to_crs(epsg=4326, inplace=True)
        
        logging.info('Processing line_undershoot [END]')
        return _input
    
    except Exception as e:
        # Log message with error level
        # error message line
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
        print(msg)

        logging.error(f'Error: {e} [FAIL]')
        input['topo_line_undershoot'] = f'error: {e}'
        return input

def polygon_out_region(input: gpd.GeoDataFrame, _overlay: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Log message with info level
    logging.info('Start processing polygon_out_region [START]')
    
    try:
        # select only the columns geometry
        _overlay = _overlay[['geometry']]
        # Spatial join to identify points inside polygons
        try:
            joined_data = gpd.sjoin(input, _overlay, how='left', predicate='intersects')
        except Exception as e:
            print("sjoin",e)
            joined_data = gpd.sjoin(input, _overlay, how='left', op='intersects')
        
        # If index_right is NaN, point is outside polygon, otherwise inside
        joined_data['topo_pologon_outregion'] = joined_data['index_right'].isna()
        
        # Convert boolean values to string 'true' and 'false'
        joined_data['topo_pologon_outregion'] = joined_data['topo_pologon_outregion'].map({True: 'true', False: 'false'})
        
        try :
            joined_data = joined_data.drop(columns=['index_right'])
        except Exception as e:
            print(e)
    
        try:
            # ตรวจสอบว่าคอลัมน์ 'x' และ 'y' มีอยู่ใน DataFrame หรือไม่
            if 'x' in joined_data.columns and 'y' in joined_data.columns:
                # ลบคอลัมน์ 'x' และ 'y' ออกจาก DataFrame
                joined_data = joined_data.drop(columns=['x', 'y'])
                logging.info("Successfully dropped columns 'x' and 'y' from DataFrame.")
            else:
                logging.error("Columns 'x' and 'y' not found in DataFrame.")
        except Exception as e:
            print("An error occurred:", e)
        return joined_data
        
    except Exception as e:
        logging.error(f'Error in polygon_out_region processing: {e}')
        input['topo_pologon_outregion'] = f'error: {e}'
        return input

def polygon_duplicates(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing polygon_duplicates [START]')
    try:
        logging.info('Read file use gdf [START]')
        # Identify and mark duplicates
        logging.info('Processing Duplicate point [START]')
        input['topo_polygon_duplicates'] = input.duplicated(subset='geometry', keep=False)
        input['topo_polygon_duplicates'] = input['topo_polygon_duplicates'].astype(str).str.lower()
        return input
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_polygon_duplicates'] = f'error: {e}'
        return input

def polygon_multipart(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing polygon_multipart [START]')
    
    try :
        # ตรวจสอบประเภทเรขาคณิตและอัปเดตคอลัมน์ "aaa"
        input['topo_multipolygon'] = input['geometry'].apply(lambda geom: 'true' if isinstance(geom, MultiPolygon) else 'false')
        return input
    
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_multipolygon'] = f'error: {e}'
        return input

def polygon_invalid(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing polygon_invalid [START]')
    
    try:
        # Identify and mark invalid polygons
        input['topo_polygon_invalid'] = input['geometry'].is_valid.map({True: 'false', False: 'true'})
        return input
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_polygon_invalid'] = f'error: {e}'
        return input

def polygon_overlap(input: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Log message with info level
    logging.info('Start processing polygon_overlap [START]')
    try:
        data_temp = input.copy()

        if 'id_ids' not in data_temp.columns:
            data_temp['id_ids'] = range(1, len(data_temp) + 1)

        # calculate the area of the intersection
        EPSG_CODE = "EPSG:32647"

        try:
            data_temp = data_temp.to_crs(EPSG_CODE)
        except Exception as e:
            # print(f'Error: {e}')
            data_temp = data_temp.set_crs("EPSG:4326", inplace=True)
            data_temp = data_temp.to_crs(EPSG_CODE, inplace=True)
        try:
            data_overlaps = gpd.overlay(data_temp, data_temp, how='intersection', keep_geom_type=False)
        except Exception as e:
            print(f'Error: {e}')
            data_temp = data_temp[data_temp.geometry.type == 'Polygon']
            data_temp.buffer(0)
            data_overlaps = gpd.overlay(data_temp, data_temp, how='intersection', keep_geom_type=False)

        # filter out the rows where the geometries are the same
        data_overlaps = data_overlaps[data_overlaps['id_ids_1'] != data_overlaps['id_ids_2']]

        # subset the rows where the id of the first geometry is less than the id of the second geometry
        data_overlaps.drop_duplicates(subset=['id_ids_1'], keep='first', inplace=True)
        
        data_overlaps = data_overlaps[data_overlaps.geometry.type != 'GeometryCollection']
        data_overlaps = data_overlaps[data_overlaps.geometry.type != 'LineString']
        data_overlaps = data_overlaps[data_overlaps.geometry.type != 'MultiLineString']
        data_overlaps = data_overlaps[data_overlaps.geometry.type != 'Point']
        data_overlaps = data_overlaps[data_overlaps.geometry.type != 'MultiPoint']

        # area of the intersection
        data_overlaps['area'] = data_overlaps.area

        # filter out the rows where the area of the intersection is less than 0.1
        data_overlaps = data_overlaps[data_overlaps['area'] > 0.1]

        # data_overlaps.to_file('data_overlaps_test.geojson', driver='GeoJSON') ## for testing

        # join data_overlaps polygon only to original data
        data_temp['topo_polygon_overlap'] = 'false'
        data_temp.loc[data_temp.id_ids.isin(data_overlaps.id_ids_1.tolist()), 'topo_polygon_overlap'] = 'true'
    
        # drop id column
        data_temp.drop(columns=['id_ids'], inplace=True)
        # print('data_temp', data_temp)

        return data_temp

    except Exception as e:
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        err = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno}"
        # Log message with error level
        print(f'Error: {err} [FAIL]')
        logging.error(f'Error: {e} [FAIL]')
        input['topo_polygon_overlap'] = f'error: {e}'
        return input

def polygon_self_intersect(input: gpd.GeoDataFrame) -> None:
    # Log message with info level
    logging.info('Start processing polygon_self_intersect [START]')
    try:
        input['topo_polygon_selfintersect'] = input.geometry.is_valid
        input['topo_polygon_selfintersect'] = ~input['topo_polygon_selfintersect']
        input['topo_polygon_selfintersect'] = input['topo_polygon_selfintersect'].astype(str).str.lower()
        return input
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error: {e} [FAIL]')
        input['topo_polygon_selfintersect'] = f'error: {e}'
        return input


def area(input: gpd.GeoDataFrame, value: float = 1.0) -> None:
    logging.info('Start processing area [START]')
    try:

        try:
            # convert crs UTM
            input.to_crs(epsg=32647, inplace=True)
        except Exception as e:
            input.set_crs("EPSG:4326", inplace=True)
            input.to_crs("EPSG:32647", inplace=True)

        # arae less than < value is 'true' else 'false'
        input['topo_area'] = input.area < value
        input['topo_area'] = input['topo_area'].map({True: 'true', False: 'false'})

        # Convert back to EPSG 4326
        input.to_crs(epsg=4326, inplace=True)
        
        return input
        
    except Exception as e:
        logging.error(f'Error in area processing: {e}')
        print(f'Error in area processing: {e}')
        input['topo_area'] = f'error: {e}'
        return input
    
def topo_bldg(mode: str, input_pwa_layer, input_bbox = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on building data.
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """

    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    _input = read_data(mode, input_pwa_layer)

    # case process area check
    try:
        area_check = area(input=_input, value=1)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error area : {e} [FAIL]')

    # case process polygon_multipart
    try:
        multipart = polygon_multipart(input=area_check)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_multipart : {e} [FAIL]')

    # case process polygon_invalid
    try:
        invalid = polygon_invalid(input=multipart)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_invalid : {e} [FAIL]')

    # case 3 process polygon duplicates
    try:
        duplicates = polygon_duplicates(input=invalid)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error point_duplicates : {e} [FAIL]')

    # case 4 process polygon out region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = polygon_out_region(input=duplicates, _overlay=_overlay)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error out_region : {e} [FAIL]')

    # case 5 process polygon_overlap
    try:
        overlap = polygon_overlap(input=out_region)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_overlap : {e} [FAIL]')

    # case 6 process polygon_self_intersect
    try:
        self_intersect = polygon_self_intersect(input=overlap)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_self_intersect : {e} [FAIL]')

    # Create result
    if self_intersect is not None:
        return self_intersect
    else:
        return None
    
def topo_pipe(mode: str, input_pwa_layer, pipe_id: str, function_id: str, input_bbox = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on pipe data.
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        pipe_id (str): The pipe id column name.
        function_id (str): The function id column name from pipe.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        pipe_id (str): The pipe id column name.
        function_id (str): The function id column name from pipe.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """

    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    _input = read_data(mode, input_pwa_layer)

    # select columns ID and geometry
    pipeidcol = pipe_id
    functionidcol = function_id

    # case 1 process line_invalid
    try:
        invalid = line_invalid(input=_input) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_invalid : {e} [FAIL]')

    # case 2 process line_multipart
    try:
        multipart = line_multipart(input=invalid) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_multipart : {e} [FAIL]')

    # case 3 process line_outregion
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        outregion = line_outregion(input=multipart, _overlay=_overlay)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_outregion : {e} [FAIL]')

    # case 4 process line_short
    try:
        short = line_short(input=outregion, distance = 0.5) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_short : {e} [FAIL]')

    # case 5 process line_duplicates
    try:
        duplicates = line_duplicates(input=short) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_duplicates : {e} [FAIL]')

    # case 6 process line_self_intersect
    try:
        self_intersect = line_self_intersect(input=duplicates) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_self_intersect : {e} [FAIL]')

    # case 7 process line_duplicate_node
    try:
        duplicate_node = line_duplicate_node(input=self_intersect) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_duplicate_node : {e} [FAIL]')

    # case 9 process line_overshoot
    try:
        overshoot = line_overshoot(input=duplicate_node) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_overshoot : {e} [FAIL]')
        
    # case 10 process line_undershoot
    try:
        undershoot = line_undershoot(input=overshoot) 

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_undershoot : {e} [FAIL]')

    # case 8 process line_nonconect
    try:
        undershoot = undershoot[undershoot[functionidcol] != 6]
        nonconect = line_nonconect(input=undershoot)
        if (undershoot[functionidcol] == 6).any():
            # There are rows where functionidcol equals 6
            undershoot_filtered = undershoot[undershoot[functionidcol] == 6]
            nonconect = pd.merge(nonconect, undershoot_filtered, on=pipeidcol, how='inner', validate='one_to_one')
        # else:
        #     # There are no rows where functionidcol equals 6
        #     print("No rows where functionidcol equals 6")

        # drop column
        nonconect = nonconect.drop(columns=[functionidcol])

    except Exception as e:
        # Log message with error level
        logging.error(f'Error line_nonconect : {e} [FAIL]')

    return nonconect

def topo_valve(mode: str, input_pwa_layer, input_pipe, valve_id: str, function_id: str, input_bbox: str = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on valve data.
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        input_pipe (str): The input file path.
        valve_id (str): The valve id column name.
        function_id (str): The function id column name from pipe.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        input_pipe: The input data frame.
        valve_id (str): The valve id column name.
        function_id (str): The function id column name from pipe.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """
    
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    _input = read_data(mode, input_pwa_layer)

    # Case 1: Process point_multipart
    try:
        multipart = point_multipart(_input)
    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates : {e} [FAIL]")

    # Case 2: Process point_duplicates
    try:
        duplicates = point_duplicates(input=multipart, column=valve_id)
    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates: {e} [FAIL]")

    # Case 3: Process point_out_region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = point_out_region(input=duplicates, _overlay=_overlay)
    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_out_region : {e} [FAIL]")

    # Case 4 and 5: Process snapping with pipes
    try:
        # Read pipe data
        _overlay = read_data(mode, input_pipe)
        try:
            _overlay = _overlay[["geometry", function_id]]
        except Exception as e:
            # Log message with error level
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
            logging.error(f"Error: {e} [FAIL]")
            logging.error(msg)
            print(msg)
            print("Data overlay has columns:", list(_overlay.columns))
            return f"No column name: {function_id}"

        # Separate pipes based on PIPE_FUNC value
        overlay_func6 = _overlay[_overlay[function_id] == 6]
        overlay_func_not6 = _overlay[_overlay[function_id] != 6]

        # Snap points with pipes where PIPE_FUNC != 6 (value = True)
        snap = point_snap(input=out_region, _overlay=overlay_func_not6, value=True)
        snap['topo_point_snap_non6'] = snap['topo_point_snap']

        # Snap points with pipes where PIPE_FUNC = 6 (value = False)
        snap2 = point_snap(input=snap, _overlay=overlay_func6, value=False)
        snap2['topo_point_snap'] = snap2.apply(
            lambda row: 'true' if row['topo_point_snap'] == 'true' or row['topo_point_snap_non6'] == 'true' else 'false', 
            axis=1
        )

        # Drop the topo_point_snap_non6 column
        snap2 = snap2.drop(columns=['topo_point_snap_non6'])

    except Exception as e:
        # Log message with error level
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
        logging.error(f"Error snapping with pipes: {e} [FAIL]")
        logging.error(msg)

    return snap2

def topo_firehydrant(mode: str, input_pwa_layer, input_pipe ,fire_id: str ,function_id: str , input_bbox = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on firehydrant data.
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        input_pipe (str): The input file path.
        fire_id (str): The valve id column name.
        function_id (str): The function id column name from pipe.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        input_pipe: The input data frame.
        fire_id (str): The valve id column name.
        function_id (str): The function id column name from pipe.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """
    
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    
    _input = read_data(mode, input_pwa_layer)

    # Case 1: Process point_multipart
    try:
        multipart = point_multipart(_input)
    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates : {e} [FAIL]")

    # Case 2: Process point_duplicates
    try:
        duplicates = point_duplicates(input=multipart, column=fire_id)
    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates: {e} [FAIL]")

    # Case 3: Process point_out_region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = point_out_region(input=duplicates, _overlay=_overlay)
    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_out_region : {e} [FAIL]")

    # Case 4 and 5: Process snapping with pipes
    try:
        # Read pipe data
        _overlay = read_data(mode, input_pipe)
        try:
            _overlay = _overlay[["geometry", function_id]]
        except Exception as e:
            # Log message with error level
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
            logging.error(f"Error: {e} [FAIL]")
            logging.error(msg)
            print(msg)
            print("Data overlay has columns:", list(_overlay.columns))
            return f"No column name: {function_id}"

        # Separate pipes based on PIPE_FUNC value
        overlay_func6 = _overlay[_overlay[function_id] == 6]
        overlay_func_not6 = _overlay[_overlay[function_id] != 6]

        # Snap points with pipes where PIPE_FUNC != 6 (value = True)
        snap = point_snap(input=out_region, _overlay=overlay_func_not6, value=True)
        snap['topo_point_snap_non6'] = snap['topo_point_snap']

        # Snap points with pipes where PIPE_FUNC = 6 (value = False)
        snap2 = point_snap(input=snap, _overlay=overlay_func6, value=False)
        snap2['topo_point_snap'] = snap2.apply(
            lambda row: 'true' if row['topo_point_snap'] == 'true' or row['topo_point_snap_non6'] == 'true' else 'false', 
            axis=1
        )

        # Drop the topo_point_snap_non6 column
        snap2 = snap2.drop(columns=['topo_point_snap_non6'])

    except Exception as e:
        # Log message with error level
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
        logging.error(f"Error snapping with pipes: {e} [FAIL]")
        logging.error(msg)
        print(msg)
        print("Data overlay has columns:", list(_overlay.columns))

    return snap2
    
def topo_meter(mode: str, input_pwa_layer, meter_id: str, input_bbox: str = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on meter data.
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """
    
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    _input = read_data(mode, input_pwa_layer)

    # Case 1: Process point_multipart
    try:
        multipart = point_multipart(_input)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates : {e} [FAIL]")

    # Case 2: Process point_duplicates
    try:
        duplicates = point_duplicates(input=multipart, column=meter_id)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates: {e} [FAIL]")

    # Case 3: Process point_out_region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = point_out_region(input=duplicates, _overlay=_overlay)

    except Exception as e:
        # Log message with error level
        exc_type, _, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        msg = f"EchoProcess job failed {e} {exc_type}, {fname}, {exc_tb.tb_lineno} [FAIL]"
        logging.error(f"Error snapping with pipes: {e} [FAIL]")
        logging.error(msg)
        print(msg)

    return out_region
    
def topo_leakpoint(mode: str, input_pwa_layer, leak_id: str, input_bbox: str = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on leakpoint data.
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        leak_id (str): The leak id column name.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        leak_id (str): The leak id column name.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """
    
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    _input = read_data(mode, input_pwa_layer)

    # Case 1: Process point_multipart
    try:
        multipart = point_multipart(_input)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates : {e} [FAIL]")

    # Case 2: Process point_duplicates
    try:
        duplicates = point_duplicates(input=multipart, column=leak_id)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates: {e} [FAIL]")

    # Case 3: Process point_out_region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = point_out_region(input=duplicates, _overlay=_overlay)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_out_region : {e} [FAIL]")

    return out_region
    
def topo_pwa_waterworks(mode: str, input_pwa_layer, pwa_id: str, input_bbox: str = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on PWA WATERWORKS data.
    
    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_pwa_layer (str): The input file path.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_pwa_layer: The input data frame.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """
    
    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    _input = read_data(mode, input_pwa_layer)

    # Case 1: Process point_multipart
    try:
        multipart = point_multipart(_input)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates : {e} [FAIL]")

    # Case 2: Process point_duplicates
    try:
        duplicates = point_duplicates(input=multipart, column=pwa_id)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_duplicates: {e} [FAIL]")

    # Case 3: Process point_out_region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = point_out_region(input=duplicates, _overlay=_overlay)

    except Exception as e:
        # Log message with error level
        logging.error(f"Error point_out_region : {e} [FAIL]")

    return out_region
    
def topo_dma_boundary(mode: str, input_pwa_layer, input_bbox = "data/province_bbox.geojson", logfile: str = "run.log"):
    """
    Perform topology checks on DMA BOUNDARY data.

    Args:
        Example: mode = 0
        mode (str): The mode of operation.
        input_file (str): The input file path.
        input_bbox (str, optional): The input bounding box file path. Defaults to "data/province_bbox.geojson".
        logfile (str, optional): The log file path. Defaults to "run.log".

        Example: mode = 1
        mode (str): The mode of operation.
        input_file: The input data frame.
        input_bbox: The input data frame.
        logfile (str, optional): The log file path. Defaults to "run.log".

    Returns:
        DataFrame: The result of the topology checks.
    """

    logging.basicConfig(filename=logfile, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    _input = read_data(mode, input_pwa_layer)

    # select columns ID and geometry
    # _input = _input[["geometry", "DMA_ID", "PWA_CODE", "DMA_NO", "DMA_NAME"]]

    # case process area check
    try:
        area_check = area(input=_input, value=1)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error area : {e} [FAIL]')

    # case process polygon_multipart
    try:
        multipart = polygon_multipart(input=area_check)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_multipart : {e} [FAIL]')

    # case process polygon_invalid
    try:
        invalid = polygon_invalid(input=multipart)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_invalid : {e} [FAIL]')

    # case 3 process polygon duplicates
    try:
        duplicates = polygon_duplicates(input=invalid)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error point_duplicates : {e} [FAIL]')

    # case 4 process polygon out region
    try:
        _overlay = read_data(mode, input_bbox)
        _overlay = _overlay[['geometry']]
        out_region = polygon_out_region(input=duplicates, _overlay=_overlay)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error out_region : {e} [FAIL]')

    # case 5 process polygon_overlap
    try:
        overlap = polygon_overlap(input=out_region)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_overlap : {e} [FAIL]')

    # case 6 process polygon_self_intersect
    try:
        self_intersect = polygon_self_intersect(input=overlap)

    except Exception as e:
        # Log message with error level
        logging.error(f'Error polygon_self_intersect : {e} [FAIL]')

    return self_intersect