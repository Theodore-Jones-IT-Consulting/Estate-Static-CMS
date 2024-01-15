import json

def generate_content(params):
    num_testimonials = int(params.get('number', 3))  # Default to 3 testimonials if not specified

    # Read and parse the JSON file
    with open('testimonials.json', 'r') as file:
        testimonials = json.load(file)

    # Generate HTML for each testimonial
    html_output = '<section class="testimonials">\n<h2>Client Testimonials</h2>\n<div class="testimonials-grid">\n'
    for testimonial in testimonials[:num_testimonials]:
        html_output += f'<blockquote class="testimonial">\n<p>"{testimonial["testimonial"]}"</p>\n'
        html_output += f'<cite>– {testimonial["name"]}</cite>\n</blockquote>\n'
    html_output += '</div>\n</section>'

    return html_output
