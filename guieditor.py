from flask import Flask, jsonify, request, send_from_directory
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
TEMPLATES_DIR = 'templates'
PAGES_DIR = os.path.join(TEMPLATES_DIR, 'pages')
BLOG_DIR = os.path.join(TEMPLATES_DIR, 'blog')
SCRIPTS_DIR = os.path.join(TEMPLATES_DIR, 'scripts')
DATA_FILE = os.path.join(TEMPLATES_DIR, 'data.json')

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def write_json_file(file_path, content):
    with open(file_path, 'w') as file:
        json.dump(content, file, indent=4)

def file_operation(directory, filename, method, content=None):
    file_path = os.path.join(directory, secure_filename(filename))
    if method == 'GET':
        if os.path.exists(file_path):
            return send_from_directory(directory, filename)
        else:
            return jsonify({"error": "File not found"}), 404
    elif method == 'PUT':
        with open(file_path, 'w') as file:
            file.write(content)
        return jsonify({"message": "File updated successfully"})
    elif method == 'DELETE':
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({"message": "File deleted successfully"})
        else:
            return jsonify({"error": "File not found"}), 404

@app.route('/site-data', methods=['GET', 'PUT'])
def site_data():
    if request.method == 'GET':
        return jsonify(read_json_file(DATA_FILE))
    elif request.method == 'PUT':
        write_json_file(DATA_FILE, request.json)
        return jsonify({"message": "Data updated successfully"})

@app.route('/pages', methods=['GET', 'POST'])
@app.route('/pages/<filename>', methods=['GET', 'PUT', 'DELETE'])
def custom_pages(filename=None):
    if request.method == 'GET':
        if filename:
            return file_operation(PAGES_DIR, filename, 'GET')
        else:
            return jsonify(os.listdir(PAGES_DIR))
    elif request.method == 'POST':
        new_file = request.files['file']
        new_file.save(os.path.join(PAGES_DIR, secure_filename(new_file.filename)))
        return jsonify({"message": "File created successfully"})
    elif request.method == 'PUT':
        return file_operation(PAGES_DIR, filename, 'PUT', request.data.decode('utf-8'))
    elif request.method == 'DELETE':
        return file_operation(PAGES_DIR, filename, 'DELETE')

@app.route('/blog-posts', methods=['GET', 'POST'])
@app.route('/blog-posts/<filename>', methods=['GET', 'PUT', 'DELETE'])
def blog_posts(filename=None):
    if request.method == 'GET':
        if filename:
            return file_operation(BLOG_DIR, filename, 'GET')
        else:
            return jsonify(os.listdir(BLOG_DIR))
    elif request.method == 'POST':
        new_file = request.files['file']
        new_file.save(os.path.join(BLOG_DIR, secure_filename(new_file.filename)))
        return jsonify({"message": "File created successfully"})
    elif request.method == 'PUT':
        return file_operation(BLOG_DIR, filename, 'PUT', request.data.decode('utf-8'))
    elif request.method == 'DELETE':
        return file_operation(BLOG_DIR, filename, 'DELETE')

@app.route('/shortcodes', methods=['GET'])
@app.route('/shortcodes/<filename>', methods=['GET', 'PUT', 'DELETE'])
def custom_shortcodes(filename=None):
    if request.method == 'GET':
        if filename:
            return file_operation(SCRIPTS_DIR, filename, 'GET')
        else:
            return jsonify(os.listdir(SCRIPTS_DIR))
    elif request.method == 'PUT':
        return file_operation(SCRIPTS_DIR, filename, 'PUT', request.data.decode('utf-8'))
    elif request.method == 'DELETE':
        return file_operation(SCRIPTS_DIR, filename, 'DELETE')

@app.route('/templates', methods=['GET'])
@app.route('/templates/<path:filepath>', methods=['GET', 'PUT', 'DELETE'])
def templates(filepath=None):
    if request.method == 'GET':
        if filepath:
            return file_operation(TEMPLATES_DIR, filepath, 'GET')
        else:
            return jsonify(os.listdir(TEMPLATES_DIR))
    elif request.method == 'PUT':
        return file_operation(TEMPLATES_DIR, filepath, 'PUT', request.data.decode('utf-8'))
    elif request.method == 'DELETE':
        return file_operation(TEMPLATES_DIR, filepath, 'DELETE')

@app.route('/pages/create', methods=['POST'])
def create_page():
    file_info = request.json
    file_name = secure_filename(file_info['name'])
    file_type = file_info['type']
    file_path = os.path.join(PAGES_DIR, f"{file_name}.{file_type}")

    if os.path.exists(file_path):
        return jsonify({"error": "File already exists"}), 409

    with open(file_path, 'w') as file:
        file.write('')  # Create an empty file

    return jsonify({"message": "File created successfully"})


if __name__ == '__main__':
    app.run(debug=True)
