import geopandas as gpd
import json
import logging

def result_ndjson(input: gpd.GeoDataFrame, file: str) -> None:
    logging.info('Write data [START]')
    try:
        # ค้นหาข้อมูลที่มีค่าเท่ากับ 'true' ในคอลัมน์ที่ขึ้นต้นด้วย 'tp_'
        # selected_data = input[input.filter(regex=r'^topo_').eq(True).any(axis=1)]
        input.replace({'true': 'incorrect', 'false': '', 'error': ''}, inplace=True)
        input.to_file(file, driver='GeoJSONSeq')
        # input.to_file(file, driver='GPKG')
        logging.info('Convert data [SUCCESS]')
        return file
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error Convert data: {e} [FAIL]')
        input = 'error'
        return input

def result_json(input: gpd.GeoDataFrame) -> None:
    try:
        logging.info('Write data [START]')
        # del input['geometry']
        # ค้นหาข้อมูลที่มีค่าเท่ากับ 'true' ในคอลัมน์ที่ขึ้นต้นด้วย 'tp_'
        selected_data = input[input.filter(regex=r'^topo_').eq('true').any(axis=1)]
        selected_data.replace({'true': 'incorrect', 'false': '', 'error': ''}, inplace=True)
        # แปลงข้อมูลเป็น JSON
        json_data = selected_data.to_json()
        # แปลง JSON เป็น dictionary
        data_dict = json.loads(json_data)

        # select data key properties
        new_json_data = []
        for feature in data_dict['features']:
            new_json_data.append(feature['properties'])
            # drop column
            # feature['properties'].pop('_ids')
        logging.info('Convert data [SUCCESS]')
        if new_json_data == []:
            return 'no data incorrect'
        return json.dumps(new_json_data, ensure_ascii=False).encode('utf-8')
        
    except Exception as e:
        # Log message with error level
        logging.error(f'Error Convert data: {e} [FAIL]')
        json_data = 'error'
        return json_data