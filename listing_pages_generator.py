from string import Template
import json
import argparse
import os
from datetime import datetime

def load_template(template_path):
    with open(template_path, 'r') as file:
        return Template(file.read())

def generate_image_gallery(images):
    return '\n'.join([f'<img src="{img}" alt="Image of property">' for img in images])

def generate_features_section(features):
    section_html = ''
    for category, details in features.items():
        section_html += f'<div class="{category}">\n'
        if details:  # Only add feature if value is not None or empty
            section_html += f'    <p><strong>{category}:</strong> {details}</p>\n'
        section_html += '</div>\n'
    return section_html

def create_html_page(feature, template_dir, destination_folder):
    properties = feature["properties"]
    
    # Load content and master templates
    content_template_path = os.path.join(template_dir, 'listing_content_template.html')
    master_template_path = os.path.join(template_dir, 'filled_master_template.html')
    mls_attribution_template_path = os.path.join(template_dir, 'mls-attribution.html')
    content_template = load_template(content_template_path)
    master_template = load_template(master_template_path)
    mls_attribution_template = load_template(mls_attribution_template_path)
    
    # Prepare image gallery HTML
    image_gallery_html = generate_image_gallery([properties["featuredImage"]] + properties["otherImages"])
    
    # Prepare features sections HTML
    interior_features = {
        'Bedrooms': properties.get("bedrooms"),
        'Bathrooms': properties.get("bathrooms"),
        'Area': f'{properties.get("area")} sqft' if properties.get("area") else None,
        'Flooring': properties.get("flooring"),
        'Year Built': properties.get("yearBuilt"),
        'Cooling': properties.get("cooling"),
        'Heating': properties.get("heating")
    }
    exterior_features = {
        'View': properties.get("view"),
        'Water': properties.get("water"),
        'Construction': properties.get("construction")
    }
    area_lot_features = {
        'Lot Size': str(properties.get("lotSize"))
        }
    financial_features = {
        'List Price': f'${properties.get("listPrice"):,.0f}' if properties.get("listPrice") else None,
        'Sub Type': properties.get("subType"),
        'Subdivision': properties.get("subdivision"),
        'Parking': properties.get("parking")
    }
    
    # Generate features sections HTML
    interior_features_html = generate_features_section(interior_features)
    exterior_features_html = generate_features_section(exterior_features)
    area_lot_features_html = generate_features_section(area_lot_features)
    financial_features_html = generate_features_section(financial_features)
    remarks = properties.get("remarks")

    # Load MLS attribution content
    last_updated_date = datetime.now().strftime("%Y-%m-%d")  # Format: YYYY-MM-DD
    mls_attribution_content = mls_attribution_template.safe_substitute({
        'last_updated_date': last_updated_date 
    })

    # Substitute variables in content template
    content_filled = content_template.safe_substitute({
        'remarks': remarks,
        'address': properties["fullAddress"]["prettyPrinted"],
        'listPrice': f'${properties.get("listPrice"):,.0f}' if properties.get("listPrice") else "N/A",
        'image_gallery': image_gallery_html,
        'interior_features': interior_features_html,
        'exterior_features': exterior_features_html,
        'area_lot_features': area_lot_features_html,
        'financial_features': financial_features_html,
        'mls_attribution': mls_attribution_content  # Add MLS attribution if needed
    })

    # Substitute content in master template
    final_html_content = master_template.safe_substitute({
        'content': content_filled
    })

    # Write to file
    filename = f"{destination_folder}/listing_{properties['mlsId']}.html"
    with open(filename, 'w') as file:
        file.write(final_html_content)
    
    return filename  # Return the path of the created/updated file


def process_listings(template_dir, output_dir, json_file):
    with open(json_file, 'r') as file:
        geojson = json.load(file)

    created_files = set()

    for feature in geojson["features"]:
        created_file = create_html_page(feature, template_dir, output_dir)
        created_files.add(created_file)

    # Compare with full paths of existing files
    existing_files = {os.path.join(output_dir, f) for f in os.listdir(output_dir)}

    # Delete files not in created_files
    for file_path in existing_files - created_files:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted stale file: {file_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate HTML pages for property listings.')
    parser.add_argument('template_dir', help='Directory of the HTML templates')
    parser.add_argument('output_dir', help='Directory to save the generated HTML files')
    parser.add_argument('json_file', help='Path to the JSON file containing listings')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    process_listings(args.template_dir, args.output_dir, args.json_file)

if __name__ == "__main__":
    main()