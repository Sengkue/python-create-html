from flask import Flask, request, render_template, jsonify
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
    file_path = os.path.join(os.getcwd(), 'about.html')

    # Write the content to the file
    try:
        with open(file_path, 'w') as file:
            file.write(html_content)
        return jsonify({"message": "File 'about.html' created successfully!"})
    except Exception as e:
        return jsonify({"message": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    # Set debug=True for development purposes
    app.run(debug=True)
