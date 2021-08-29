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
- Order types are unique, and have their own meaning. For example Order and Order_Retrochange are different transaction types, and are not considered the same kind of transaction type.
- I assume that rows can be made unique with their order id and type. This will allow us to upload
the same file without duplicating rows

Dev notes:
I am using pipenv for dependency management. To install:
```
brew install pipenv
```

To install dependencies used for this assigment, type the commands:
```
pipenv install
```

Run migrations first.
```
./manage.py makemigrations
./manage.py migrate
```

Start server.
```
python manage.py runserver
```

To upload a file, you can use curl, try this command in a different terminal:
```
curl -i --form docfile=@./example_transactions.csv http://127.0.0.1:8000/api/transactions/
```