# Thailand Universal GIS Data Stack (v1.2.0)

โครงการรวบรวมและจัดหมวดหมู่ข้อมูลภูมิสารสนเทศ (GIS) ของประเทศไทยจากแหล่งข้อมูลมาตรฐานสากลและหน่วยงานภาครัฐ เพื่อสนับสนุนการพัฒนาระบบเทคโนโลยีสารสนเทศที่ต้องการความแม่นยำสูงในระดับจังหวัด, อำเภอ และตำบล

---

## โครงสร้างข้อมูล (Data Categories)

ชุดข้อมูลถูกจำแนกออกเป็น 3 รูปแบบหลัก เพื่อให้ครอบคลุมทุกวัตถุประสงค์การใช้งานในระดับมาตรฐานอุตสาหกรรม:

### 1. High-Performance Optimized (Highly Recommended)

ชุดข้อมูลที่ผ่านกระบวนการ "รีดไขมัน" (77% Reduction) เพื่อให้สามารถใช้งานบนเว็บแอปพลิเคชันได้จริงโดยไม่สูญเสียความแม่นยำทางพิกัด

* `data/geojson/web-optimized/thailand-subdistricts-optimized.json`: ระดับตำบล (339 MB - แนะนำสำหรับระดับตำบล)
* `data/geojson/web-optimized/thailand-provinces-web.json`: ระดับจังหวัด

![แผนที่ประเทศไทยระดับจังหวัด](assets/map-provinces.png)

### 2. Official Grade (Standard & Precise)

**แหล่งข้อมูลอ้างอิง:** UN OCHA (Humanitarian Data Exchange - HDX)
ข้อมูลขอบเขตการปกครองที่มีความแม่นยำสูงสุด อ้างอิงมาตรฐานรหัส P-Code สากล พร้อมข้อมูลพิกัดจุดศูนย์กลาง (Centroids)

* `data/geojson/final/provinces-final.json`: ระดับจังหวัด (77 จังหวัด)
* `data/geojson/final/districts-final.json`: ระดับอำเภอ (928 อำเภอ)
* `data/geojson/final/subdistricts-final.json`: ระดับตำบล (1.5 GB)

![แผนที่ประเทศไทยระดับตำบลความละเอียดสูง](assets/map-subdistricts.png)

### 3. Professional Shapefiles (Standard GIS)

**แหล่งข้อมูลอ้างอิง:** cvibhagool/thailand-map
ชุดข้อมูลมาตรฐานในรูปแบบ Shapefile สำหรับการใช้งานระดับมืออาชีพร่วมกับซอฟต์แวร์วิศวกรรมแผนที่ (อาทิ QGIS, ArcGIS)

* `data/shapefile/` (ประกอบด้วยไฟล์นามสกุล .shp, .dbf, .shx, .prj)

### ตารางแนะนำการใช้งาน (Use Case Selection)

| ลักษณะงาน | ชุดข้อมูลที่แนะนำ | เหตุผลประกอบ |
| :--- | :--- | :--- |
| พัฒนา Web Application / Dashboard | Web Optimized | ขนาดไฟล์เล็ก โหลดข้อมูลได้รวดเร็ว |
| การวิเคราะห์ข้อมูลเชิงสถิติหรืองานวิจัย | Official Grade | ความแม่นยำทางพิกัดสูงและอ้างอิงมาตรฐานสากล |
| งานออกแบบแผนที่ (Cartography / QGIS) | Professional Shapefiles | รองรับซอฟต์แวร์มาตรฐานวิศวกรรมแผนที่ |
| ระบบค้นหาที่อยู่และรหัสทางภูมิศาสตร์ | Official Grade | มีข้อมูล P-Code และพิกัดจุดศูนย์กลางที่ครบถ้วน |

---

## Automated Data Pipeline

โครงการนี้ประกอบด้วยระบบการจัดการข้อมูลอัตโนมัติผ่าน Python Scripts เพื่อรักษาความทันสมัยของข้อมูล:

### 1. การซิงโครไนซ์ข้อมูล (update_gis_pipeline.py)

ระบบดึงข้อมูลล่าสุดโดยตรงจาก UN OCHA API และดำเนินการจัดระเบียบโครงสร้างไฟล์โดยอัตโนมัติ

