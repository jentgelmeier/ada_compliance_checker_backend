import unittest
import json
from flask import Flask, jsonify, request
from app import app

# --- The Flask Application to be tested ---

# # A mock database or data store for the API
# mock_db = {
#     "items": [
#         {"id": 1, "name": "Apple"},
#         {"id": 2, "name": "Banana"}
#     ]
# }

# @app.route('/')
# def index():
#     """A simple index route for a sanity check."""
#     return "API is running!", 200

# @app.route('/api/data', methods=['GET'])
# def get_all_data():
#     """Returns all items from the mock database."""
#     return jsonify(mock_db), 200

# @app.route('/api/add', methods=['POST'])
# def add_item():
#     """Adds a new item to the mock database."""
#     if not request.is_json:
#         return jsonify({"error": "Request must be JSON"}), 400
    
#     new_item = request.get_json()
#     if 'name' not in new_item:
#         return jsonify({"error": "Missing 'name' in request body"}), 400
        
#     new_id = len(mock_db['items']) + 1
#     item = {"id": new_id, "name": new_item['name']}
#     mock_db['items'].append(item)
    
#     return jsonify({"message": "Item added successfully", "item": item}), 201

# --- The Unit Test Class ---
class TestAPIEndpoints(unittest.TestCase):
    """
    A class for unit testing the Flask API endpoints.
    """
    
    def setUp(self):
        """
        This method is run before each test method.
        It sets up a test client for the Flask app.
        """
        # Create a test client and configure the app for testing
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """Test the main index route returns a 200 status code."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_no_issues(self):
        """Test the /api/v1/html-check endpoint for string that has no issues."""
        html_string = { "html": """
                        <html lang="en">
                            <head>
                                <title>Test</title>
                            </head>
                            <body>
                                <h1>Heading</h1>
                                <h2>Heading2</h2>
                                <h3>Heading3</h3>
                                <h2>Heading2</h2>
                                <img src="src" alt="alt">
                                <a href="#">Link to recipes</a>
                                <p style="color: blue; background-color: lightgrey">text</p>
                            </body>
                        </html>
                       """}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_empty_string(self):
        """Test the /api/v1/html-check endpoint for empty string."""
        html_string = { "html": ""}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "details": "The document's primary language is not declared.",
            "element": "<html>",
            "problem": "Missing 'lang' Attribute",
            "rule": "DOC_LANG_MISSING"
        },
        {
            "details": "Every page must have a non-empty <title> tag.",
            "element": "<title>",
            "problem": "Missing Title",
            "rule": "DOC_TITLE_MISSING"
        }])
    
    def test_empty_lang_and_title(self):
        """Test the /api/v1/html-check endpoint for empty lang and title."""
        html_string = { "html": "<html lang=\"\"><title> </title></html>"}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "details": "The document's primary language is not declared.",
            "element": "<html>",
            "problem": "Missing 'lang' Attribute",
            "rule": "DOC_LANG_MISSING"
        },
        {
            "details": "Every page must have a non-empty <title> tag.",
            "element": "<title>",
            "problem": "Missing Title",
            "rule": "DOC_TITLE_MISSING"
        }])

    def test_empty_alt(self):
        """Test the /api/v1/html-check endpoint for empty img alt."""
        html_string = { "html": "<html lang=\"en\"><head><title>T</title><head><body><img><img alt=""></body></html>"}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "details": "Informative images must have a descriptive 'alt' attribute.",
            "element": "<img>",
            "problem": "Missing 'alt' Text",
            "rule": "IMG_ALT_MISSING"
        },
        {
            "details": "Informative images must have a descriptive 'alt' attribute.",
            "element": "<img alt=>",
            "problem": "Missing 'alt' Text",
            "rule": "IMG_ALT_MISSING"
        }])
        
    def test_lengthy_alt(self):
        """Test the /api/v1/html-check endpoint for alt > 120 characters."""
        html_string = { "html": """
                        <html lang="en">
                            <head>
                                <title>T</title>
                            <head>
                            <body>
                                <img alt="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa">
                            </body>
                        </html>
                       """}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "details": "The 'alt' attribute text should not exceed 120 characters.",
            "element": "<img alt=\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\">",
            "problem": "'alt' Text Too Long",
            "rule": "IMG_ALT_LENGTH"
        }])

    def test_link(self):
        """Test the /api/v1/html-check endpoint for bad link."""
        html_string = { "html": """
                        <html lang="en">
                            <head>
                                <title>T</title>
                            <head>
                            <body>
                                <a href="#">Click here</a>
                            </body>
                        </html>
                       """}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
        "details": "Link text should be descriptive. Avoid \"Click here.\"",
        "element": "<a href=\"#\">Click here</a>",
        "problem": "Generic Link Text",
        "rule": "LINK_GENERIC_TEXT"
    }])
        
    def test_mult_h1s(self):
        """Test the /api/v1/html-check endpoint for multiple h1s."""
        html_string = { "html": """
                        <html lang="en">
                            <head>
                                <title>T</title>
                            <head>
                            <body>
                                <h1>heading1</h1>
                                <h1>heading2</h2>
                            </body>
                        </html>
                       """}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "details": "Only use one <h1> per page. There are 2 in this page.",
            "element": "<h1>",
            "problem": "Multiple <h1> Tags",
            "rule": "HEADING_MULTIPLE_H1"
        }])

    def test_heading_order(self):
        """Test the /api/v1/html-check endpoint for bad heading order."""
        html_string = { "html": """
                        <html lang="en">
                            <head>
                                <title>T</title>
                            <head>
                            <body>
                                <h5>heading1</h5>
                                <h2>heading2</h2>
                                <h4>heading3</h4>
                            </body>
                        </html>
                       """}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "details": "Pages should start with <h1>. <h5> should not be used until all lower heading levels appear first.",
            "element": "<h5>",
            "problem": "Skipped Heading Level",
            "rule": "HEADING_ORDER"
        },
        {
            "details": "The <h2> element is followed by <h4>. The heading level(s) in between should not be skipped.",
            "element": "<h2>, <h4>",
            "problem": "Skipped Heading Level",
            "rule": "HEADING_ORDER"
        }])

    def test_contrast(self):
        """Test the /api/v1/html-check endpoint for color contrast issues."""
        html_string = { "html": """
                            <html lang="en">
                            <head>
                                <title>Test</title>
                                <style>
                                    .test {
                                        color: blue;
                                        font-size: 18.5px;
                                        font-weight: 700;
                                    }
                                    #intro {
                                        background-color: #f0f0f0;
                                    }
                                </style>
                            </head>
                            <body>
                                <div style='background-color: #f0f0f0;'>
                                    <h1>Good Contrast</h1>
                                    <p>This paragraph has good contrast on a light background.</p>
                                </div>
                                <div style='background-color: #87cefa;'>
                                    <p style='color: #6495ED; font-size: 24px'>This paragraph has poor contrast for large text.</p>
                                    <span style='color: rgb(255,0,255); font-size: 20em;'>This span also has poor contrast.</span>
                                </div>
                                <div id="intro">
                                    <p class="test">This paragraph has good contrast.</p>
                                    <span style='color: rgba(102, 111, 255, .9); font-size: 20em;' class="test">This span's font size can't be determined.</span>
                                </div>
                            </body>
                            </html>
                       """}
        response = self.app.post('/api/v1/html-check', data=json.dumps(html_string), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.data)
        self.assertEqual(data, [{
            "background_color": "rgb(135, 206, 250)",
            "details": "The contrast ratio is 1.73. The minimum required for large text is 3.0.",
            "element": "<p style=\"color: #6495ED; font-size: 24px\">This paragraph has poor contrast for large text.</p>",
            "foreground_color": "rgb(100, 149, 237)",
            "problem": "Low Contrast Ratio",
            "ratio": 1.73,
            "rule": "COLOR_CONTRAST"
        },
        {
            "background_color": "rgb(135, 206, 250)",
            "details": "The contrast ratio is 1.83. The minimum required for normal text is 4.5.",
            "element": "<span style=\"color: rgb(255,0,255); font-size: 20em;\">This span also has poor contrast.</span>",
            "foreground_color": "rgb(255, 0, 255)",
            "problem": "Low Contrast Ratio",
            "ratio": 1.83,
            "rule": "COLOR_CONTRAST"
        },
        {
            "background_color": "rgb(240, 240, 240)",
            "details": "Unable to determine font-size. The contrast ratio is 3.05. This is okay for large text (unbolded text ≥ 18 pt [~24 pixels] or bold text ≥ 14 pt [~18.66 pixels]), but the minimum required for normal text is 4.5.",
            "element": "<span class=\"test\" style=\"color: rgba(102, 111, 255, .9); font-size: 20em; font-weight: 700\">This span's font size can't be determined.</span>",
            "foreground_color": "rgb(116, 124, 253)",
            "problem": "Low Contrast Ratio",
            "ratio": 3.05,
            "rule": "COLOR_CONTRAST"
        }])

# --- Main block to run the tests ---
if __name__ == '__main__':
    unittest.main()
