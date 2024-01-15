import json
import random

def generate_random_coordinates():
    lat = random.uniform(39.8756, 40.1379)
    lon = random.uniform(-75.2803, -75.2495)
    return {"lat": lat, "lng": lon}

def generate_random_address():
    streets = ["Market St", "Broad St", "Walnut St", "Chestnut St", "South St"]
    city = "Philadelphia"
    state = "PA"
    postal_code = f"{random.randint(19100, 19199)}"
    street_number = random.randint(100, 9999)
    street_name = random.choice(streets)

    full_address = {
        "street": f"{street_number} {street_name}",
        "city": city,
        "state": state,
        "postalCode": postal_code,
        "country": "USA",
        "prettyPrinted": f"{street_number} {street_name}, {city}, {state} {postal_code}",
        "geo": generate_random_coordinates()
    }

    return full_address

def generate_random_images():
    num_images = random.randint(1, 5)
    return [f"https://example.com/image_{i}.jpg" for i in range(num_images)]

def generate_random_agent():
    first_names = ["John", "Jane", "Alice", "Bob", "Carol"]
    last_names = ["Smith", "Doe", "Johnson", "Williams", "Brown"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_random_company():
    companies = ["Philly Homes", "Liberty Realty", "Brotherly Love Estates", "Independence Properties", "Penn Real Estate"]
    return random.choice(companies)

def generate_listing(mls_id):
    images = generate_random_images()
    address = generate_random_address()

    return {
        "type": "Feature",
        "properties": {
            "fullAddress": address,
            "yearBuilt": random.randint(1900, 2021),
            "bedrooms": random.randint(1, 5),
            "mlsId": mls_id,
            "bathrooms": random.randint(1, 3) + 0.5 * random.randint(0, 1),
            "area": random.randint(500, 3500),
            "featuredImage": images[0] if images else None,
            "otherImages": images[1:] if len(images) > 1 else [],
            "agentName": generate_random_agent(),
            "agentCompany": generate_random_company()
        },
        "geometry": {
            "type": "Point",
            "coordinates": [address["geo"]["lng"], address["geo"]["lat"]]
        }
    }

def generate_test_data(num_listings):
    features = [generate_listing(mls_id) for mls_id in range(1, num_listings + 1)]
    return {"type": "FeatureCollection", "features": features}

def main():
    test_data = generate_test_data(25000)

    with open('mock_listings.geojson', 'w') as file:
        json.dump(test_data, file, indent=4)

    print("Test GeoJSON with 25,000 listings generated successfully.")

if __name__ == "__main__":
    main()
