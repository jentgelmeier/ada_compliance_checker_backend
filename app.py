from flask import Flask, jsonify, request
from flask_cors import cross_origin

from ada_checks import check_h1, check_headers, check_lang, check_title, check_img_alt, check_link_text
from contrast_check import check_contrast_ratio

# Create an instance of the Flask application
# The __name__ variable helps Flask find the root path of the application
app = Flask(__name__)

# Define an API endpoint for the root URL ('/')
# This endpoint will respond to GET requests.
@app.route('/')
def home():
    """
    Handles requests to the home page.
    Returns a simple greeting message.
    """
    return "<h1>Welcome to the Flask API!</h1><p>Try /api/ada_check to check if your html meets accessibility standards.</p>"

# This endpoint will respond to POST requests to '/api/v1/ada-check'.
@app.route('/api/v1/ada-check', methods=['POST'])
@cross_origin()
def check_html_accessibility():
    """
    Receives a JSON object with an 'html' string and returns
    Expects a JSON payload like: {"html": "your string here"}.
    Returns a JSON response: [{"problem": "Low Contrast Ratio", "element": "<h1>" , "details": "The contrast ratio is 1.98. The
    minimum required for large text is 3.0.", "rule": ""COLOR_CONTRAST"}, {...}].
    """
    request_data = request.get_json()

    # Validate that the request_data is not empty and contains the 'text' key.
    if not request_data or 'html' not in request_data:
        return jsonify({"message": "Invalid request: JSON object with 'html' key required"}), 400

    # Ensure the value associated with 'text' is actually a string.
    input_string = request_data['html']
    if not isinstance(input_string, str):
        return jsonify({"message": "Invalid input: 'html' must be a string"}), 400

    response = []

    # Check the language attribute.
    lang_err = check_lang(input_string)
    if lang_err:
        response.append(lang_err)

    # Check the title.
    title_err = check_title(input_string)
    if title_err:
        response.append(title_err)

    # Check the color contrast.
    contrast_err = check_contrast_ratio(input_string)
    print('ce', contrast_err)
    if contrast_err:
        response.extend(contrast_err)

    # Check the img alt attribute and length.
    alt_err = check_img_alt(input_string)
    if alt_err:
        response.extend(alt_err)

    # Check meaningful link text.
    link_err = check_link_text(input_string)
    if link_err:
        response.extend(link_err)

    # Check that there's only one h1.
    h1_err = check_h1(input_string)
    if h1_err:
        response.append(h1_err)

    # Check the heading heirarchy.
    header_err = check_headers(input_string)
    if header_err:
        response.extend(header_err)

    # Return the result as a JSON object.
    return jsonify(response), 200

# This block ensures the Flask development server runs only when the script is executed directly.
if __name__ == '__main__':

    # Run the Flask application in debug mode for development.
    # In a production environment, you would use a production-ready WSGI server.
    app.run(debug=True)
