# Running and Requirements

## Requirements

Requirements:
- Python 3.x
- Markdown module (for Markdown files conversion)
- `geopy` library for geographical computations.

An example of a list of commands that can be used to do all of the steps of building a site, except for downloading MLS data is as follows. For MLS downloading see the later parts of this documentation.

# Template HTML Files

A default template can be found in the `template` folder of this repository. The template contains all content that is individual to the theme used and the site being built. 

A sample of a fully built website can be found in the `dummyweb` folder. 

`master_template.html` -- This HTML file contains the site-wide template, including things like headers, the main menu, the footer, and similar. 

`map_template.html` -- This HTML template contains an interactive map and a filter section for property listings. Users can filter properties based on price, bedrooms, bathrooms, and type, with results displayed on the map and in a listing container. The template uses Leaflet.js for map functionality, adjusts layout responsively for different screen sizes, and includes custom styling for a user-friendly interface.

`listing_template.html` -- This HTML template is used to generate individual listings. 

`listing_page_template.html`  -- This HTML template is used to build out pages that contains a large number of listings, in particular, the pages showing all listings. 

`listing_content_template.html` -- This HTML template is for an individual listing page that contains all of the details about a listing. 

`scripts` folder -- this contains the scripts that define shortcodes 

# Page Generator Scripts

The page generator scripts can be found at the root folder of this repository.

## MLS Data Downloader Script

This Python script is designed to download real estate listing data from the SimplyRETS API and convert it into a GeoJSON format.

- **Functionality**: Fetches property listings data using API credentials, formats the data into a GeoJSON structure, and saves it as a file.
- **Output**: A `mls_data.geojson` file containing the formatted property listings.

#### Technical Details

1. **Data Retrieval and Processing**:
   - Fetches data from SimplyRETS API using provided API key and secret.
   - Handles pagination in API responses to retrieve all available listings.
   - Converts each property listing into a GeoJSON feature.

2. **Execution**:
   - Run the script via the command line, optionally specifying paths to files containing the API key and secret.

3. **Key Functions**:
   - `fetch_mls_data()`: Retrieves property listings from the API.
   - `format_property_to_feature()`: Transforms a property listing into a GeoJSON feature.
   - `format_to_geojson()`: Compiles all features into a GeoJSON feature collection.
   - `save_geojson()`: Saves the GeoJSON data to a file.

4. **Customization and Adaptability**:
   - The script can be modified to handle different API structures or additional data fields.

#### Sample Command
```bash
python download_mls.py --api_key_file /path_to_api_key_file --api_secret_file /path_to_api_secret_file
```
- `/path_to_api_key_file` and `/path_to_api_secret_file` should be the paths to the files containing the API key and secret, respectively.

## Real Estate Mock Listings Data Generation Script

This Python script is crafted for generating mock real estate listing data, particularly useful for testing and development purposes. It creates a large number of simulated property listings with random attributes, formatted as a GeoJSON file. 

- **Functionality**: Produces a customizable number of mock real estate listings with random characteristics like location, images, agent details, and property specifics.
- **Output**: A `mock_listings.geojson` file, containing the generated listings in GeoJSON format.

###

1. **Data Generation**:
   - **Coordinates**: Randomly generates geographic coordinates within a specific range.
   - **Address**: Creates random addresses.
   - **Images**: Generates URLs for a random number of images per listing.
   - **Agent and Company**: Randomly selects agent names and real estate companies from predefined lists.
   - **Property Attributes**: Randomly assigns year built, bedrooms, bathrooms, area, etc.

2. **Output**:
   - The script outputs a GeoJSON file (`mock_listings.geojson`) containing a `FeatureCollection` with each property represented as a `Feature`.

3. **Execution**:
   - Run the script via the command line. The script generates 25,000 mock listings by default.

#### Sample Usage
Run the script without any arguments:
```bash
python dummy_listing.py
```

## Master Template Filling Script

This script is designed to fill the master HTML template with site-wide constant information such as social media links, contact phone numbers, and email addresses. 

- **Functionality**: Reads data from a JSON file and injects this information into specific placeholders in the master HTML template.
- **Output**: A new HTML file (`filled_master_template.html`) that contains the updated site-wide information, ready to be used across the website.

