# ADA Compliance Checker
## Introduction
This app evaluates a string of html code to check that it complies with the following ADA rules.

1. General Document Structure
* **Language**: The `<html>` element must have a valid lang attribute.
* **Title**: Every page must have a non-empty `<title>` tag.
* **Color Contrast**: Text must have a contrast ratio of at least 4.5:1 for normal text and
3.0:1 for large text. Large text is any unbolded text that has a font size equal to or greater than 24 pixels or bolded text that has a font size equal to or greater than 18.5 pixels.
2. Images
* **Alternative Text**: All `<img>` tags must have an alt attribute.
* **Alternative Text Length**: The alt attribute text should not exceed 120 characters to remain concise.
3. Links
* **Meaningful Link Text**: Link text must not be generic (e.g., "click here").
4. Headings
* **Heirarchical Order**: Heading levels must not be skipped.
* **Single `<h1\>`**: There must be only one `<h1>` per page.

## Innovative Features
The most advanced techniques in this app are those used to identify low color contrast ratios. The relevant code can be found in the /backend/contrask_check file. If I wanted to keep things simple, I could have only identified color contrast ratios based on inline styling and one color format-- hex codes, for example. However, I chose to devote significant attention to this rule and make the program robust. Therefore, the app identifies styling from a `<style>` tag and inline styling; it reads colors formatted as hex codes, color aliases, rgb values, and even rgba values; and it accounts for font-size and font-weight based on styling or element tags (for instance, the app recognizes a `<strong>` tag as bolded text and uses a different font-size threshold to determine what is "large" text compared to normal-sized text).



## Install and Run Locally
Prerequisites: Python 3, pip, Node

If you don't have these installed, you can easiy find instructions on how to install these using an AI chatbot or a search engine. For reference, I am using python 3.12.10, pip 25.0.1, and Node 22.19.0.

### Front End
Unzip the file. Then use the terminal to navigate to the /frontend folder. Enter `npm i` to install the dev dependncies. Then enter `npm run dev` to start the dev server. Navigate to http://localhost:5173/ in your browser. The app will not work properly until you run the back end as well.

### Back End
Use the terminal to naviate to the /backend folder. If you are currently in the /frontend folder, enter `cd ../backend`. First, you will need to set up a virtual environment and then activate it. To do this enter
```
python3 -m venv .venv
source .venv/bin/activate
```
To verify that your virtual environment is active, check to make sure that your terminal now shows a prefix that says (.venv) at the start of your shell prompt. Next, intall the requirements from the requirements file by entering `pip install -r requirements.txt`.

Finally, to start the dev server, enter `python3 app.py`. It will run on http://127.0.0.1:5000, but you don't need to navigate there. Just use the frontend app at http://localhost:5173/. You can now enter html code and click Submit to check for accessibility issues. Feel free to copy and paste an html string from the test.py file.

## Testing
The Backend includes a test file that can be run in the terminal. Navigate to the /backend file and enter `python3 test.py` to run the tests. There are 10 tests in total that test an html string with no issues and 9 other html strings that include violations of all eight rules listed above.
