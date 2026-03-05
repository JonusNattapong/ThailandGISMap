#!/usr/bin/env python3
"""
Thailand GIS Export to Image Tool (Enhanced Regional Support)
สร้างภาพแผนที่จากไฟล์ GeoJSON โดยสามารถแบ่งตามภูมิภาค และเลือกระหว่างข้อมูลจังหวัดหรือตำบล

Author: Nattapong Tapachoom
Email: jonusnattapong@gmail.com
"""

import os
import sys
import argparse
import json
from datetime import datetime
from pathlib import Path

# แก้ไขปัญหา Unicode บน Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.collections import PatchCollection
    import geopandas as gpd
    from shapely.geometry import Polygon, MultiPolygon
except ImportError as e:
    print("Error: ต้องติดตั้ง dependencies ก่อน:")
    print("pip install matplotlib geopandas shapely")
    print(f"Error: {e}")
    sys.exit(1)

# ตั้งค่าฟอนต์สำหรับภาษาไทย
import matplotlib
matplotlib.rcParams['font.family'] = 'Tahoma' # หรือฟอนต์ไทยอื่นๆ ที่ติดตั้งในระบบ

# ข้อมูลการแบ่งภูมิภาคของประเทศไทย (77 จังหวัด)
THAILAND_REGIONS = {
    "ภาคเหนือ": [
        "แม่ฮ่องสอน", "เชียงใหม่", "เชียงราย", "พะเยา", "น่าน", 
        "ลำพูน", "ลำปาง", "แพร่", "อุตรดิตถ์"
    ],
    "ภาคกลาง": [
        "กรุงเทพมหานคร", "สมุทรปราการ", "นนทบุรี", "ปทุมธานี", "พระนครศรีอยุธยา", 
        "อ่างทอง", "ลพบุรี", "สิงห์บุรี", "ชัยนาท", "สระบุรี", "ชลบุรี", 
        "ระยอง", "จันทบุรี", "ตราด", "ฉะเชิงเทรา", "นครนายก", "ปราจีนบุรี", 
        "สระแก้ว", "ราชบุรี", "กาญจนบุรี", "สุพรรณบุรี", "นครปฐม", 
        "สมุทรสาคร", "สมุทรสงคราม", "เพชรบุรี", "ประจวบคีรีขันธ์", "นครสวรรค์", 
        "อุทัยธานี", "กำแพงเพชร", "ตาก", "สุโขทัย", "พิษณุโลก", "พิจิตร", "เพชรบูรณ์"
    ],
    "ภาคอีสาน": [
        "นครราชสีมา", "บุรีรัมย์", "สุรินทร์", "ศรีสะเกษ", "อุบลราชธานี", 
        "ยโสธร", "ชัยภูมิ", "อำนาจเจริญ", "หนองบัวลำภู", "ขอนแก่น", 
        "อุดรธานี", "เลย", "หนองคาย", "มหาสารคาม", "ร้อยเอ็ด", 
        "กาฬสินธุ์", "สกลนคร", "นครพนม", "มุกดาหาร", "บึงกาฬ"
    ],
    "ภาคใต้": [
        "นครศรีธรรมราช", "กระบี่", "พังงา", "ภูเก็ต", "สุราษฎร์ธานี", 
        "ระนอง", "ชุมพร", "สงขลา", "สตูล", "ตรัง", "พัทลุง", 
        "ปัตตานี", "ยะลา", "นราธิวาส"
    ]
}

DEFAULT_PATHS = {
    "province": "data/geojson/web-optimized/thailand-provinces-web.json",
    "district": "data/geojson/final/districts-final.json",
    "subdistrict": "data/geojson/web-optimized/thailand-subdistricts-optimized.json"
}

# เพิ่มการแมปชื่อจังหวัดที่มักเขียนผิดหรือแตกต่างกัน
PROVINCE_ALIASES = {
    "หนอง khai": "หนองคาย",
    "พัง-nga": "พังงา"
}