#### Technical Details

1. **Input and Output**:
   - Input: A master HTML template and a JSON file containing the site-wide information.
   - Output: A new HTML file with the template filled with the provided data.

2. **Execution**:
   - Run the script via the command line, specifying the directory of the HTML template and the path to the JSON data file.

3. **Key Functions**:
   - `generate_top_bar_content(social_links, phone, email)`: Generates HTML content for the top bar of the site, including social media links, phone number, and email address.
   - `fill_master_template(template_dir, data_file)`: Fills the master template with the provided data and generates the updated HTML file.

4. **Customization and Adaptability**:
   - The script can be modified to accommodate different data structures in the JSON file or different template structures.

#### Sample Command
```bash
python generate_template.py /path_to_template_directory /path_to_data_file.json
```

- `/path_to_template_directory` should be the directory where the master HTML template is stored.
- `/path_to_data_file.json` is the path to the JSON file containing the site-wide data.

## Paginated Listing Pages Generator Script

This Python script is designed to create paginated HTML pages for property listings from a JSON data file. It's ideal for real estate websites that need to display numerous listings in an organized and navigable format.

### Usage
- **Functionality**: The script reads property data from a JSON file and generates HTML pages, each containing a specified number of listings. It supports different sorting options and pagination.
- **Output**: A set of HTML files for each pagination page, sorted by different criteria like most recent, highest price first, and lowest price first.

### Technical Details

1. **Input and Output**:
   - Input: A JSON file with property listings and HTML templates for individual listings and the master page layout.
   - Output: Multiple HTML files for paginated listing pages, stored in the specified output directory.

2. **Execution**:
   - Run the script via the command line, providing the template directory, output directory, and the JSON file path.

3. **Key Functions**:
   - `generate_pagination_links()`: Creates navigable pagination links for traversing between pages.
   - `generate_paginated_html()`: Generates HTML content for each paginated page, incorporating listing details and pagination links.
   - `sort_listings()`: Sorts listings based on specified criteria like price or date.

4. **Customization and Adaptability**:
   - Templates can be modified for different website designs and layouts.
   - The script can be adjusted to accommodate different JSON structures or sorting criteria.

#### Sample Command
```bash
python listing_list_page.py /path_to_template_directory /path_to_output_directory /path_to_json_file
```

- `/path_to_template_directory` is the directory where HTML templates are stored.
- `/path_to_output_directory` is where the generated HTML files will be saved.
- `/path_to_json_file` is the path to the JSON file containing the property listings.

## Property Listings HTML Generator Script

#### Overview
This Python script is crafted to automate the generation of individual HTML pages for property listings, utilizing provided templates and data from a JSON file.

- **Functionality**: Processes a JSON file containing property data, and generates HTML pages for each listing by populating predefined templates with specific property details.
- **Output**: HTML files for each property listing, named using the property's MLS ID.

#### Technical Details

1. **Input and Output**:
   - Input: A JSON file with property listing data and HTML templates for the content and overall page structure.
   - Output: HTML files for each listing, stored in the specified output directory.

2. **Execution**:
   - Run the script via the command line, providing paths to the template directory, output directory, and the JSON file.

3. **Key Functions**:
   - `generate_image_gallery(images)`: Creates HTML for an image gallery from a list of image URLs.
   - `generate_features_section(features)`: Generates HTML for various property features (interior, exterior, financial, etc.).
   - `create_html_page(feature, template_dir, destination_folder)`: Produces the complete HTML page for a single listing.
   - `process_listings(template_dir, output_dir, json_file)`: Processes all listings in the JSON file and manages the creation and deletion of HTML files.

4. **Customization and Flexibility**:
   - Templates can be customized for different layouts and styles.
   - Script can be adapted to handle different data structures in the JSON file.

#### Sample Command
```bash
python listing_pages_generator.py /path_to_template_directory /path_to_output_directory /path_to_json_file
```

- `/path_to_template_directory` should be the directory where HTML templates are stored.
- `/path_to_output_directory` is where the generated HTML files will be saved.
- `/path_to_json_file` is the path to the JSON file containing property listings.

