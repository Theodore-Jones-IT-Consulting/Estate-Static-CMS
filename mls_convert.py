import json
import random
from geopy.distance import great_circle

def generate_random_coords(origin, max_distance_km):
    """Generate random coordinates within a specified distance from the origin."""
    bearing = random.randint(0, 360)
    distance = random.uniform(0, max_distance_km)
    new_point = great_circle(kilometers=distance).destination(origin, bearing)
    return [new_point.longitude, new_point.latitude]

def process_geojson(input_file, output_file, demo_mode=False):
    """Process GeoJSON file and convert it to simplified format."""
    with open(input_file, 'r') as file:
        data = json.load(file)

    new_features = []
    origin = (31.9686, -99.9018)

    for feature in data['features']:
        properties = feature['properties']
        new_feature = {
            "type": "Feature",
            "properties": {
                "fullAddress": properties['fullAddress']['prettyPrinted'],
                "bedrooms": properties['bedrooms'],
                "bathrooms": properties['bathrooms'],
                "area": properties['area'],
                "listPrice": properties['listPrice'],
                "listingPhoto": properties['featuredImage'],
                "mlsId": properties['mlsId']
            },
            "geometry": {
                "type": "Point",
                "coordinates": generate_random_coords(origin, 5) if demo_mode else feature['geometry']['coordinates']
            }
        }
        new_features.append(new_feature)

    new_data = {
        "type": "FeatureCollection",
        "features": new_features
    }

    with open(output_file, 'w') as file:
        json.dump(new_data, file, indent=4)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert GeoJSON to a simplified format.")
    parser.add_argument("input_file", help="Path to the input GeoJSON file")
    parser.add_argument("output_file", help="Path to the output GeoJSON file")
    parser.add_argument("--demo", action="store_true", help="Enable demo mode with random coordinates")

    args = parser.parse_args()
    process_geojson(args.input_file, args.output_file, args.demo)