def filter_by_region(gdf, region_name):
    """กรองข้อมูลตามภูมิภาค"""
    if region_name not in THAILAND_REGIONS:
        return None
    
    provinces_in_region = THAILAND_REGIONS[region_name]
    
    # ตรวจสอบคอลัมน์ชื่อจังหวัดที่เป็นไปได้
    province_col = None
    for col in ['pro_th', 'p_th', 'name_th']:
        if col in gdf.columns:
            province_col = col
            break
    
    # ถ้าไม่เจอคอลัมน์ภาษาไทย ลองใช้ name (ซึ่งอาจเป็นไทยหรืออังกฤษ)
    if province_col is None and 'name' in gdf.columns:
        province_col = 'name'
    
    if province_col is None:
        print(f"Error: ไม่พบคอลัมน์ชื่อจังหวัดในข้อมูล. คอลัมน์ที่มี: {gdf.columns.tolist()}")
        return None
    
    # กรองข้อมูล
    mask = gdf[province_col].isin(provinces_in_region)
    filtered_gdf = gdf[mask].copy()
    
    return filtered_gdf

def create_map_image(gdf, output_path, title="Thailand GIS Map", dpi=300):
    """สร้างภาพแผนที่จาก GeoDataFrame"""
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 16), dpi=dpi)
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#1a1a1a')
    
    # วาดข้อมูล
    gdf.plot(
        ax=ax,
        color='#00d2ff',
        edgecolor='white',
        linewidth=0.1 if len(gdf) > 500 else 0.3,
        alpha=0.5,
        antialiased=True
    )
    
    ax.set_title(title, color='white', fontsize=20, fontweight='bold', pad=15)
    ax.axis('off')
    
    # สถิติ
    info_text = f"Total Features: {len(gdf)}\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    plt.text(0.02, 0.02, info_text, transform=ax.transAxes, color='#888888', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=dpi, facecolor='#1a1a1a', bbox_inches='tight')
    plt.close()
    
    print(f"Success: {output_path}")

def main():
    parser = argparse.ArgumentParser(
        description='Thailand GIS Regional Map Exporter',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input', nargs='?', help='Path to GeoJSON (Provice/District/Subdistrict)')
    parser.add_argument('--level', '-l', choices=['province', 'district', 'subdistrict'], 
                        help='เลือกระดับข้อมูล (จะใช้พาธมาตรฐานหากไม่ระบุ input)')
    parser.add_argument('--region', '-r', choices=list(THAILAND_REGIONS.keys()) + ['all'], 
                        help='เลือกภูมิภาคที่ต้องการ export')
    parser.add_argument('--output-dir', '-d', default='exported_maps', help='โฟลเดอร์สำหรับเก็บไฟล์')
    parser.add_argument('--dpi', type=int, default=300, help='ความละเอียดภาพ')
    
    args = parser.parse_args()

    # ระบุพาธไฟล์
    file_path = args.input
    if not file_path:
        if args.level:
            file_path = DEFAULT_PATHS[args.level]
        else:
            print("❌ กรุณาระบุไฟล์ input หรือเลือก --level (province/district/subdistrict)")
            sys.exit(1)

    if not os.path.exists(file_path):
        print(f"❌ ไม่พบไฟล์ที่ {file_path}")
        sys.exit(1)

    # กรองข้อมูล
    print(f"Loading data from: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        gdf = gpd.GeoDataFrame.from_features(data['features'])
    except Exception as e:
        print(f"❌ โหลดข้อมูลล้มเหลว: {e}")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    level_name = args.level or Path(file_path).stem

    # จัดการการ Export
    target_regions = []
    if args.region == 'all':
        target_regions = list(THAILAND_REGIONS.keys())
    elif args.region:
        target_regions = [args.region]
    else:
        # Export ทั้งประเทศไทย
        out_path = os.path.join(args.output_dir, f"thailand_{level_name}_full.png")
        create_map_image(gdf, out_path, f"Thailand {level_name.capitalize()} Map", args.dpi)
        return

    for reg in target_regions:
        print(f"📍 กำลังสร้างแผนที่ {reg} ({level_name})...")
        filtered_gdf = filter_by_region(gdf, reg)
        
        if filtered_gdf is not None and not filtered_gdf.empty:
            out_path = os.path.join(args.output_dir, f"{reg}_{level_name}.png")
            create_map_image(filtered_gdf, out_path, f"ประเทศไทย {reg} ({level_name})", args.dpi)
        else:
            print(f"⚠️ ไม่พบข้อมูลสำหรับ {reg}")

if __name__ == "__main__":
    main()
