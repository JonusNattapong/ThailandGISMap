import json
import os
import sys

# แก้ไขปัญหา Unicode บน Windows Console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "data", "latest", "geojson")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "geojson", "final")

def process_geojson(input_file, output_file, level):
    input_path = os.path.join(INPUT_DIR, input_file)
    output_path = os.path.join(OUTPUT_DIR, output_file)

    if not os.path.exists(input_path):
        print(f"ข้าม: ไม่พบไฟล์ {input_file}")
        return

    print(f"กำลังประมวลผล: {input_file} -> {output_file}...")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for feature in data['features']:
        props = feature['properties']
        new_props = {}

        # แมพปิ้งข้อมูลพื้นฐาน
        if level == 1: # จังหวัด
            new_props['pro_th'] = props.get('adm1_name1')
            new_props['pro_en'] = props.get('adm1_name')
            new_props['pro_code'] = props.get('adm1_pcode')
        elif level == 2: # อำเภอ
            new_props['pro_th'] = props.get('adm1_name1')
            new_props['amp_th'] = props.get('adm2_name1')
            new_props['amp_en'] = props.get('adm2_name')
            new_props['amp_code'] = props.get('adm2_pcode')
        elif level == 3: # ตำบล
            new_props['pro_th'] = props.get('adm1_name1')
            new_props['amp_th'] = props.get('adm2_name1')
            new_props['tam_th'] = props.get('adm3_name1')
            new_props['tam_en'] = props.get('adm3_name')
            new_props['tam_code'] = props.get('adm3_pcode')

        # ข้อมูลเสริมที่ UN ให้มาและมีประโยชน์
        new_props['area_sqkm'] = props.get('area_sqkm')
        new_props['center_lat'] = props.get('center_lat')
        new_props['center_lon'] = props.get('center_lon')
        
        feature['properties'] = new_props

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"สำเร็จ: {output_file}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # ประมวลผลแต่ละระดับ
    process_geojson("tha_admin1.geojson", "provinces-final.json", 1)
    process_geojson("tha_admin2.geojson", "districts-final.json", 2)
    process_geojson("tha_admin3.geojson", "subdistricts-final.json", 3)

    print("\n-------------------------------------------")
    print("รวมข้อมูลและจัดรูปแบบ Final Dataset สำเร็จ!")
    print(f"เช็คผลลัพธ์ได้ที่: {OUTPUT_DIR}")
    print("-------------------------------------------")

if __name__ == "__main__":
    main()
