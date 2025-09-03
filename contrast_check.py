import re
import tinycss2
from bs4 import BeautifulSoup


# W3C color aliases in a dictionary for easy lookup
W3C_COLORS = {
    "aliceblue": [240, 248, 255], "antiquewhite": [250, 235, 215],
    "aqua": [0, 255, 255], "aquamarine": [127, 255, 212],
    "azure": [240, 255, 255], "beige": [245, 245, 220],
    "bisque": [255, 228, 196], "black": [0, 0, 0],
    "blanchedalmond": [255, 235, 205], "blue": [0, 0, 255],
    "blueviolet": [138, 43, 226], "brown": [165, 42, 42],
    "burlywood": [222, 184, 135], "cadetblue": [95, 158, 160],
    "chartreuse": [127, 255, 0], "chocolate": [210, 105, 30],
    "coral": [255, 127, 80], "cornflowerblue": [100, 149, 237],
    "cornsilk": [255, 248, 220], "crimson": [220, 20, 60],
    "cyan": [0, 255, 255], "darkblue": [0, 0, 139],
    "darkcyan": [0, 139, 139], "darkgoldenrod": [184, 134, 11],
    "darkgray": [169, 169, 169], "darkgreen": [0, 100, 0],
    "darkgrey": [169, 169, 169], "darkkhaki": [189, 183, 107],
    "darkmagenta": [139, 0, 139], "darkolivegreen": [85, 107, 47],
    "darkorange": [255, 140, 0], "darkorchid": [153, 50, 204],
    "darkred": [139, 0, 0], "darksalmon": [233, 150, 122],
    "darkseagreen": [143, 188, 143], "darkslateblue": [72, 61, 139],
    "darkslategray": [47, 79, 79], "darkslategrey": [47, 79, 79],
    "darkturquoise": [0, 206, 209], "darkviolet": [148, 0, 211],
    "deeppink": [255, 20, 147], "deepskyblue": [0, 191, 255],
    "dimgray": [105, 105, 105], "dimgrey": [105, 105, 105],
    "dodgerblue": [30, 144, 255], "firebrick": [178, 34, 34],
    "floralwhite": [255, 250, 240], "forestgreen": [34, 139, 34],
    "fuchsia": [255, 0, 255], "gainsboro": [220, 220, 220],
    "ghostwhite": [248, 248, 255], "gold": [255, 215, 0],
    "goldenrod": [218, 165, 32], "gray": [128, 128, 128],
    "green": [0, 128, 0], "greenyellow": [173, 255, 47],
    "grey": [128, 128, 128], "honeydew": [240, 255, 240],
    "hotpink": [255, 105, 180], "indianred": [205, 92, 92],
    "indigo": [75, 0, 130], "ivory": [255, 255, 240],
    "khaki": [240, 230, 140], "lavender": [230, 230, 250],
    "lavenderblush": [255, 240, 245], "lawngreen": [124, 252, 0],
    "lemonchiffon": [255, 250, 205], "lightblue": [173, 216, 230],
    "lightcoral": [240, 128, 128], "lightcyan": [224, 255, 255],
    "lightgoldenrodyellow": [250, 250, 210], "lightgray": [211, 211, 211],
    "lightgreen": [144, 238, 144], "lightgrey": [211, 211, 211],
    "lightpink": [255, 182, 193], "lightsalmon": [255, 160, 122],
    "lightseagreen": [32, 178, 170], "lightskyblue": [135, 206, 250],
    "lightslategray": [119, 136, 153], "lightslategrey": [119, 136, 153],
    "lightsteelblue": [176, 196, 222], "lightyellow": [255, 255, 224],
    "lime": [0, 255, 0], "limegreen": [50, 205, 50],
    "linen": [250, 240, 230], "magenta": [255, 0, 255],
    "maroon": [128, 0, 0], "mediumaquamarine": [102, 205, 170],
    "mediumblue": [0, 0, 205], "mediumorchid": [186, 85, 211],
    "mediumpurple": [147, 112, 219], "mediumseagreen": [60, 179, 113],
    "mediumslateblue": [123, 104, 238], "mediumspringgreen": [0, 250, 154],
    "mediumturquoise": [72, 209, 204], "mediumvioletred": [199, 21, 133],
    "midnightblue": [25, 25, 112], "mintcream": [245, 255, 250],
    "mistyrose": [255, 228, 225], "moccasin": [255, 228, 181],
    "navajowhite": [255, 222, 173], "navy": [0, 0, 128],
    "oldlace": [253, 245, 230], "olive": [128, 128, 0],
    "olivedrab": [107, 142, 35], "orange": [255, 165, 0],
    "orangered": [255, 69, 0], "orchid": [218, 112, 214],
    "palegoldenrod": [238, 232, 170], "palegreen": [152, 251, 152],
    "paleturquoise": [175, 238, 238], "palevioletred": [219, 112, 147],
    "papayawhip": [255, 239, 213], "peachpuff": [255, 218, 185],
    "peru": [205, 133, 63], "pink": [255, 192, 203],
    "plum": [221, 160, 221], "powderblue": [176, 224, 230],
    "purple": [128, 0, 128], "rebeccapurple": [102, 51, 153],
    "red": [255, 0, 0], "rosybrown": [188, 143, 143],
    "royalblue": [65, 105, 225], "saddlebrown": [139, 69, 19],
    "salmon": [250, 128, 114], "sandybrown": [244, 164, 96],
    "seagreen": [46, 139, 87], "seashell": [255, 245, 238],
    "sienna": [160, 82, 45], "silver": [192, 192, 192],
    "skyblue": [135, 206, 235], "slateblue": [106, 90, 205],
    "slategray": [112, 128, 144], "slategrey": [112, 128, 144],
    "snow": [255, 250, 250], "springgreen": [0, 255, 127],
    "steelblue": [70, 130, 180], "tan": [210, 180, 140],
    "teal": [0, 128, 128], "thistle": [216, 191, 216],
    "tomato": [255, 99, 71], "turquoise": [64, 224, 208],
    "violet": [238, 130, 238], "wheat": [245, 222, 179],
    "white": [255, 255, 255], "whitesmoke": [245, 245, 245],
    "yellow": [255, 255, 0], "yellowgreen": [154, 205, 50]
}


