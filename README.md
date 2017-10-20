## Description

A url-shortener


## Compatability

This program has been written with Python 3.6


## Install 

After creating and activing the virtual environment with:

virtualenv -p python3 envname
source envname/bin/activate

The requirements can be installed with: 

pip3 install -r requirements.txt


# Running

You can run the app with:

python3 run.py 

and then visit the page http://127.0.0.1:5000/  
From this page, you can add a new shortened url by inserting the full url in the unique input of the page and clicking on "Get shortened url", or retrieve all the shortened urls by clicking on "Get all urls"

# Testing

You can test the app with:

python3 test.py 

I couldn't (yet) set a different database for the test, therefore I am testing on the production database.


## Author

**Alessandro Marra** - (https://github.com/Ale-Marra)
