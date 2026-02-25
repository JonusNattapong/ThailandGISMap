import json
import os
import sys

# บังคับให้ใช้ UTF-8 สำหรับการ Print บน Windows
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def inspect_geojson(file_path):
    if not os.path.exists(file_path):
        print(f"Error: ไม่พบไฟล์ที่ {file_path}")
        return

    print(f"Inspecting: {os.path.basename(file_path)}")
    print("-" * 50)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if data.get('type') != 'FeatureCollection':
            print("Not a standard GeoJSON FeatureCollection.")
            return

        features = data.get('features', [])
        total_features = len(features)
        print(f"Total Features: {total_features:,}")

        if total_features > 0:
            sample_props = features[0].get('properties', {})
            print(f"Property Keys:")
            for key in sample_props.keys():
                print(f"   - {key}")
            
            print("\nSample Data (First Feature):")
            print(json.dumps(sample_props, indent=4, ensure_ascii=False))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    default_file = "data/geojson/high-res/thailand-provinces-detailed.geojson"
    target = sys.argv[1] if len(sys.argv) > 1 else default_file
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    full_path = os.path.join(project_root, target)
    
    inspect_geojson(full_path)
