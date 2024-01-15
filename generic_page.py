"""
Generic Page Generator Script

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

[script:script_name param1=value1 param2=value2 ...]

- `script_name` is the name of the Python script (without .py extension) to be executed.
- `param1`, `param2`, ... are the optional parameters to pass to the script.

Each script must define a `generate_content(params)` function that accepts a dictionary of
parameters and returns a string containing HTML content.

Example:
[script:testimonial number=3]

This will execute 'testimonial.py' script in the 'scripts' subfolder, passing it the parameter
'number' with a value of '3'. The script is expected to return HTML content for 3 testimonials.

External Scripts:
Scripts placed in the 'scripts' subfolder can be executed and must also define a 
`generate_content(params)` function. The current working directory for these scripts
will be set to the template directory.

The 'scripts' subfolder can contain any number of scripts, and they will be referenced
in the content files via shortcodes.

Requirements:
- Python 3.x
- Markdown module (for Markdown files conversion)

To run the script:
python generic_page_generator.py [TEMPLATE_DIR] [OUTPUT_DIR]

Where:
- [TEMPLATE_DIR] is the directory containing the 'pages', 'scripts', and master template.
- [OUTPUT_DIR] is the directory where the generated HTML files will be saved.
"""
"""
Inline Scripts:
To create and use an inline script within an HTML or Markdown file, embed Python code within
a specific tag that the script will recognize and process. The tag should specify that it contains
inline Python code and will be executed when generating the page.

The inline script should be encapsulated in a block that is clearly marked to avoid confusion with
regular content. The output of the script will replace the script block in the final HTML.

Example of an inline script block in an HTML file:

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
"""
import os
import markdown
import json
import datetime
import re
from string import Template
import importlib.util
import sys
from io import StringIO
import contextlib

# Function to execute external script with parameters
def execute_external_script(script_name, params, template_dir):
    # Save the current working directory
    original_cwd = os.getcwd()

    # Change to the template directory
    os.chdir(template_dir)

    try:
        # Create a full path to the script
        script_path = os.path.join('scripts', script_name + '.py')

        if not os.path.isfile(script_path):
            raise FileNotFoundError(f"Script {script_name} not found in scripts directory.")

        # Load and execute the script as a module
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        script_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script_module)

        # Execute the 'generate_content' function from the script, if it exists
        if hasattr(script_module, 'generate_content'):
            result = script_module.generate_content(params)
        else:
            raise AttributeError(f"Script {script_name} does not have a 'generate_content' function.")
    finally:
        # Change back to the original working directory
        os.chdir(original_cwd)

    return result


# Function to find and process shortcode-like placeholders
def process_shortcodes(content, template_dir):
    # Regular expression to find shortcodes
    shortcode_pattern = re.compile(r'\[script:(\w+)(?:\s+([^\]]+))?\]')
    
    # Function to replace shortcode with script output
    def replace_shortcode(match):
        script_name = match.group(1)
        params = match.group(2)
        
        # Convert params string to a dictionary
        params_dict = {}
        if params:
            params_list = params.split(',')
            for param in params_list:
                key, value = param.split('=')
                params_dict[key.strip()] = value.strip()

        return execute_external_script(script_name, params_dict, template_dir)

    return re.sub(shortcode_pattern, replace_shortcode, content)

# Function to execute inline Python script
def execute_inline_script(script_code):
    # Capture the output of the script
    with StringIO() as buf, contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        # Execute the script in the default global and local scope
        exec(script_code, globals(), locals())
        return buf.getvalue()


# Function to find and process inline Python scripts
def process_inline_scripts(content):
    # Regular expression to find inline Python scripts
    inline_script_pattern = re.compile(r'<!--python(.*?)python-->', re.DOTALL)
    
    # Function to replace script block with its output
    def replace_script_block(match):
        script_code = match.group(1)
        return execute_inline_script(script_code)

    return re.sub(inline_script_pattern, replace_script_block, content)

def convert_markdown_to_html(markdown_text):
    return markdown.markdown(markdown_text)

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def process_files(template_dir, output_dir):
    pages_dir = os.path.join(template_dir, 'pages')
    master_template_path = os.path.join(template_dir, 'filled_master_template.html')
    master_template_content = read_file(master_template_path)
    master_template = Template(master_template_content)

    for file_name in os.listdir(pages_dir):
        try:
            file_path = os.path.join(pages_dir, file_name)
            file_content = read_file(file_path)

            # Process any inline scripts in the content
            file_content = process_inline_scripts(file_content)

            # Process any shortcodes in the content
            file_content = process_shortcodes(file_content, template_dir)

            # Convert Markdown to HTML if necessary
            if file_name.endswith('.md'):
                file_content = convert_markdown_to_html(file_content)
                output_file_name = file_name.replace('.md', '.html')
            elif file_name.endswith('.html'):
                output_file_name = file_name
            else:
                continue  # Skip non-Markdown/HTML files

            final_content = master_template.substitute(content=file_content)
            output_path = os.path.join(output_dir, output_file_name)
            write_file(output_path, final_content)

            print(f"Processed {file_name} into {output_file_name}")
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generic_page_generator.py [TEMPLATE_DIR] [OUTPUT_DIR]")
    else:
        template_dir = sys.argv[1]
        output_dir = sys.argv[2]
        process_files(template_dir, output_dir)
