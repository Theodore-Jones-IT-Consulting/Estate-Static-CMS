import json
import argparse
import os
from string import Template

LISTINGS_PER_PAGE = 20

def load_template(template_path):
    with open(template_path, 'r') as file:
        return Template(file.read())

def sort_listings(listings, sort_key=None, reverse=False):
    if sort_key:
        return sorted(listings, key=lambda x: x['properties'].get(sort_key, 0), reverse=reverse)
    return listings

def generate_pagination_links(current_page, total_pages, version_name):
    links = []

    # Define how many page links to show around the current page
    num_links_around_current = 2

    for page in range(1, total_pages + 1):
        # Adjust URL for first page of "Most Recent"
        page_link = 'index.html' if page == 1 and version_name == 'Most_Recent' else f'{version_name}_page_{page}.html'

        # Always show the first and last pages
        if page == 1 or page == total_pages:
            links.append(f'<a href="{page_link}">{page}</a>')

        # Show current page and num_links_around_current pages around it
        elif page >= current_page - num_links_around_current and page <= current_page + num_links_around_current:
            if page == current_page:
                links.append(f'<span>{page}</span>')
            else:
                links.append(f'<a href="{page_link}">{page}</a>')

        # Show ellipses when there is a gap
        elif page == current_page - num_links_around_current - 1 or page == current_page + num_links_around_current + 1:
            links.append('...')

    # "Previous" and "Next" buttons
    prev_page = max(1, current_page - 1)
    next_page = min(total_pages, current_page + 1)

    prev_page_link = 'index.html' if prev_page == 1 and version_name == 'Most_Recent' else f'{version_name}_page_{prev_page}.html'
    next_page_link = f'{version_name}_page_{next_page}.html'

    prev_link = f'<a href="{prev_page_link}">&laquo; Previous</a>' if current_page > 1 else ''
    next_link = f'<a href="{next_page_link}">Next &raquo;</a>' if current_page < total_pages else ''

    return prev_link + ' ' + ' '.join(links) + ' ' + next_link

def generate_paginated_html(listings, listing_template, master_template, output_dir, version_name, generated_files):
    total_pages = (len(listings) + LISTINGS_PER_PAGE - 1) // LISTINGS_PER_PAGE

    for page in range(1, total_pages + 1):
        page_listings = listings[(page - 1) * LISTINGS_PER_PAGE : page * LISTINGS_PER_PAGE]

        content = ''
        content += '"<div class="listing-navigation"> <a href="index.html">Most Recent</a> | <a href="Highest_Price_First_page_1.html">Highest Price First</a> | <a href="Lowest_Price_First_page_1.html">Lowest Price First</a></div>'
        for listing in page_listings:
            # Flatten the properties
            flattened_props = listing['properties']
            flattened_props['fullAddressPrettyPrinted'] = flattened_props['fullAddress']['prettyPrinted']
            
            # Formatting listPrice
            if 'listPrice' in flattened_props:
                try:
                    list_price = float(flattened_props['listPrice'])
                    flattened_props['listPrice'] = f"${list_price:,.0f}"
                except ValueError:
                    flattened_props['listPrice'] = flattened_props['listPrice']
            else:
                flattened_props['listPrice'] = "N/A"

            # Handle missing data
            flattened_props = {k: v if v is not None else '' for k, v in flattened_props.items()}

            content += listing_template.safe_substitute(flattened_props) + '\n'

        # Generate pagination links for each page
        pagination_links = generate_pagination_links(page, total_pages, version_name)

        page_content = f"<div class='listing-table'>{content}</div><nav class='pagination'>{pagination_links}</nav>"

        # Generate a dynamic title for each page
        title = f"{version_name.replace('_', ' ')} Listings - Page {page}"

        # Substitute content and title in master template
        final_content = master_template.safe_substitute(content=page_content, title=title)

        # Determine file name
        file_name = 'index.html' if page == 1 and version_name == 'Most_Recent' else f'{version_name}_page_{page}.html'
        file_path = os.path.join(output_dir, file_name)
        generated_files.add(file_path)

        with open(file_path, 'w') as file:
            file.write(final_content)


def main():
    parser = argparse.ArgumentParser(description='Generate Paginated Listing Pages.')
    parser.add_argument('template_dir', help='Directory of HTML templates')
    parser.add_argument('output_dir', help='Directory for output HTML files')
    parser.add_argument('json_file', help='JSON file with listings')
    args = parser.parse_args()

    with open(args.json_file, 'r') as file:
        data = json.load(file)
        listings = data['features']  # Extract listings from features key

    listing_template = load_template(os.path.join(args.template_dir, 'listing_template.html'))
    master_template = load_template(os.path.join(args.template_dir, 'filled_master_template.html'))

    generated_files = set()
    
    # Most Recent
    generate_paginated_html(listings, listing_template, master_template, args.output_dir, 'Most_Recent', generated_files)

    # Highest Price First
    sorted_listings = sort_listings(listings, 'listPrice', True)
    generate_paginated_html(sorted_listings, listing_template, master_template, args.output_dir, 'Highest_Price_First', generated_files)

    # Lowest Price First
    sorted_listings = sort_listings(listings, 'listPrice')
    generate_paginated_html(sorted_listings, listing_template, master_template, args.output_dir, 'Lowest_Price_First', generated_files)

    # Delete files not generated by the script
    existing_files = set(os.listdir(args.output_dir))
    for file_path in existing_files - generated_files:
        if os.path.isfile(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    main()
