import json

def generate_content(feedme):
    # Read and parse the data.json file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # CSS to be included in the style tag
    css_content = """
    <style>
    .custom-agents-section {
        padding: 20px;
        background-color: #f5f5f5;
    }
    .custom-agents-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        justify-content: center; /* Updated to center to fix spacing on the right */
    }
    .custom-agent-item {
        background-color: #ffffff;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 5px;
        text-align: center;
        box-sizing: border-box; /* Ensures padding is included in width */
        width: calc(33.333% - 20px); /* Updated to use width with calc for responsiveness */
        margin-bottom: 20px; /* Added bottom margin for spacing between rows */
    }
    .custom-agent-item img {
        max-width: 100%;
        height: auto;
        border-radius: 50%;
    }
    .custom-agent-content {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .custom-agent-title, .custom-agent-contact, .custom-agent-license {
        font-weight: bold;
        color: #333;
    }
    .custom-agent-bio {
        font-size: 14px;
        color: #666;
    }
    .custom-agent-contact a {
        color: #0066cc;
        text-decoration: none;
    }
    .custom-agent-contact a:hover {
        text-decoration: underline;
    }
    /* Media query for smaller screens */
    @media (max-width: 967px) {
        .custom-agent-item {
            width: calc(50% - 20px); /* Adjust to 50% for 2 columns */
        }
    }
    /* Media query for even smaller screens */
    @media (max-width: 680px) {
        .custom-agent-item {
            width: 100%; /* Full width for single column layout */
        }
    }
    </style>
    """

    # Generate HTML for each agent
    html_output = '<section class="custom-agents-section">\n'
    html_output += '<div class="custom-agents-grid">\n'
    for agent in data["agents"]:
        html_output += f'  <div class="custom-agent-item">\n'
        html_output += f'    <img src="{agent["profile_photo_url"]}" alt="{agent["name"]}">\n<br>'
        html_output += f'    <div class="custom-agent-content">\n'
        html_output += f'      <h3>{agent["name"]}</h3>\n'
        html_output += f'      <p class="custom-agent-title">{agent["title"]}</p>\n'
        html_output += f'      <p class="custom-agent-license">License: {agent["license_number"]}</p>\n'
        html_output += f'      <p class="custom-agent-bio">{agent["bio"]}</p>\n'
        html_output += f'      <p class="custom-agent-contact"><a href="tel:{agent["phone"]}">Phone: {agent["phone"]}</a></p>\n'
        html_output += f'      <p class="custom-agent-contact"><a href="mailto:{agent["email"]}">Email: {agent["email"]}</a></p>\n'
        html_output += '    </div>\n'
        html_output += '  </div>\n'
    html_output += '</div>\n'
    html_output += '</section>'

    return css_content + html_output
