# ada_compliance_checker
This app evaluates html to check for ADA compliance


## Installation
set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

git clone

pip install -r requirements.txt

## Run locally
python app.py

Then send a POST request to http://127.0.0.1:5000/api/ada-check with a JSON body that has an "html" key with a value of the html to check.