def apply_styles_to_inline(html_string):
    """
    Finds color/background-color rules in <style> tags and applies them as inline styles.
    It removes the <style> tags after processing.

    Returns:
        str: The modified HTML string with inline color styles.
    """
    soup = BeautifulSoup(html_string, 'html.parser')
    style_tags = soup.find_all('style')

    # Store styles to apply
    rules_to_apply = []

    # Retrieve rules from style tags
    for style_tag in style_tags:
        css_text = style_tag.string
        if not css_text:
            continue
        
        parsed_rules = tinycss2.parse_stylesheet(css_text)

        for rule in parsed_rules:
            if rule.type == 'qualified-rule':
                selector = tinycss2.serialize(rule.prelude).strip()
                styles_to_apply = {}
                declarations = tinycss2.parse_blocks_contents(rule.content)
                for declaration in declarations:
                    if declaration.type == 'declaration':
                        name = declaration.name
                        value = tinycss2.serialize(declaration.value).strip()
                        styles_to_apply[name] = value
                
                if styles_to_apply:
                    rules_to_apply.append({'selector': selector, 'styles': styles_to_apply})
        
        # Remove the <style> tag from the HTML tree after parsing
        style_tag.decompose()

    # Now, apply the styles to the elements
    for rule in rules_to_apply:
        try:
            elements_to_style = soup.select(rule['selector'])
            for element in elements_to_style:
                existing_styles = rule['styles']
                existing_attr = element.get('style', '')
                if existing_attr:
                    for prop in existing_attr.split(';'):
                        if ':' in prop:
                            name, value = prop.split(':', 1)
                            existing_styles[name.strip()] = value.strip()
                
                new_style_str = '; '.join([f"{name}: {value}" for name, value in existing_styles.items()])
                element['style'] = new_style_str

        except Exception as e:
            print(f"Warning: Could not select elements for '{rule['selector']}'. Error: {e}")

    return soup
 
