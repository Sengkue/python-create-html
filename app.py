from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

# File to store the list of generated files
FILES_JSON = 'files.json'

# Predefined email and password
ADMIN_EMAIL = "sengkuevang@gmail.com"
ADMIN_PASSWORD = "79929556"

# Load existing files from the JSON file (if it exists)
if os.path.exists(FILES_JSON):
    with open(FILES_JSON, 'r') as f:
        created_files = json.load(f)
else:
    created_files = []

# Route for the homepage (index)
@app.route('/')
def index():
    return render_template('index.html', files=created_files)

# Route to handle file creation
@app.route('/create-file', methods=['POST'])
def create_file():
    data = request.get_json()
    file_name = data['file_name']
    html_content = data['content']

    file_name_with_ext = f"{file_name}.html"
    file_dir = os.path.join(os.getcwd(), 'generated_files')
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, file_name_with_ext)

    back_to_home_button = """
    <button onclick="window.location.href='/'" style="position: fixed; bottom: 20px; right: 20px; background-color: #333; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;">
        Back to Home
    </button>
    """

    full_html_content = f"{html_content}\n{back_to_home_button}"

    try:
        with open(file_path, 'w') as file:
            file.write(full_html_content)

        if file_name_with_ext not in created_files:
            created_files.append(file_name_with_ext)
            with open(FILES_JSON, 'w') as f:
                json.dump(created_files, f)

        return jsonify({"message": "File created successfully!", "redirect_url": f"/files/{file_name_with_ext}"})
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

# Route to delete a file
@app.route('/delete-file/<file_name>', methods=['DELETE'])
def delete_file(file_name):
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Check if the provided email and password are correct
    if email != ADMIN_EMAIL or password != ADMIN_PASSWORD:
        return jsonify({"message": "Email or password incorrect.", "success": False}), 401

    file_name_with_ext = f"{file_name}"
    file_dir = os.path.join(os.getcwd(), 'generated_files')
    file_path = os.path.join(file_dir, file_name_with_ext)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            if file_name_with_ext in created_files:
                created_files.remove(file_name_with_ext)
                with open(FILES_JSON, 'w') as f:
                    json.dump(created_files, f)
            return jsonify({"message": f"{file_name_with_ext} deleted successfully!", "success": True}), 200
        except Exception as e:
            return jsonify({"message": f"An error occurred while deleting the file: {e}", "success": False}), 500
    else:
        return jsonify({"message": f"{file_name_with_ext} not found!", "success": False}), 404

# Serve the generated HTML files
@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'generated_files'), filename)

if __name__ == '__main__':
    app.run(debug=True)