```powershell
python scripts/update_gis_pipeline.py
```

### 2. การจัดรูปแบบข้อมูลมาตรฐาน (finalize_dataset.py)

ระบบประมวลผลเพื่อแปลงข้อมูลดิบจากแหล่งสากลให้เข้ากับโครงสร้างข้อมูลมาตรฐานของโครงการ (Standardized Property Mapping)

```powershell
python scripts/finalize_dataset.py
```

### 3. Optimize (optimize_geojson.py)

ระบบประมวลผลขั้นสูงเพื่อลดขนาดไฟล์ GeoJSON (สูงสุด 77%) โดยการปรับทศนิยมพิกัดและการทำ Minification เพื่อให้ใช้งานบนเว็บได้จริง

```powershell
python scripts/optimize_geojson.py
```

---

## Utilities

### ระบบตรวจสอบคุณสมบัติข้อมูล (inspect_data.py)

ใช้สำหรับตรวจสอบโครงสร้าง Meta-data และคุณสมบัติ (Properties) เบื้องต้นของไฟล์ GeoJSON

![ตรวจสอบข้อมูลระดับจังหวัด](assets/terminal-provinces.png)

```powershell
python scripts/inspect_data.py [path_to_file]
```

### ระบบจำลองแผนที่เชิงโต้ตอบ (web_viewer.html)

ระบบพรีวิวข้อมูลสารสนเทศภูมิศาสตร์ผ่านเบราว์เซอร์โดยใช้ Leaflet.js

![พรีวิวแผนที่ระดับอำเภอ](assets/viewer-districts.png)

1. ติดตั้ง Local Server: `python -m http.server 8000`
2. เข้าชมผ่าน URL: `http://localhost:8000/scripts/web_viewer.html`

### ระบบส่งออกแผนที่เป็นรูปภาพ (export_to_image.py)

เครื่องมือสำหรับส่งออกข้อมูล GeoJSON ให้เป็นไฟล์รูปภาพ PNG คุณภาพสูง (300 DPI) เพื่อใช้ในการนำเสนอหรือทำรายงาน

![ตัวอย่างแผนที่ระดับอำเภอ](assets/map-districts.png)

```powershell
python scripts/export_to_image.py
```

---

## Property Cheat Sheet

| คุณลักษณะ (Key) | รายละเอียด | ตัวอย่างข้อมูล |
| :--- | :--- | :--- |
| `pro_th` / `pro_en` | ชื่อจังหวัด (ไทย / อังกฤษ) | พะเยา / Phayao |
| `amp_th` / `amp_en` | ชื่ออำเภอ (ไทย / อังกฤษ) | สิงหนคร / Singhanakhon |
| `tam_th` / `tam_en` | ชื่อตำบล (ไทย / อังกฤษ) | พระบรมมหาราชวัง |
| `pro_code` | รหัสมาตรฐานเขตการปกครอง (P-Code) | TH10 |
| `area_sqkm` | พื้นที่ครอบคลุม (ตารางกิโลเมตร) | 1571.37 |
| `center_lat/lon`| พิกัดภูมิศาสตร์จุดศูนย์กลาง | 13.72 / 100.60 |

---

## Credits

ขอขอบพระคุณหน่วยงานและผู้จัดทำชุดข้อมูลต้นทางเพื่อสาธารณประโยชน์:

1. [UN OCHA / HDX](https://data.humdata.org/dataset/cod-ab-tha): สำหรับข้อมูล Official COD-AB
2. [chingchai/OpenGISData-Thailand](https://github.com/chingchai/OpenGISData-Thailand): ข้อมูลระดับเขตการปกครองละเอียดสูง
3. [apisit/thailand.json](https://github.com/apisit/thailand.json): ข้อมูล GeoJSON เวอร์ชันจัดเตรียมสำหรับเว็บ
4. [cvibhagool/thailand-map](https://github.com/cvibhagool/thailand-map): ข้อมูล Shapefile มาตรฐานสากล

---

## Project Maintainer

**Nattapong Tapachoom**
อีเมล: <jonusnattapong@gmail.com>
GitHub Profile: [JonusNattapong](https://github.com/JonusNattapong)

---
*จัดสรรและพัฒนาระบบเพื่อสนับสนุนชุมชนสารสนเทศภูมิศาสตร์ไทย*
