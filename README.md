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


## Running

You can run the app with:

python3 run.py 

and then visit the page http://127.0.0.1:5000/  
From this page, you can:

1. add a new shortened url
2. retrieve all the existing shortened urls
3. delete all the existing shortened urls
4. navigate to the shortened url and be redirected to the target url
5. configure an existing shortened url to redirect to a different target

## Testing

You can test the app with:

python3 test.py 


## Author

**Alessandro Marra** - (https://github.com/Ale-Marra)
