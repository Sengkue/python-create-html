from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import json

app = Flask(__name__)

# File to store the list of generated files
FILES_JSON = 'files.json'

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

    # Define the file name with .html extension
    file_name_with_ext = f"{file_name}.html"

    # Define the path to the new file in the 'generated_files' directory
    file_dir = os.path.join(os.getcwd(), 'generated_files')
    os.makedirs(file_dir, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(file_dir, file_name_with_ext)

    # Write the content to the file
    try:
        with open(file_path, 'w') as file:
            file.write(html_content)

        # Update the list of created files
        if file_name_with_ext not in created_files:
            created_files.append(file_name_with_ext)
            # Save the list to a JSON file
            with open(FILES_JSON, 'w') as f:
                json.dump(created_files, f)

        # Send the URL for redirection
        return jsonify({"message": "File created successfully!", "redirect_url": f"/files/{file_name_with_ext}"})
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

# Serve the generated HTML files
@app.route('/files/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.path.join(os.getcwd(), 'generated_files'), filename)

if __name__ == '__main__':
    app.run(debug=True)
