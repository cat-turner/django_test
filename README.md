Perch Take-Home Test

First, make sure to install `django` https://docs.djangoproject.com/en/3.1/topics/install/#installing-official-release
Also install `rest_framework` https://www.django-rest-framework.org/#installation
Feel free to use any additional packages 

Three important files to look at in the `transactions` folder:
1. `models.py`
2. `example_transactions.csv`
3. `views.py`


In `models.py`, you will write the model definition for an `FBATransaction`

You will need to examine `example_transactions.csv` to determine what fields a transaction can have

After the model definition is completed, read the API endpoints stubbed out in `views.py` and add the functionality specified in the comments.

Postman is highly recommended to use to test your endpoints after writing them (https://www.postman.com/downloads/)
You can run the server by calling `python manage.py runserver` and route requests to `localhost:8000`.

Assumptions:

- I am assuming that the geographic data is correct and will not check if the zip code matches the city
- Averages should only be done for the same type, because Fees are negative while orders are positive. It doesn't make sense to have fees and orders be averaged since they are different types
- Order types are unique, and have their own meaning. For example Order and Order_Retrochange are different transaction types, and are not considered the same kind of transaction type.
- 

Dev notes:
I am using pipenv for dependency management. To install:
```
brew install pipenv
```

To install dependencies used for this assigment, type the commands:
```
pipenv install
```

It looks like the link you include to install django is referring to 