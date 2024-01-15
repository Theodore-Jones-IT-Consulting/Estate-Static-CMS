import json
import os
import argparse
from string import Template

def load_template(template_path):
    with open(template_path, 'r') as file:
        return Template(file.read())

def generate_testimonials_html(testimonials):
    testimonials_html = '<div class="testimonials-grid">'
    for testimonial in testimonials:
        name = testimonial.get('name', 'A Client')
        text = testimonial.get('testimonial', '')
        date = testimonial.get('date', '')

        testimonials_html += f'''
            <div class="testimonial">
                <p class="testimonial-text">"{text}"</p>
                <p class="testimonial-name">- {name}, {date}</p>
            </div>
        '''
    testimonials_html += '</div>'
    return testimonials_html

def main():
    parser = argparse.ArgumentParser(description='Generate a Testimonials page.')
    parser.add_argument('template_dir', help='Directory of the HTML templates')
    parser.add_argument('output_dir', help='Directory to save the generated HTML file')
    args = parser.parse_args()

    # Load the master template
    master_template_path = os.path.join(args.template_dir, 'filled_master_template.html')
    master_template = load_template(master_template_path)

    # Load testimonials data
    testimonials_path = os.path.join(args.template_dir, 'testimonials.json')
    with open(testimonials_path, 'r') as file:
        testimonials = json.load(file)

    # Generate testimonials HTML
    testimonials_html = generate_testimonials_html(testimonials)

    # Substitute the testimonials HTML into the master template
    final_content = master_template.safe_substitute(content=testimonials_html)

    # Write to output file
    output_file_path = os.path.join(args.output_dir, 'testimonials.html')
    with open(output_file_path, 'w') as file:
        file.write(final_content)

if __name__ == '__main__':
    main()
