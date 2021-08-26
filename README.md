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
1. order ids are unique, and can be used as the primary key. In the real world, we could assume they may not be unique, and thus we will need to make them. But we will need to make an assertion that they will be unique for their provider.
2. All the types in the csv are they types that we permit. Any data that is not that type will throw an error.
3. I am assuming that the geographic data is correct and will not check if the zip code matches the city
4. Averages should only be done for the same type, because Fees are negative while orders are positive. It doesn't make sense to have fees and orders be averaged since they are different types

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