import re

def check_lang(input_string):
    """
    Searches for <html>. If there is no <html> or the lang attribute is empty or invalid, returns JSON message with info about the error.
    """
    html = re.search(r"<html.*?>", input_string)
    if not html or not re.search(r"lang=['\"][a-zA-Z]{2,3}(-[a-zA-Z0-9]{2,8})*['\"]", html.group()):
        return {
            "problem": "Missing valid 'lang' Attribute",
            "element": "<html>",
            "details": "The document's primary language is not declared.",
            "rule": "DOC_LANG_MISSING"
        }

def check_title(input_string):
    """
    Searches for <title>. If there is no <title> or there is no text in the <title>, returns JSON message with info about the error.
    """
    title = re.search(r"<title.*?>\s*?\S+.*?</title>", input_string)
    if not title:
        return {
            "problem": "Missing Title",
            "element": "<title>",
            "details": "Every page must have a non-empty <title> tag.",
            "rule": "DOC_TITLE_MISSING"
        }

def check_img_alt(input_string):
    """
    Searches for <img>. If there is no alt attribute for an <img> or the alt attribute is over 120 characters,
    returns JSON messages with info about the errors
    """
    violations = []
    img_tags = re.findall(r"<img.*?>", input_string)

    # For each img, look for missing/empty alt attribute or alt attribute that is too long
    for img in img_tags:
        alt_text = re.search(r"alt=(['\"]\S+['\"])", img)
        if not alt_text:
            violations.append({
            "problem": "Missing 'alt' Text",
            "element": img,
            "details": "Informative images must have a descriptive 'alt' attribute.",
            "rule": "IMG_ALT_MISSING",
        })
        elif len(alt_text.group(1)) > 120:
            violations.append({
            "problem": "'alt' Text Too Long",
            "element": img,
            "details": "The 'alt' attribute text should not exceed 120 characters.",
            "rule": "IMG_ALT_LENGTH",
        })

    return violations

def check_link_text(input_string):
    """
    Searches for <a> elements and checks if link text is too generic. If so returns JSON message(s) with error info
    """
    violations = []
    link_matches = re.findall(r"<a href.*?>.*?</a>", input_string)

    for link in link_matches:
        link_text = re.search(r"<a href.*?>(.*?)</a>", link)
        generic_text = re.search(r"click here|click this|read more|more info|^more$|^here$|^this$", link_text.group(1), re.IGNORECASE)
        if generic_text:
            violations.append({
                "problem": "Generic Link Text",
                "element": link,
                "details": 'Link text should be descriptive. Avoid "' + link_text.group(1) + '."',
                "rule": "LINK_GENERIC_TEXT"
            })
    return violations

def check_h1(input_string):
    """
    Searches for <h1> elements. If there are more than one, returns JSON message with info about the error
    """
    h1_tags = re.findall(r"<h1", input_string)

    if len(h1_tags) > 1:
        return {
            "problem": "Multiple <h1> Tags",
            "element": "<h1>",
            "details": "Only use one <h1> per page. There are " + str(len(h1_tags)) + " in this page.",
            "rule": "HEADING_MULTIPLE_H1"
        }

def check_headers(input_string):
    """
    Searches for <h[x]> elements. If the first heading is not h1 or
    if there is an increase from one heading level to the next greater than 1,
    returns a JSON message with the appropriate error info
    """
    violations = []
    headers = re.findall(r"<h([1-6])", input_string)
    
    # Check if the first heading is <h1>
    if len(headers) and headers[0] != '1':
        violations.append({
            "problem": "Skipped Heading Level",
            "element": "<h" + (headers[0] if headers[0] else "1") + ">",
            "details": "Pages should start with <h1>. <h" + headers[0]+ "> should not be used until all lower heading levels appear first.",
            "rule": "HEADING_ORDER"
        })
    
    # Check if there is a heading level skipped, i.e. an increase greater than 1
    for index in range(1, len(headers)):
        if int(headers[index]) - int(headers[index - 1]) > 1:
            violations.append({
                "problem": "Skipped Heading Level",
                "element": "<h" + headers[index - 1]+ ">, <h" + headers[index] + ">",
                "details": "The <h" + headers[index -1 ] +"> element is followed by <h" + headers[index] + ">. The heading level(s) in between should not be skipped.",
                "rule": "HEADING_ORDER"
            })

    return violations
