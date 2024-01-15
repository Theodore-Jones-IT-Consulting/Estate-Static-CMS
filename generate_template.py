import json
import os
from string import Template
from datetime import datetime

def load_template(template_path):
    with open(template_path, 'r') as file:
        return Template(file.read())

def generate_top_bar_content(social_links, phone, email):
    links_html = ''
    for name, url in social_links.items():
        if url:  # Only include social media links that are provided
            links_html += f'<a href="{url}" target="_blank"><i class="fab fa-{name.lower()}"></i></a>\n'
    contact_html = ''
    if phone:
        contact_html += f'<a href="tel:{phone}"><i class="fas fa-phone"></i> {phone}</a>\n'
    if email:
        contact_html += f'<a href="mailto:{email}"><i class="fas fa-envelope"></i> {email}</a>\n'
    
    return f'{contact_html}{links_html}'

def fill_master_template(template_dir, data_file):
    master_template_path = os.path.join(template_dir, 'master_template.html')
    master_template = load_template(master_template_path)

    with open(data_file, 'r') as json_file:
        data = json.load(json_file)

    top_bar_content = generate_top_bar_content(
        social_links=data.get('social_media', {}),
        phone=data.get('phone', ''),
        email=data.get('email', '')
    )

    filled_content = master_template.safe_substitute(
        top_bar_content=top_bar_content,
        phone=data.get('phone', ''),
        email=data.get('email', ''),
        current_year=datetime.now().year
    )

    output_path = os.path.join(template_dir, 'filled_master_template.html')
    with open(output_path, 'w') as file:
        file.write(filled_content)

    print("filled_master_template.html has been created successfully.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Fill HTML template based on provided data.')
    parser.add_argument('template_dir', help='Directory of the HTML template')
    parser.add_argument('data_file', help='JSON file with data to fill the template')
    args = parser.parse_args()

    fill_master_template(args.template_dir, args.data_file)
