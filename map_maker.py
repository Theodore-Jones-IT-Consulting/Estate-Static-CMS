import json
import argparse
import os
from datetime import datetime
from string import Template

def load_template(template_path):
    with open(template_path, 'r') as file:
        return Template(file.read())

def create_html_page(map_template, master_template, destination_folder):
    # Load and prepare the map page content
    map_page_content = map_template.safe_substitute()

    # Inject the map page content and Leaflet resources into the master template
    html_content = master_template.safe_substitute(
        content=map_page_content,
        current_year=datetime.now().year
    )

    # Write the final HTML to a file
    file_path = os.path.join(destination_folder, "map.html")
    with open(file_path, 'w') as file:
        file.write(html_content)

def main():
    parser = argparse.ArgumentParser(description='Generate a map page with property listings.')
    parser.add_argument('template_dir', help='Directory of the HTML templates')
    parser.add_argument('output_dir', help='Directory to save the generated HTML file')
    args = parser.parse_args()

    map_template_path = os.path.join(args.template_dir, 'map_template.html')
    master_template_path = os.path.join(args.template_dir, 'filled_master_template.html')

    map_template = load_template(map_template_path)
    master_template = load_template(master_template_path)

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    create_html_page(map_template, master_template, args.output_dir)

if __name__ == '__main__':
    main()

