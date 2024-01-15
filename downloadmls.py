import argparse
import requests
import json
import time
from urllib.parse import urlparse, parse_qs

def read_api_credentials(file_path):
    with open(file_path, 'r') as file:
        return file.readline().strip()

def fetch_mls_data(api_key, api_secret, last_id=0, max_retries=3, limit=500):
    url = f"https://api.simplyrets.com/properties?limit={limit}&lastId={last_id}"
    retries = 0

    while retries < max_retries:
        try:
            response = requests.get(url, auth=(api_key, api_secret))
            if response.status_code == 200:
                links = response.links
                next_link = links.get('next', {}).get('url')
                next_last_id = extract_last_id(next_link) if next_link else None
                return response.json(), next_last_id
            else:
                print(f"Failed to fetch data, status code: {response.status_code}. Retrying...")
                retries += 1
                time.sleep(2)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            retries += 1
            time.sleep(2)

    return None, None

def extract_last_id(next_link):
    if not next_link:
        return None
    parsed_url = urlparse(next_link)
    query_params = parse_qs(parsed_url.query)
    return query_params.get('lastId', [None])[0]

def format_property_to_feature(prop):
    images = prop.get("photos", [])
    listingAgent = prop.get("listingAgent", {})
    address = prop.get("address", {})
    property_details = prop.get("property", {})
    sales_data = prop.get("sales", {})
    agent_data = sales_data.get("agent", {})
    office_data = sales_data.get("office", {})

    full_address = {
        "street": address.get("full"),
        "city": address.get("city"),
        "state": address.get("state"),
        "postalCode": address.get("postalCode"),
        "country": address.get("country"),
        "prettyPrinted": f"{address.get('streetNumberText', '')} {address.get('streetName', '')}, {address.get('city', '')}, {address.get('state', '')} {address.get('postalCode', '')}"
    }

    feature = {
        "type": "Feature",
        "properties": {
            "fullAddress": full_address,
            "yearBuilt": prop.get("yearBuilt"),
            "bedrooms": property_details.get("bedrooms"),
            "mlsId": prop.get("mlsId"),
            "bathrooms": property_details.get("bathsFull", 0) + property_details.get("bathsHalf", 0) * 0.5,
            "area": property_details.get("area"),
            "featuredImage": images[0] if images else None,
            "otherImages": images[1:] if len(images) > 1 else [],
            "agentName": listingAgent.get("fullName"),
            "agentCompany": listingAgent.get("office", {}).get("name"),
            "listPrice": prop.get("listPrice"),
            "subType": property_details.get("subType"),
            "subdivision": property_details.get("subdivision"),
            "cooling": property_details.get("cooling"),
            "heating": property_details.get("heating"),
            "parking": property_details.get("parking", {}).get("spaces"),
            "flooring": property_details.get("flooring"),
            "lotSize": property_details.get("lotSize"),
            "water": property_details.get("water"),
            "view": property_details.get("view"),
            "construction": property_details.get("construction"),
            "virtualTourUrl": prop.get("virtualTourUrl"),
            "remarks": prop.get("remarks"),
            "salesAgentName": agent_data.get("fullName"),
            "salesOfficeName": office_data.get("name")
        },
        "geometry": {
            "type": "Point",
            "coordinates": [address.get("geo", {}).get("lng"), address.get("geo", {}).get("lat")]
        }
    }

    return feature

def format_to_geojson(properties):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for prop in properties:
        feature = format_property_to_feature(prop)
        geojson["features"].append(feature)

    return geojson

def save_geojson(geojson, filename):
    with open(filename, 'w') as file:
        json.dump(geojson, file, indent=4)

def process_all_properties(api_key, api_secret):
    all_properties = []
    last_id = 0
    limit = 500

    while last_id is not None:
        properties, next_last_id = fetch_mls_data(api_key, api_secret, last_id=last_id, limit=limit)
        if properties:
            all_properties.extend(properties)
            last_id = next_last_id
        else:
            break

    return all_properties

def get_args():
    parser = argparse.ArgumentParser(description="Download MLS data and save as GeoJSON.")
    parser.add_argument('--api_key_file', type=str, help='Path to file containing the API key')
    parser.add_argument('--api_secret_file', type=str, help='Path to file containing the API secret')
    return parser.parse_args()

def main():
    args = get_args()

    if args.api_key_file:
        api_key = read_api_credentials(args.api_key_file)
    else:
        api_key = input("Enter your SimplyRETS API key: ")

    if args.api_secret_file:
        api_secret = read_api_credentials(args.api_secret_file)
    else:
        api_secret = input("Enter your SimplyRETS API secret: ")

    all_properties = process_all_properties(api_key, api_secret)

    if all_properties:
        geojson = format_to_geojson(all_properties)
        save_geojson(geojson, "mls_data.geojson")
        print("GeoJSON file saved successfully.")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
