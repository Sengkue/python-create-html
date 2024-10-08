from flask import Flask, request, render_template, jsonify, send_from_directory, redirect
import os

app = Flask(__name__)

# Route for the homepage (index)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file creation
@app.route('/create-file', methods=['POST'])
def create_file():
    data = request.get_json()
    html_content = data['content']

    # Define the path to the new file
    file_name = 'about.html'
    file_path = os.path.join(os.getcwd(), file_name)

    # Write the content to the file
    try:
        with open(file_path, 'w') as file:
            file.write(html_content)
        
        # Send the URL for redirection
        return jsonify({"message": "File created successfully!", "redirect_url": f"/files/{file_name}"})
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

# Serve the newly created HTML file
@app.route('/files/<path:filename>')
def serve_file(filename):
    # Serve the file from the root directory
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True)
