from ninja import NinjaAPI
from ninja.errors import HttpError
from django.shortcuts import get_object_or_404
from .models import Book
from .schemas import BookIn, BookOut

api = NinjaAPI()


@api.get('/book', response=list[BookOut], operation_id='get_all_books')
def get_all_books(request):
    try:
        return Book.objects.all()
    except Exception as e:
        raise HttpError(500, str(e))


@api.get('/book/{id}', response=BookOut, operation_id='get_book')
def get_book(request, id: int):
    book = get_object_or_404(Book, id=id)
    return book


@api.post('/book')
def create_book(request, payload: BookIn, operation_id='create_book'):
    try:
        # book = Book.objects.create(**payload.dict())
        book = Book(**payload.dict())
        book.validate_constraints()
        book.save()
        raise HttpError(200, 'Sucessful')
    except Exception as e:
        print(f"Error : {e}")
        raise HttpError(400, str(e))


@api.put('/book/{id}')
def update_book(request, id: int, payload: BookIn, operation_id='update_book'):
    book = get_object_or_404(Book, id=id)
    try:
        for attr, value in payload.dict().items():
            setattr(book, attr, value)
        book.validate_constraints()
        book.save()
    except Exception as e:
        raise HttpError(400, str(e))
    raise HttpError(201, 'Successful')


@api.delete('/book/{id}')
def delete_book(request, id: int):
    book = get_object_or_404(Book, id=id)
    book.delete()
    raise HttpError(201, 'Successful')
