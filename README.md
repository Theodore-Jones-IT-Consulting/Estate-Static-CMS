# Running and Requirements

## Requirements

Requirements:
- Python 3.x
- Markdown module (for Markdown files conversion)
- `geopy` library for geographical computations.

# Page Generator Scripts

The page generator scripts can be found at the root folder of this repository 

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
python path_to_script.py /path_to_template_directory /path_to_output_directory
```

- Replace `path_to_script.py` with the actual path to the script file.
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
python path_to_script.py /path_to_input_file.geojson /path_to_output_file.geojson --demo
```

- Replace `path_to_script.py` with the actual script path.
- `/path_to_input_file.geojson` and `/path_to_output_file.geojson` should be replaced with the respective paths for the input and output files.
- The `--demo` flag is optional and generates random coordinates for the properties.


## Testimonials Page 

The script that generates the testimonials page is `testimonials.py`

`python path_to_script.py /path_to_template_directory /path_to_output_directory`

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

Usage:
This script is designed to automate the process of generating web pages for a static site.
It reads content from Markdown (.md) or HTML (.html) files located in the 'pages' subfolder
within the template directory and injects it into the placeholder of a master template.
The generated pages are written to a specified output directory.

It also supports the execution of Python scripts embedded within the content files or 
referenced as external scripts in the 'scripts' subfolder. These scripts can dynamically
generate additional HTML content which gets injected into the final pages.

Embedded Scripts:
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
