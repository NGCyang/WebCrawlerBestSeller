# Crawler for Best Sellers Products

Using web crawler to build an application that is able to find the best sellers products in website https://www.adafruit.com/categories

## Prerequisites
- Python
- MongoDB

## Run Application
Set up Environment
- ```pip install -r requirements.txt```

Run following commend line under the directory of this application
- ```python app.py```

## API
- ```GET /bestseller```

  Get the best seller from the entire website

- ```GET /bestseller/category/<category_id>```

  Get the best seller within given category.
A complete table for category id and category name can be found in ...
