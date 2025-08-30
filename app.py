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

# This endpoint will respond to POST requests to '/api/v1/ada-check'.
@app.route('/api/v1/ada-check', methods=['POST'])
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
    contrast_err = check_contrast(input_string)
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

def check_title(input_string):
    title = re.search(r"<title>\S*?</title>", input_string)
    if not title:
        return {
            "problem": "Missing Title",
            "element": "<title>",
            "details": "Every page must have a non-empty <title> tag.",
            "rule": "DOC_TITLE_MISSING"
        }
    return

def check_contrast(input_string):
    default_bg = "#FFFFFF"
    default_color = "#000000"
    default_ratio = "21:1"

    colors = re.findall(r"color", input_string)
    return

def alias_to_rgb(alias):
     
    alias_dict = {
        "aliceblue": [240, 248, 255],
        "antiquewhite": [250, 235, 215],
        "aqua": [0, 255, 255],
        "aquamarine": [127, 255, 212],
        "azure": [240, 255, 255],
        "beige": [245, 245, 220],
        "bisque": [255, 228, 196],
        "black": [0, 0, 0],
        "blanchedalmond": [255, 235, 205],
        "blue": [0, 0, 255],
        "blueviolet": [138, 43, 226],
        "brown": [165, 42, 42],
        "burlywood": [222, 184, 135],
        "cadetblue": [95, 158, 160],
        "chartreuse": [127, 255, 0],
        "chocolate": [210, 105, 30],
        "coral": [255, 127, 80],
        "cornflowerblue": [100, 149, 237],
        "cornsilk": [255, 248, 220],
        "crimson": [220, 20, 60],
        "cyan": [0, 255, 255],
        "darkblue": [0, 0, 139],
        "darkcyan": [0, 139, 139],
        "darkgoldenrod": [184, 134, 11],
        "darkgray": [169, 169, 169],
        "darkgreen": [0, 100, 0],
        "darkgrey": [169, 169, 169],
        "darkkhaki": [189, 183, 107],
        "darkmagenta": [139, 0, 139],
        "darkolivegreen": [85, 107, 47],
        "darkorange": [255, 140, 0],
        "darkorchid": [153, 50, 204],
        "darkred": [139, 0, 0],
        "darksalmon": [233, 150, 122],
        "darkseagreen": [143, 188, 143],
        "darkslateblue": [72, 61, 139],
        "darkslategray": [47, 79, 79],
        "darkslategrey": [47, 79, 79],
        "darkturquoise": [0, 206, 209],
        "darkviolet": [148, 0, 211],
        "deeppink": [255, 20, 147],
        "deepskyblue": [0, 191, 255],
        "dimgray": [105, 105, 105],
        "dimgrey": [105, 105, 105],
        "dodgerblue": [30, 144, 255],
        "firebrick": [178, 34, 34],
        "floralwhite": [255, 250, 240],
        "forestgreen": [34, 139, 34],
        "fuchsia": [255, 0, 255],
        "gainsboro": [220, 220, 220],
        "ghostwhite": [248, 248, 255],
        "gold": [255, 215, 0],
        "goldenrod": [218, 165, 32],
        "gray": [128, 128, 128],
        "green": [0, 128, 0],
        "greenyellow": [173, 255, 47],
        "grey": [128, 128, 128],
        "honeydew": [240, 255, 240],
        "hotpink": [255, 105, 180],
        "indianred": [205, 92, 92],
        "indigo": [75, 0, 130],
        "ivory": [255, 255, 240],
        "khaki": [240, 230, 140],
        "lavender": [230, 230, 250],
        "lavenderblush": [255, 240, 245],
        "lawngreen": [124, 252, 0],
        "lemonchiffon": [255, 250, 205],
        "lightblue": [173, 216, 230],
        "lightcoral": [240, 128, 128],
        "lightcyan": [224, 255, 255],
        "lightgoldenrodyellow": [250, 250, 210],
        "lightgray": [211, 211, 211],
        "lightgreen": [144, 238, 144],
        "lightgrey": [211, 211, 211],
        "lightpink": [255, 182, 193],
        "lightsalmon": [255, 160, 122],
        "lightseagreen": [32, 178, 170],
        "lightskyblue": [135, 206, 250],
        "lightslategray": [119, 136, 153],
        "lightslategrey": [119, 136, 153],
        "lightsteelblue": [176, 196, 222],
        "lightyellow": [255, 255, 224],
        "lime": [0, 255, 0],
        "limegreen": [50, 205, 50],
        "linen": [250, 240, 230],
        "magenta": [255, 0, 255],
        "maroon": [128, 0, 0],
        "mediumaquamarine": [102, 205, 170],
        "mediumblue": [0, 0, 205],
        "mediumorchid": [186, 85, 211],
        "mediumpurple": [147, 112, 219],
        "mediumseagreen": [60, 179, 113],
        "mediumslateblue": [123, 104, 238],
        "mediumspringgreen": [0, 250, 154],
        "mediumturquoise": [72, 209, 204],
        "mediumvioletred": [199, 21, 133],
        "midnightblue": [25, 25, 112],
        "mintcream": [245, 255, 250],
        "mistyrose": [255, 228, 225],
        "moccasin": [255, 228, 181],
        "navajowhite": [255, 222, 173],
        "navy": [0, 0, 128],
        "oldlace": [253, 245, 230],
        "olive": [128, 128, 0],
        "olivedrab": [107, 142, 35],
        "orange": [255, 165, 0],
        "orangered": [255, 69, 0],
        "orchid": [218, 112, 214],
        "palegoldenrod": [238, 232, 170],
        "palegreen": [152, 251, 152],
        "paleturquoise": [175, 238, 238],
        "palevioletred": [219, 112, 147],
        "papayawhip": [255, 239, 213],
        "peachpuff": [255, 218, 185],
        "peru": [205, 133, 63],
        "pink": [255, 192, 203],
        "plum": [221, 160, 221],
        "powderblue": [176, 224, 230],
        "purple": [128, 0, 128],
        "rebeccapurple": [102, 51, 153],
        "red": [255, 0, 0],
        "rosybrown": [188, 143, 143],
        "royalblue": [65, 105, 225],
        "saddlebrown": [139, 69, 19],
        "salmon": [250, 128, 114],
        "sandybrown": [244, 164, 96],
        "seagreen": [46, 139, 87],
        "seashell": [255, 245, 238],
        "sienna": [160, 82, 45],
        "silver": [192, 192, 192],
        "skyblue": [135, 206, 235],
        "slateblue": [106, 90, 205],
        "slategray": [112, 128, 144],
        "slategrey": [112, 128, 144],
        "snow": [255, 250, 250],
        "springgreen": [0, 255, 127],
        "steelblue": [70, 130, 180],
        "tan": [210, 180, 140],
        "teal": [0, 128, 128],
        "thistle": [216, 191, 216],
        "tomato": [255, 99, 71],
        "turquoise": [64, 224, 208],
        "violet": [238, 130, 238],
        "wheat": [245, 222, 179],
        "white": [255, 255, 255],
        "whitesmoke": [245, 245, 245],
        "yellow": [255, 255, 0],
        "yellowgreen": [154, 205, 50]
    }

    return alias_dict[alias]