## Map Page Generator Script

This Python script is designed to generate a map page for property listings, combining a map template with a master template to produce a complete HTML file. It is especially useful for real estate websites that feature interactive maps displaying various properties.

- **Functionality**: The script integrates a specific map page template into a master HTML template, embedding dynamic content such as the current year and other custom placeholders.
- **Output**: The final output is an HTML file named `map.html`, which is saved in a specified output directory.

#### Technical Details

1. **Input**:
   - HTML template files for the map page and the master page, located in a specified directory.

2. **Execution**:
   - Run the script via the command line, specifying the directory containing the HTML templates and the directory for the output HTML file.

3. **Key Functions**:
   - `load_template(template_path)`: Reads and returns an HTML template as a Python `Template` object.
   - `create_html_page(map_template, master_template, destination_folder)`: Generates the final HTML content by substituting placeholders in the templates and writes it to a file in the destination folder.

4. **Customization**:
   - The script can be modified to include additional dynamic content in the HTML templates, making it adaptable for different map page designs.

#### Sample Command
```bash
python map_maker.py /path_to_template_directory /path_to_output_directory
```

- `/path_to_template_directory` should be replaced with the path to the directory where your HTML templates are stored.
- `/path_to_output_directory` should be replaced with the path to the directory where you want the generated `map.html` file to be saved.

## Simplified MLS Data Generation Script

This script converts the full MLS data into a smaller, simplified form with fewer data points which can be loaded in bulk by client side JS without using too much download bandwidth, even if thousands of entries are downloaded. This is used by the search page. 
- **Demo Mode**: Option to generate random coordinates for property listings, useful for demonstrations or testing without using actual location data.

#### Technical Details

1. **Input and Output**:
   - Input: A detailed GeoJSON file containing MLS data.
   - Output: A simplified GeoJSON file, significantly reduced in size.

2. **Functionality**:
   - Extracts essential property details (address, bedrooms, bathrooms, area, list price, listing photo, MLS ID) from the input data.
   - Option to replace actual geographical coordinates with random ones within a specified distance from a given origin (in demo mode).
   - Outputs a cleaner, lighter GeoJSON file optimized for web usage.

3. **Execution**:
   - Run the script via the command line, specifying the input and output file paths, and optionally enable demo mode.

#### Sample Command
```bash
python mls_convert.py /path_to_input_file.geojson /path_to_output_file.geojson --demo
```

- `/path_to_input_file.geojson` and `/path_to_output_file.geojson` should be replaced with the respective paths for the input and output files.
- The `--demo` flag is optional and generates random coordinates for the properties.


## Testimonials Page 

The script that generates the testimonials page is `testimonials.py`

`python testimonials.py /path_to_template_directory /path_to_output_directory`

This script is designed to dynamically generate a testimonials page. The script reads client testimonials from a JSON file and integrates them into an HTML template, resulting in a complete testimonials page. The final output is an HTML file named `testimonials.html` that contains all the testimonials formatted according to the website's design standards.

### Technical Details

1. Files that should be in the templates folder 
   - A JSON file (`testimonials.json`) containing the testimonials data.
   - The generic global page template.

2. **Execution**:
   - Run the script via the command line, specifying the template directory and the output directory.

3. **Functionality Breakdown**:
   - `load_template(template_path)`: Loads the HTML master template file.
   - `generate_testimonials_html(testimonials)`: Processes each testimonial from the JSON file and formats it into HTML.
   - The script substitutes the testimonials HTML into the master template using a safe substitution method.

###  Structuring the Testimonials JSON File

#### Overview
The Testimonials Page Generation Script for the real estate website requires a well-structured JSON file to function correctly. This JSON file contains the testimonials data, which the script reads and incorporates into the website's testimonials page.

#### JSON File Structure
The JSON file should be an array of testimonial objects. Each object represents a single testimonial and must contain the following key-value pairs:

1. **`name`**: The name of the client who provided the testimonial.
2. **`testimonial`**: The testimonial text.
3. **`date`**: The date when the testimonial was given or when it was added to the site.

