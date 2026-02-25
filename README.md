# Thailand Universal GIS Data Stack (v1.0.0)

โครงการรวบรวมและจัดหมวดหมู่ข้อมูลภูมิสารสนเทศ (GIS) ของประเทศไทยจากแหล่งข้อมูลมาตรฐานสากลและหน่วยงานภาครัฐ เพื่อสนับสนุนการพัฒนาระบบเทคโนโลยีสารสนเทศที่ต้องการความแม่นยำสูงในระดับจังหวัด, อำเภอ และตำบล

---

## โครงสร้างข้อมูล (Data Categories)

ชุดข้อมูลถูกจำแนกออกเป็น 3 รูปแบบหลัก เพื่อให้ครอบคลุมทุกวัตถุประสงค์การใช้งานในระดับมาตรฐานอุตสาหกรรม:

### 1. Official Grade (Latest & Most Accurate)

**แหล่งข้อมูลอ้างอิง:** UN OCHA (Humanitarian Data Exchange - HDX)
ข้อมูลขอบเขตการปกครองที่มีความแม่นยำสูงสุด อ้างอิงมาตรฐานรหัส P-Code สากล พร้อมข้อมูลพิกัดจุดศูนย์กลาง (Centroids) และพื้นที่โดยละเอียด

* `data/geojson/final/provinces-final.json`: ระดับจังหวัด (77 จังหวัด)
* `data/geojson/final/districts-final.json`: ระดับอำเภอ (928 อำเภอ)
* `data/geojson/final/subdistricts-final.json`: ระดับตำบล (กว่า 7,000 ตำบล)

### 2. Web Optimized (High Performance)

**แหล่งข้อมูลอ้างอิง:** apisit/thailand.json
ข้อมูลรูปแบบ GeoJSON ที่ผ่านกระบวนการลดทอนรายละเอียดเชิงพื้นที่ (Simplification) เพื่อเพิ่มประสิทธิภาพในการโหลดข้อมูลสำหรับ Web Application และ Dashboard

* `data/geojson/web-optimized/thailand-provinces-web.json`

### 3. Professional Shapefiles (Standard GIS)

**แหล่งข้อมูลอ้างอิง:** cvibhagool/thailand-map
ชุดข้อมูลมาตรฐานในรูปแบบ Shapefile สำหรับการใช้งานระดับมืออาชีพร่วมกับซอฟต์แวร์วิศวกรรมแผนที่ (อาทิ QGIS, ArcGIS)

* `data/shapefile/` (ประกอบด้วยไฟล์นามสกุล .shp, .dbf, .shx, .prj)

---

## ระบบประมวลผลข้อมูลอัตโนมัติ (Automated Data Pipeline)

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

---

## เครื่องมือวิเคราะห์และแสดงผล (Utilities)

### ระบบตรวจสอบคุณสมบัติข้อมูล (inspect_data.py)

ใช้สำหรับตรวจสอบโครงสร้าง Meta-data และคุณสมบัติ (Properties) เบื้องต้นของไฟล์ GeoJSON

```powershell
python scripts/inspect_data.py [path_to_file]
```

### ระบบจำลองแผนที่เชิงโต้ตอบ (web_viewer.html)

ระบบพรีวิวข้อมูลสารสนเทศภูมิศาสตร์ผ่านเบราว์เซอร์โดยใช้ Leaflet.js

1. ติดตั้ง Local Server: `python -m http.server 8000`
2. เข้าชมผ่าน URL: `http://localhost:8000/scripts/web_viewer.html`

---

## ตารางอ้างอิงคุณลักษณะข้อมูล (Property Cheat Sheet)

| คุณลักษณะ (Key) | รายละเอียด | ตัวอย่างข้อมูล |
| :--- | :--- | :--- |
| `pro_th` / `pro_en` | ชื่อจังหวัด (ไทย / อังกฤษ) | พะเยา / Phayao |
| `amp_th` / `amp_en` | ชื่ออำเภอ (ไทย / อังกฤษ) | สิงหนคร / Singhanakhon |
| `tam_th` / `tam_en` | ชื่อตำบล (ไทย / อังกฤษ) | พระบรมมหาราชวัง |
| `pro_code` | รหัสมาตรฐานเขตการปกครอง (P-Code) | TH10 |
| `area_sqkm` | พื้นที่ครอบคลุม (ตารางกิโลเมตร) | 1571.37 |
| `center_lat/lon`| พิกัดภูมิศาสตร์จุดศูนย์กลาง | 13.72 / 100.60 |

---

## กิตติกรรมประกาศ (Credits)

ขอขอบพระคุณหน่วยงานและผู้จัดทำชุดข้อมูลต้นทางเพื่อสาธารณประโยชน์:

1. **UN OCHA / HDX**: สำหรับข้อมูล Official COD-AB
2. **chingchai/OpenGISData-Thailand**: ข้อมูลระดับเขตการปกครองละเอียดสูง
3. **apisit/thailand.json**: ข้อมูล GeoJSON เวอร์ชันจัดเตรียมสำหรับเว็บ
4. **cvibhagool/thailand-map**: ข้อมูล Shapefile มาตรฐานสากล

---

## ผู้จัดทำ (Project Maintainer)

**Nattapong Tapachoom**
อีเมล: <jonusnattapong@gmail.com>
GitHub Profile: [JonusNattapong](https://github.com/JonusNattapong)

---
*จัดสรรและพัฒนาระบบเพื่อสนับสนุนชุมชนสารสนเทศภูมิศาสตร์ไทย*
