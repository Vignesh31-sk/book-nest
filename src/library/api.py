from ninja import NinjaAPI
from ninja.security import django_auth, django_auth_superuser
from ninja.errors import HttpError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from .models import Book, Borrow
from library import schemas
from datetime import datetime, timedelta

api = NinjaAPI(csrf=True)

""" Administrative tasks endpoints."""


@api.get(
    '/book',
    response=list[schemas.BookOut],
    operation_id='get_all_books',
    auth=django_auth_superuser
)
def get_all_books(request):
    """Get all books"""
    try:
        return Book.objects.all()
    except Exception as e:
        raise HttpError(500, str(e))


@api.get(
    '/book/{id}',
    response=schemas.BookOut,
    operation_id='get_book',
    auth=django_auth_superuser
)
def get_book(request, id: int):
    """ Get a book by book's id"""
    book = get_object_or_404(Book, id=id)
    return book


@api.post(
    '/book',
    auth=django_auth_superuser,
    operation_id='create_book'
)
def create_book(request, payload: schemas.BookIn):
    """Create a new book."""
    try:
        book = Book(**payload.dict())
        book.validate_constraints()
        book.save()
        return 200, "Successful"
    except Exception as e:
        print(f"Error : {e}")
        raise HttpError(400, str(e))


@api.put(
    '/book/{id}',
    operation_id='update_book',
    auth=django_auth_superuser
)
def update_book(request, id: int, payload: schemas.BookIn):
    """Update a book"""
    book = get_object_or_404(Book, id=id)
    try:
        for attr, value in payload.dict().items():
            setattr(book, attr, value)
        book.validate_constraints()
        book.save()
    except Exception as e:
        raise HttpError(400, str(e))
    raise HttpError(201, 'Successful')


@api.delete(
    '/book/{id}',
    auth=django_auth_superuser,
    operation_id='delete_book'
)
def delete_book(request, id: int):
    book = get_object_or_404(Book, id=id)
    book.delete()
    raise HttpError(201, 'Successful')


""" Login, Logout and SignUp endpoints."""


@api.post("/user", operation_id='create_user')
def create_user(request, payload: schemas.UserIn):
    user = User.objects.filter(username=payload.username)
    if user.exists():
        raise HttpError(400, 'User already exsists')
    try:
        User.objects.create_user(
            username=payload.username,
            password=payload.password
        )
    except Exception as e:
        raise HttpError(400, str(e))
    raise HttpError(200, 'User has been created.')


@api.get('/token')
def get_csrf_token(request):
    token = get_token(request)
    return 200, {"csrf-token": token}


@api.post('/login', operation_id='login')
def login_user(request, payload: schemas.UserIn):
    user = authenticate(username=payload.username, password=payload.password)
    if user is not None:
        login(request=request, user=user)
        csrf_token = get_token(request)
        return 200, {"Status": "Login Successful", "CSRF-Token": csrf_token}
    raise HttpError(401, 'Cannot login. Invalid Credentials')


@api.get('/logout', operation_id='logout')
def logout_user(request):
    logout(request=request)
    raise HttpError(200, 'User logged out.')


"""User tasks endpoints"""


@api.get(
    '/availabe',
    operation_id='available_book',
    response=list[schemas.BookOut],
    auth=django_auth
)
def get_available_book(request):
    """Get list of available books."""
    books = Book.objects.filter(borrow__isnull=True)
    return books


@api.get('/borrow', response=list[schemas.BookOut], auth=django_auth)
def get_borrowed_books(request):
    """ Get list of borrowed books."""
    try:
        books = Book.objects.filter(borrow__user=request.user)
    except Exception as e:
        raise HttpError(400, str(e))
    return books


@api.post('/borrow/{id}', operation_id='borrow_book', auth=django_auth)
def borrow_book(request, id: int):
    """ Borrow a book by book's id"""
    try:
        user = request.user
        book = Book.objects.get(id=id)
        borrow = Borrow(user=user, book=book)
        borrow.due = datetime.now().date() + timedelta(days=15)
        borrow.save()
    except Exception as e:
        raise HttpError(400, str(e))
    return 200, "Book borrowed successfully"


@api.delete('/return/{id}', auth=django_auth)
def return_book(request, id: int):
    """ Return a book by book's id"""
    try:
        borrow = Borrow.objects.get(book=id)
        borrow.delete()
        return 200, 'Returned Book sucessfully'
    except Exception as e:
        raise HttpError(400, str(e))