#### Sample JSON Structure
```json
[
    {
        "name": "John Doe",
        "testimonial": "The professionalism and personalized service that we got from this real estate agency is unlike any other company. They truly care about finding you the perfect home!",
        "date": "2024-01-01"
    },
    {
        "name": "Jane Smith",
        "testimonial": "Absolutely thrilled with our new home! The agents understood our needs and were with us every step of the way. Highly recommend to everyone!",
        "date": "2024-02-15"
    }
]
```

#### Notes
- **Format**: Ensure that the file is in valid JSON format.
- **Keys**: The keys `name`, `testimonial`, and `date` must be present in each testimonial object. If any of these keys are missing, the script will use default values for `name` and `date`, and leave the `testimonial` blank if it's missing.
- **Content**:
   - The `name` should be a string containing the full name of the client.
   - The `testimonial` should be a string containing the client's feedback.
   - The `date` should be a string in the format `YYYY-MM-DD`.

## Shortcodes and Generic Page Generator Script 

The script that generates pages based on content in the `pages` subfolder of the templates folder is `generic_page.py`

To run the script:
`python generic_page_generator.py [TEMPLATE_DIR] [OUTPUT_DIR]`

This script is designed to automate the process of generating web pages for a static site.
It reads content from Markdown (.md) or HTML (.html) files located in the 'pages' subfolder
within the template directory and injects it into the placeholder of a master template.
The generated pages are written to a specified output directory.

It also supports the execution of Python scripts embedded within the content files or 
referenced as external scripts in the 'scripts' subfolder. These scripts can dynamically
generate additional HTML content which gets injected into the final pages.

Use Shortcodes:
To embed a Python script directly within an HTML or Markdown file, use the following shortcode:

`[script:script_name param1=value1 param2=value2 ...]`

- `script_name` is the name of the Python script (without .py extension) to be executed.
- `param1`, `param2`, ... are the optional parameters to pass to the script.

Each script must define a `generate_content(params)` function that accepts a dictionary of
parameters and returns a string containing HTML content.

Example:
`[script:testimonial number=3]`

This will execute 'testimonial.py' script in the 'scripts' subfolder, passing it the parameter
'number' with a value of '3'. The script is expected to return HTML content for 3 testimonials.

External Scripts:
Scripts placed in the 'scripts' subfolder can be executed and must also define a 
`generate_content(params)` function. The current working directory for these scripts
will be set to the template directory.

The 'scripts' subfolder can contain any number of scripts, and they will be referenced
in the content files via shortcodes.

Where:
- [TEMPLATE_DIR] is the directory containing the 'pages', 'scripts', and master template.
- [OUTPUT_DIR] is the directory where the generated HTML files will be saved.

As follows is an example of such a script 

```
def generate_content(params):
    name = params.get('name', 'World')
    return f"<p>Hello, {name}!</p>"
```

Inline Scripts:
To create and use an inline script within an HTML or Markdown file, embed Python code within
a specific tag that the script will recognize and process. The tag should specify that it contains
inline Python code and will be executed when generating the page.

The inline script should be encapsulated in a block that is clearly marked to avoid confusion with
regular content. The output of the script will replace the script block in the final HTML.

Example of an inline script block in an HTML file:

```
<!--python
# Inline Python script starts here
def inline_script():
    number_of_testimonials = 3  # Set the desired number of testimonials
    # ... Generate testimonials HTML ...
    return testimonials_html

# Call the inline script and capture the output
output_html = inline_script()
# Inline Python script ends here
python-->
```
The enclosed Python code will be executed, and the 'output_html' will be injected into the page
where the script block was placed.

Note:
- Inline scripts must not interfere with the structure of the HTML or Markdown.
- The output must be valid HTML content.
- The inline script tag <!--python ... python--> is only an example and should be defined 
  according to the pattern matching logic implemented in the page generator script.

Security Implications:
Be cautious when executing inline scripts, as this can pose a security risk. Only allow inline
scripts from trusted sources and ensure that they do not contain harmful code.

Inline scripts offer a powerful way to inject dynamic content into pages, but they should be used
responsibly and with a clear understanding of the implications.
