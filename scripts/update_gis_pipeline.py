import os
import json
import urllib.request
import ssl
import sys
import zipfile
import io

# แก้ไขปัญหา Unicode บน Windows Console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# ปิดการตรวจสอบ SSL ชั่วคราว
ssl._create_default_https_context = ssl._create_unverified_context

HDX_DATASET_ID = "cod-ab-tha"
HDX_API_URL = f"https://data.humdata.org/api/3/action/package_show?id={HDX_DATASET_ID}"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "latest", "geojson")

def download_and_extract_zip(url, target_dir):
    print(f"กำลังดาวน์โหลดและแตกไฟล์จาก: {url}...")
    try:
        with urllib.request.urlopen(url) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as z:
                # กรองเอาเฉพาะไฟล์ GeoJSON
                for file_info in z.infolist():
                    if file_info.filename.lower().endswith(".geojson"):
                        # เปลี่ยนชื่อให้สื่อความหมาย
                        new_name = file_info.filename.lower()
                        if "adm1" in new_name:
                            new_name = "thailand-provinces-official.geojson"
                        elif "adm2" in new_name:
                            new_name = "thailand-districts-official.geojson"
                        elif "adm3" in new_name:
                            new_name = "thailand-subdistricts-official.geojson"
                        
                        # บันทึกไฟล์
                        file_info.filename = new_name
                        z.extract(file_info, target_dir)
                        print(f" - แตกไฟล์สำเร็จ: {new_name}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการแตกไฟล์: {e}")

def fetch_latest_metadata():
    print("กำลังเรียกดูข้อมูลล่าสุดจาก HDX (UN OCHA)...")
    try:
        with urllib.request.urlopen(HDX_API_URL) as response:
            data = json.loads(response.read().decode())
            if data["success"]:
                return data["result"]["resources"]
            else:
                return None
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        return None

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    resources = fetch_latest_metadata()
    if not resources:
        return

    for res in resources:
        name = res["name"].lower()
        url = res["url"]
        
        # ค้นหาไฟล์ Zip ที่รวม GeoJSON
        if "geojson" in name and url.endswith(".zip"):
            download_and_extract_zip(url, OUTPUT_DIR)
            break

    print("\n-------------------------------------------")
    print("อัปเดตข้อมูล Pipeline (Zip) สำเร็จ!")
    print(f"ตรวจสอบไฟล์ได้ที่: {OUTPUT_DIR}")
    print("-------------------------------------------")

if __name__ == "__main__":
    main()
