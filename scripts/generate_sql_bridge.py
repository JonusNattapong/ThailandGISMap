import json
import os
import sys

# แก้ไขปัญหา Unicode บน Windows Console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROVINCES_JSON = os.path.join(BASE_DIR, "data", "geojson", "final", "provinces-final.json")
DISTRICTS_JSON = os.path.join(BASE_DIR, "data", "geojson", "final", "districts-final.json")
OUTPUT_SQL = os.path.join(BASE_DIR, "data", "thailand_gis_update.sql")

def generate_sql():
    print("กำลังสร้างไฟล์ SQL Update เพื่อเชื่อมข้อมูล GIS เข้ากับฐานข้อมูล SQL Server ของคุณ...")
    
    sql_commands = []
    sql_commands.append("-- Thailand GIS Data Update Script")
    sql_commands.append("\n-- 1. Add columns if not exist")
    sql_commands.append("IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[province]') AND name = N'LATITUDE') ALTER TABLE [province] ADD [LATITUDE] DECIMAL(18,10), [LONGITUDE] DECIMAL(18,10), [AREA_SQKM] DECIMAL(18,2);")
    sql_commands.append("IF NOT EXISTS (SELECT * FROM sys.columns WHERE object_id = OBJECT_ID(N'[amphur]') AND name = N'LATITUDE') ALTER TABLE [amphur] ADD [LATITUDE] DECIMAL(18,10), [LONGITUDE] DECIMAL(18,10), [AREA_SQKM] DECIMAL(18,2);")
    
    if os.path.exists(PROVINCES_JSON):
        with open(PROVINCES_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        sql_commands.append("\n-- Province Updates")
        for feature in data['features']:
            p = feature['properties']
            code = p.get('pro_code', '').replace('TH', '')
            lat = p.get('center_lat')
            lon = p.get('center_lon')
            area = p.get('area_sqkm')
            if code and lat:
                sql_commands.append(f"UPDATE [province] SET [LATITUDE] = {lat}, [LONGITUDE] = {lon}, [AREA_SQKM] = {area} WHERE [PROVINCE_CODE] = '{code}';")

    if os.path.exists(DISTRICTS_JSON):
        with open(DISTRICTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        sql_commands.append("\n-- Amphur Updates")
        for feature in data['features']:
            p = feature['properties']
            code = p.get('amp_code', '').replace('TH', '')
            lat = p.get('center_lat')
            lon = p.get('center_lon')
            area = p.get('area_sqkm')
            if code and lat:
                sql_commands.append(f"UPDATE [amphur] SET [LATITUDE] = {lat}, [LONGITUDE] = {lon}, [AREA_SQKM] = {area} WHERE [AMPHUR_CODE] = '{code}';")

    with open(OUTPUT_SQL, 'w', encoding='utf-8') as f:
        f.write("\n".join(sql_commands))
    print(f"Generated {OUTPUT_SQL}")

if __name__ == "__main__":
    generate_sql()
