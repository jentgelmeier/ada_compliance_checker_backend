# ADA Compliance Checker
## Introduction
This app evaluates a string of html code to check that it complies with the following ADA rules.

1. General Document Structure
* **Language**: The `<html>` element must have a valid lang attribute.
* **Title**: Every page must have a non-empty `<title>` tag.
* **Color Contrast**: Text must have a contrast ratio of at least 4.5:1 for normal text and
3.0:1 for large text. Large text is ≥ 18 pt (~24 pixels) unbolded or ≥ 14 pt (~18.66 pixels) bolded.
2. Images
* **Alternative Text**: All `<img>` tags must have an alt attribute.
* **Alternative Text Length**: The alt attribute text should not exceed 120 characters to remain concise.
3. Links
* **Meaningful Link Text**: Link text must not be generic (e.g., "click here").
4. Headings
* **Hierarchical Order**: Heading levels must not be skipped.
* **Single `<h1\>`**: There must be only one `<h1>` per page.

## Innovative Features
The most advanced techniques in this app are those used to identify low color contrast ratios. The relevant code can be found in the /backend/contrast_check file. If I wanted to keep things simple, I could have only identified color contrast ratios based on inline styling and one color format--hex codes, for example. However, I chose to devote significant attention to this rule and make the program robust. Therefore, the app identifies styling from a `<style>` tag and inline styling; it reads colors formatted as hex codes, color aliases, rgb values, and even rgba values; and it accounts for font-size and font-weight based on styling or element tags (for instance, the app recognizes a `<b>` tag as bolded text and uses a different font-size threshold to determine what is "large" text for bold text compared to unbolded text).

The primary function checking the contrast ratios is the check_contrast_ratio function, which uses several smaller functions, to complete sub-tasks. The app first converts styling from a `<style>` to inline styling by parsing the html using BeautifulSoup and identifying the css rules using tinycss2 (see apply_styles_to_inline function). Next, the app goes through each element and identifies the color, background-color, font-weight, and font-size based on the inline styling; it assumes preset defaults when these are unspecified. If any colors are found, it converts the these to rgba values (see parse_color function)Based on the font-weight, font-size, and the specific element (`<hx>` elements have default font-sizes), it determines the minimum contrast ratio. Next, if the foreground color's alpha is less than 1.0, it blends the foreground and background colors based on the foreground color's alpha to produce a rgb value for the foreground color (see blend_rgba_with_rbg function). Last, it calculates the relative luminance values of both colors to determine the contrast ratio between the foreground and background colors (see calculate_contrast_ratio and get_relative_luminance functions). If the ratio is the below the minimum, a JSON object is returned with the violation details.

In addition to the color contrast feature, I added a feature to check html by providing a url. Simply click the toggle to switch to the URL Input mode and enter a valid url. The app will scrape the html and check for accessibility issues. The code for this can be found in the /backend/app file under the /api/v1/url-check route. It uses the requests library to retrieve the html text. I also included tests for the /api/v1/html-check endpoint.

### Limitations (color contrast ratio): 
* This app does not incorporate external stylesheets.
* If the color is in the hex code format, the app won't be able to read it unless it between 6-8 digits long. 3-digit hex codes won't work.
* It can't determine color contrast ratios from background images
* It only identifies background color from the "background-color" property. It won't pick up background colors from the more generic "background" property. 
* It can only identify font-size specified in pixels (%, vw, em, rem will not work). In these cases, the app will flag any ratios below 4.5:1. If the ratio is greater than 3.0:1, it will acknowledge it can't determine the font-size and that the contrast ratio may be okay if the text is large. 
* It cannot prioritize css styling from a `<style>` tag correctly (id > class > tag). Instead, if two separate rules apply to the same element, the app gives priority to the first rule, so there will be inaccurate results in such cases. 
* The blend_rgba_with_rgb function does not account for the background color's alpha; instead it assumes the background color is fully opaque. A potential expansion of this project could account for the background's alpha by blending any background colors with an alpha less than 1 against the element's inherited background. This would require looping through parent elements to determine if any have a specified background color.

## Install and Run Locally
Prerequisites: Python 3, pip, Node

If you don't have these installed, you can easily find instructions on how to install these using an AI chatbot or a search engine. For reference, I am using python 3.12.10, pip 25.0.1, and Node 22.19.0.

### Front End
Unzip the file. Then use the terminal to navigate to the /frontend folder. Enter `npm i` to install the dev dependencies. Then enter `npm run dev` to start the dev server. Navigate to http://localhost:5173/ in your browser. The app will not work properly until you run the back end as well.

### Back End
Use the terminal to navigate to the /backend folder. If you are currently in the /frontend folder, enter `cd ../backend`. First, you will need to set up a virtual environment and then activate it. To do this enter
```
python3 -m venv .venv
source .venv/bin/activate
```
To verify that your virtual environment is active, check to make sure that your terminal now shows a prefix that says (.venv) at the start of your shell prompt. Next, install the requirements from the requirements file by entering `pip install -r requirements.txt`.

Finally, to start the dev server, enter `python3 app.py`. It will run on http://127.0.0.1:5000, but you don't need to navigate there. Just use the frontend app at http://localhost:5173/. You can now enter html code and click Submit to check for accessibility issues. Feel free to copy and paste an html string from the test.py file.

## Testing
The Backend includes a test file that can be run in the terminal. Navigate to the /backend file and enter `python3 test.py` to run the tests. There are 10 tests in total that test an html string with no issues and 9 other html strings that include violations of all eight rules listed above.
