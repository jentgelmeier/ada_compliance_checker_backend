from flask import Flask, jsonify, request
import re

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

# This endpoint will respond to POST requests to '/api/ada-check'.
@app.route('/api/ada-check', methods=['POST'])
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
    is_over_10_chars = len(input_string) > 10

    # Check the color contrast.
    is_over_10_chars = len(input_string) > 10

    # Check the img alt attribute.
    alt_err = check_img_alt(input_string)
    if alt_err:
        response.append(alt_err)

    # Check the img alt length.
    is_over_10_chars = len(input_string) > 10

    # Check meaningful link text.
    link_err = check_link_text(input_string)
    if link_err:
        response.extend(link_err)

    # Check that there's only one h1.
    h1_err = check_h1(input_string)
    if h1_err:
        response.append(h1_err)

    # Check the heading heirarchy.
    is_over_10_chars = len(input_string) > 10

    # Return the result as a JSON object.
    return jsonify(response), 200

def check_lang(input_string):
    html = re.search(r"<html.*?>", input_string)
    if not html or not re.search(r"lang=(""|')\w('|"")", html.group()):
        return {
            "problem": "Missing 'lang' Attribute",
            "element": "<html>",
            "details": "The document's primary language is not declared.",
            "rule": "DOC_LANG_MISSING"
        }
    return

def check_img_alt(input_string):
    count = 0
    img_tags = re.findall(r"<img.*?>", input_string)

    for img in img_tags:
        if not re.search(r"alt=(""|')\S('|"")", img):
            count+= 1
    
    if count:
        return {
                "problem": "Missing 'alt' Text",
                "element": "<img>",
                "details": "Informative images must have a descriptive 'alt' attribute.",
                "rule": "IMG_ALT_MISSING",
                "instances": count
            }
    return


def check_link_text(input_string):
    result = []
    link_matches = re.findall(r"<a href.*?>(?P<text>.*?)</a>", input_string)

    for link_text in link_matches:
        generic_text = re.search(r"click here|click this|read more|more info|^more$|^here$|^this$", link_text, re.IGNORECASE)
        if generic_text:
            result.append({
                "problem": "Generic Link Text",
                "element": "<a>",
                "details": 'Link text should be descriptive. Avoid "' + generic_text.group() + '."',
                "rule": "LINK_GENERIC_TEXT"
            })
    return result

def check_h1(input_string):
    h1_tags = re.findall(r"<h1", input_string)

    if len(h1_tags) > 1:
        return {
            "problem": "Multiple <h1> Tags",
            "element": "<h1>",
            "details": "Only use one <h1> per page. There are " + str(len(h1_tags)) + " in this page.",
            "rule": "HEADING_MULTIPLE_H1"
        }
    return

    

# This block ensures the Flask development server runs only when the script is executed directly.
if __name__ == '__main__':
    # Run the Flask application in debug mode for development.
    # In a production environment, you would use a production-ready WSGI server.
    app.run(debug=True)