def parse_color(color_string):
    """Converts a color string (hex, rgb, rgba, name) to an RGBA tuple."""
    color_string = color_string.strip().lower()

    if color_string in W3C_COLORS:
        rgb = W3C_COLORS[color_string]
        return tuple(rgb) + (255,)
    
    # Hex with alpha (#RRGGBBAA) or without (#RRGGBB)
    hex_match = re.fullmatch(r'#?([0-9a-fA-F]{6}|[0-9a-fA-F]{8})', color_string)
    if hex_match:
        hex_color = hex_match.group(1)
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16) if len(hex_color) == 8 else 255
        return (r, g, b, a)

    # RGB or RGBA format
    rgba_match = re.fullmatch(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', color_string)
    if rgba_match:
        r, g, b = [int(c) for c in rgba_match.group(1, 2, 3)]
        a = float(rgba_match.group(4)) if rgba_match.group(4) else 1.0
        return (r, g, b, int(a * 255))
        
    return None

def get_relative_luminance(rgb_tuple):
    """Calculates the relative luminance of an RGB color."""
    r, g, b = [c / 255.0 for c in rgb_tuple]

    def component_to_linear(c):
        if c <= 0.03928:
            return c / 12.92
        else:
            return ((c + 0.055) / 1.055) ** 2.4

    r_linear = component_to_linear(r)
    g_linear = component_to_linear(g)
    b_linear = component_to_linear(b)

    return 0.2126 * r_linear + 0.7152 * g_linear + 0.0722 * b_linear

def blend_rgba_with_rgb(rgba_fg, rgb_bg):
    """Blends an RGBA foreground color with an opaque RGB background."""
    fg_r, fg_g, fg_b, fg_a = [c / 255.0 for c in rgba_fg]
    bg_r, bg_g, bg_b = [c / 255.0 for c in rgb_bg]

    blended_r = (fg_r * fg_a) + (bg_r * (1 - fg_a))
    blended_g = (fg_g * fg_a) + (bg_g * (1 - fg_a))
    blended_b = (fg_b * fg_a) + (bg_b * (1 - fg_a))

    return (int(blended_r * 255), int(blended_g * 255), int(blended_b * 255))

def calculate_contrast_ratio(rgb1, rgb2):
    """Calculates the contrast ratio between two RGB colors."""
    L1 = get_relative_luminance(rgb1)
    L2 = get_relative_luminance(rgb2)
    L_light = max(L1, L2)
    L_dark = min(L1, L2)
    return (L_light + 0.05) / (L_dark + 0.05)

def check_contrast_ratio(html_string):
    """
    Analyzes an HTML string for color contrast violations. Unable to read font-sizes if they aren't in pixels.
    The function accounts for font-size, font-weight, and color to determine contrast ratios. 
    It will convert styles in a style tag to inline styles to determine contrast ratios.

    Returns:
        list: A list of dictionaries, where each dictionary represents an element
              that failed the contrast check.
    """
    soup = apply_styles_to_inline(html_string)
    violations = []
    
    default_text_color = (0, 0, 0)      # black
    default_bg_color = (255, 255, 255)  # white

    large_text_min_ratio = 3.0 # large text min ratio 3:1
    text_min_ratio = 4.5 # standard text min ratio 4.5:1

    for element in soup.find_all(True):
        if not element.string:
            continue  # Skip elements without text content

        # Traverse up the DOM tree to find inherited colors and font-size
        current_element = element
        fg_color = None
        bg_color = None
        font_size = None
        font_weight = None

        # default minimum ratio to standard text minimum 4.5:1
        min_ratio = text_min_ratio
        # unknown font-size flag
        unknown_fs = False

        while current_element and (not fg_color or not bg_color or not font_size):
            style = current_element.get('style', '')
            # Use regex to find color, background-color, font-size, font-weight properties
            fg_match = re.search(r'(?<!-)color\s*:\s*([^;]+)', style)
            bg_match = re.search(r'background-color\s*:\s*([^;]+)', style)
            fs_match = re.search(r'font-size\s*:\s*([^;]+)', style)
            fw_match = re.search(r'font-weight\s*:\s*([^;]+)', style)

            if not fg_color and fg_match:
                fg_color = parse_color(fg_match.group(1))
            
            if not bg_color and bg_match:
                bg_color = parse_color(bg_match.group(1))
            
            if not font_size and fs_match:
                font_size = fs_match.group(1)
            
            if not font_weight and fw_match:
                font_weight = fw_match.group(1)
            
            current_element = current_element.parent

        # Use default colors if none are found in the element or its parents
        fg_tuple = fg_color if fg_color else (default_text_color[0], default_text_color[1], default_text_color[2], 255)
        bg_tuple = bg_color if bg_color else (default_bg_color[0], default_bg_color[1], default_bg_color[2], 255)

        # Default font-weight to 400
        if not font_weight:
            font_weight = 400
        
        # Use large text ratio if no font-size given for h1-h4 headings
        if not font_size:
            if element.name == "h1":
                min_ratio = large_text_min_ratio
            elif element.name == "h2":
                min_ratio = large_text_min_ratio
            elif element.name == "h3":
                min_ratio = large_text_min_ratio
            elif element.name == "h4":
                min_ratio = large_text_min_ratio
        elif "px" not in font_size:
            # Cannot determine font-size if it is not in pixels
            unknown_fs = True
        else:
            # Extract just the number to compare size
            fs_digits = re.search(r'(\d+)\s*px', font_size)

            if element.name in ["strong", "b"] or font_weight == "bold" or int(font_weight) >= 700:
                if int(fs_digits.group(1)) >= 18.5: # If the font is bold and bigger than 18.5px, it's considered large text
                    min_ratio = large_text_min_ratio
            elif int(fs_digits.group(1)) >= 24: # Normal font is considered large if its bigger than 24px
                min_ratio = large_text_min_ratio


        # If foreground is transparent, blend it with the background
        if fg_tuple[3] < 255:
            final_fg_rgb = blend_rgba_with_rgb(fg_tuple, (bg_tuple[0], bg_tuple[1], bg_tuple[2]))
        else:
            final_fg_rgb = (fg_tuple[0], fg_tuple[1], fg_tuple[2])

        # Calculate contrast ratio between the final opaque colors
        ratio = calculate_contrast_ratio(final_fg_rgb, (bg_tuple[0], bg_tuple[1], bg_tuple[2]))

        if ratio < min_ratio:
            details = f"Unable to determine font-size. The contrast ratio is {round(ratio, 2)}. This is okay for large text, but the minimum required for normal text is {min_ratio}." \
                        if unknown_fs and ratio > 3 \
                        else f"The contrast ratio is {round(ratio, 2)}. The minimum required for {"normal" if min_ratio == 4.5 else "large"} text is {min_ratio}."
            violations.append({
                'problem': "Low Contrast Ratio",
                'element': str(element).strip(),
                'ratio': round(ratio, 2),
                'foreground_color': f"rgb({final_fg_rgb[0]}, {final_fg_rgb[1]}, {final_fg_rgb[2]})",
                'background_color': f"rgb({bg_tuple[0]}, {bg_tuple[1]}, {bg_tuple[2]})",
                'details': details,
                'rule': "COLOR_CONTRAST"
            })
            
    return violations