def hex_to_rgba(hex_color):
    hex_color = hex_color.lstrip('#')
    
    if not re.fullmatch(r'^[0-9a-f]{6}$|^[0-9a-f]{8}$', hex_color, re.IGNORECASE):
        return None
    
    # Handle 3-digit shorthand
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # Parse the hex components
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    # Set alpha to 255 for 6-digit hex, or parse it for 8-digit hex
    if len(hex_color) == 8:
        a = int(hex_color[6:8], 16)
    else:
        a = 255
        
    return [r, g, b, a]

# I need to update to include alpha. I should be able to do it with alpha since I will know both colors
def get_relative_luminance(rgb_tuple):
    """
    Calculates the relative luminance of an RGB color, per WCAG 2.1.
    RGB values are assumed to be 0-255.
    """
    r, g, b = rgb_tuple
    
    # Normalize RGB values to 0-1 scale
    r_srgb = r / 255.0
    g_srgb = g / 255.0
    b_srgb = b / 255.0

    # Apply the sRGB conversion formula
    def component_to_linear(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r_linear = component_to_linear(r_srgb)
    g_linear = component_to_linear(g_srgb)
    b_linear = component_to_linear(b_srgb)

    # Calculate relative luminance
    L = 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear
    return L

def calculate_contrast_ratio(hex1, hex2):
    try:
        rgb1 = hex_to_rgb(hex1)
        rgb2 = hex_to_rgb(hex2)
    except ValueError as e:
        return str(e)

    L1 = get_relative_luminance(rgb1)
    L2 = get_relative_luminance(rgb2)

    # Ensure L1 is the lighter of the two luminances for the formula
    if L1 < L2:
        L1, L2 = L2, L1

    # WCAG contrast ratio formula
    contrast_ratio = (L1 + 0.05) / (L2 + 0.05)
    return round(contrast_ratio, 2)


def check_img_alt(input_string):
    result = []
    miss_count = 0
    len_count = 0
    img_tags = re.findall(r"<img.*?>", input_string)

    for img in img_tags:
        alt_text = re.search(r"alt=(""|')\S('|"")", img)
        if not alt_text:
            miss_count += 1
        elif len(alt_text) > 120:
            len_count += 1
 
    if miss_count:
        result.append({
            "problem": "Missing 'alt' Text",
            "element": "<img>",
            "details": "Informative images must have a descriptive 'alt' attribute.",
            "rule": "IMG_ALT_MISSING",
            "instances": miss_count
        })
    if len_count:
        result.append({
            "problem": "'alt' Text Too Long",
            "element": "<img>",
            "details": "The 'alt' attribute text should not exceed 120 characters.",
            "rule": "IMG_ALT_LENGTH",
            "instances": len_count
        })

    return result

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

def check_headers(input_string):
    result = []
    headers = re.findall(r"<h([1|2|3|4|5|6])", input_string)
    
    if headers[0] != 1:
        result.append({
            "problem": "Skipped Heading Level",
            "element": "<h" + headers[0]+ ">",
            "details": "Pages should start with <h1>. <h" + headers[0]+ "> should not be used until all lower heading levels appear first.",
            "rule": "HEADING_ORDER"
        })
    
    for index in range(1, len(headers)):
        if int(headers[index]) - int(headers[index - 1]) > 1:
            result.append({
                "problem": "Skipped Heading Level",
                "element": "<h" + headers[index - 1]+ ">, <h" + headers[index] + ">",
                "details": "The <h" + headers[index -1 ] +"> element is followed by <h" + headers[index] + ">. The heading level(s) in between should not be skipped.",
                "rule": "HEADING_ORDER"
            })

    return result

# This block ensures the Flask development server runs only when the script is executed directly.
if __name__ == '__main__':

    # Run the Flask application in debug mode for development.
    # In a production environment, you would use a production-ready WSGI server.
    app.run(debug=True)
