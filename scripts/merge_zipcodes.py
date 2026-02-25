import json
import os
import re
import sys

# แก้ไขปัญหา Unicode บน Windows Console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_FILE = os.path.join(BASE_DIR, "data", "thailand_sqlserver.sql")
DISTRICTS_JSON = os.path.join(BASE_DIR, "data", "geojson", "final", "districts-final.json")
SUBDISTRICTS_JSON = os.path.join(BASE_DIR, "data", "geojson", "final", "subdistricts-final.json")

def extract_zipcodes_from_sql(sql_path):
    zipcode_map = {} # amp_code -> zipcode
    print(f"กำลังสแกนหาตัวเลขรหัสไปรษณีย์ใน {os.path.basename(sql_path)}...")
    
    # รูปแบบ: VALUES (1, '1001', N'พระนคร', '10200', 1)
    pattern = re.compile(r"VALUES\s*\(\d+,\s*N?'(\d{4})',\s*N'[^']+',\s*N?'(\d{5})'")
    
    try:
        with open(sql_path, 'r', encoding='utf-16') as f:
            content = f.read()
    except UnicodeError:
        with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

    matches = pattern.findall(content)
    for code, zip_code in matches:
        zipcode_map[f"TH{code}"] = zip_code
    
    print(f"ดึงรหัสไปรษณีย์สำเร็จ: {len(zipcode_map)} อำเภอ")
    return zipcode_map

def merge_zipcodes():
    zip_map = extract_zipcodes_from_sql(SQL_FILE)
    
    if os.path.exists(DISTRICTS_JSON):
        print(f"กำลังเพิ่มรหัสไปรษณีย์ลงใน: {os.path.basename(DISTRICTS_JSON)}")
        with open(DISTRICTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for feature in data['features']:
            code = feature['properties'].get('amp_code')
            if code in zip_map:
                feature['properties']['zipcode'] = zip_map[code]
                count += 1
        
        with open(DISTRICTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"สำเร็จ: อัปเดตไป {count} อำเภอ")

    if os.path.exists(SUBDISTRICTS_JSON):
        print(f"กำลังเพิ่มรหัสไปรษณีย์ลงใน: {os.path.basename(SUBDISTRICTS_JSON)} (ขั้นตอนนี้ใช้เวลาครู่หนึ่ง...)")
        with open(SUBDISTRICTS_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        count = 0
        for feature in data['features']:
            tam_code = feature['properties'].get('tam_code', '')
            amp_code = tam_code[:6]
            if amp_code in zip_map:
                feature['properties']['zipcode'] = zip_map[amp_code]
                count += 1
        
        with open(SUBDISTRICTS_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"สำเร็จ: อัปเดตไป {count} ตำบล")

if __name__ == "__main__":
    merge_zipcodes()
