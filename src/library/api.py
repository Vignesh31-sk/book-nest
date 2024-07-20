from ninja import NinjaAPI
from ninja.security import django_auth, django_auth_superuser
from ninja.errors import HttpError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from .models import Book
from library import schemas

api = NinjaAPI(csrf=True)


@api.get(
    '/book',
    response=list[schemas.BookOut],
    operation_id='get_all_books',
    auth=django_auth_superuser
)
def get_all_books(request):
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
    book = get_object_or_404(Book, id=id)
    return book


@api.post(
    '/book',
    auth=django_auth_superuser,
    operation_id='create_book'
)
def create_book(request, payload: schemas.BookIn):
    try:
        # book = Book.objects.create(**payload.dict())
        book = Book(**payload.dict())
        book.validate_constraints()
        book.save()
        raise HttpError(200, 'Sucessful')
    except Exception as e:
        print(f"Error : {e}")
        raise HttpError(400, str(e))


@api.put(
    '/book/{id}',
    operation_id='update_book',
    auth=django_auth_superuser
)
def update_book(request, id: int, payload: schemas.BookIn):
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


@api.post('/login', operation_id='login')
def login_user(request, payload: schemas.UserIn):
    user = authenticate(username=payload.username, password=payload.password)
    print(user)
    if user is not None:
        login(request=request, user=user)
        raise HttpError(200, 'Login successful')
    raise HttpError(401, 'Cannot login. Invalid Credentials')


@api.get('/logout', operation_id='logout')
def logout_user(request):
    logout(request=request)
    raise HttpError(200, 'User logged out.')
