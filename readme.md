# Crawler for Best Sellers Products

Using web crawler to build an application that is able to find the best sellers products in website https://www.adafruit.com/categories

## Prerequisites
- Python
- MongoDB

## Run Application
Set up the environment
- ```pip install -r requirements.txt```

Run following commend line under the directory of this application
- ```python app.py```

The application will running on Running on http://0.0.0.0:5000/

## API

- ```GET /bestseller```
- ```GET /bestseller/page<int:page>```

  ```
      parameters:
          |-------------------
          |#optional
          |lower_price : _lower_price
          |upper_price : _upper_price

  ```
    Examples:
      - http://0.0.0.0:5000/bestseller
      - http://0.0.0.0:5000/bestseller/page3
      - http://0.0.0.0:5000/bestseller/page3?lower_price=15.0&upper_price=30.0

 

  - Get the best seller from the entire website.
  - Return a json contains an array of at most 20 products.
  - If not specified return the first page, otherwise return the page specified in url
  - Optional parameters lower_price and upper_price can be used to filting result within given price range


- ```GET /category/<int:category_id>/bestseller```
- ```GET /category/<int:category_id>/bestseller/page<int:page>```

  ```
      parameters:
          |-------------------
          |#optional
          |lower_price : _lower_price
          |upper_price : _upper_price

  ```

    Examples:

      - http://0.0.0.0:5000/category/117/bestseller
      - http://0.0.0.0:5000/category/117/bestseller/page2
      - http://0.0.0.0:5000/category/117/bestseller/page1?lower_price=10.0&upper_price=30.0

  - Get the best seller within a given category.
  - Return a json file contains a page of 20 products.
  - If not specified return the first page, otherwise return the page specified in url
  - Optional parameters lower_price and upper_price can be used to filting result within given price range


## Implementation

#### Storage Number Handling:
- int:Num In Stock   : int Num
- In Stock           : 100
- Out of Stock       : 0
- Discontinued       : Ignore
- Coming Soon        : Ignore

#### Ranking Priority
0 (Out of stock) > int(num In Stock) > 100(In Stock)


#### Spider design:
##### v1
- Entry from products pages https://www.adafruit.com/product/proudct_id

##### v2
- Entry from categories pages https://www.adafruit.com/categorys
