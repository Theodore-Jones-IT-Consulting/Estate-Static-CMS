import json

def generate_content(params):
    num_listings = int(params.get('number', 3))  # Default to 3 listings if not specified

    # Read and parse the GeoJSON file
    with open('mls_data.geojson', 'r') as file:
        data = json.load(file)

    # Generate HTML for each listing
    html_output = '<section class="re-listings-section">\n<div class="re-listings-grid">\n'
    for feature in data["features"][:num_listings]:
        properties = feature["properties"]
        formatted_price = "{:,}".format(properties["listPrice"])
        mls_id = properties["mlsId"]
        html_output += f'<div class="re-listing-item">\n'
        html_output += f'<img src="{properties["listingPhoto"]}" alt="Listing Photo">\n'
        html_output += f'<p>{properties["fullAddress"]}</p>\n'
        html_output += f'<p>Bedrooms: {properties["bedrooms"]}, Bathrooms: {properties["bathrooms"]}, Area: {properties["area"]} sqft</p>\n'
        html_output += f'<p class="re-listing-price">Price: ${formatted_price}</p>\n'
        html_output += f'<a href="/listing/listing_{mls_id}.html">More Information</a>\n'
        html_output += '</div>\n'
    html_output += '</div>\n</section>'

    return html_output
