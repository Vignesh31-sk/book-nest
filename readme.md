# Book Nest - Library Management System

A simplified backend for an online library management using Django-ninja.

The system can perform following actions.

1. Admin Actions:
- Add new books to the library.
- Update book details.
- Delete books from the library.
- View all books in the library.

2. User Actions:
- View the list of available books.
- View list of borrowed books.
- Borrow a book.
- Return a borrowed book.


## Deployment Instructions.

Install pipenv ( A virtual environment management tool )
```
pip install pipenv
```
Install the required packages.

```
pipenv install
```
Activate the environment.
```
pipenv shell
```
Move to src directory.

```
cd src
```
Create the database and tables.
```
pipenv run manage.py migrate
```
Create a admin account.
```
pipenv run manage.py createsuperuser
```
Start the server.
```
pipenv run manage.py runserver
```

## Usage

####  Your api web-interface will be running on *[localhost:8000/api/docs](http://127.0.0.1:5000/api/docs)*  by default.

#### Through the api interface you can interact with the API.

#### Watch the below vedio for the reference.
https://drive.google.com/file/d/1j4sZ8nVTyl-h4rd-po4Y_QwgPVJ6VKiN/view?usp=sharing



To close the server press `Ctrl-C` 

To remove your python environments.
```
deactivate
```
```
pipenv --rm
```

Thanks for using our application. ! :smiley: