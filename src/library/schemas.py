from library import models
from django.contrib.auth.models import User
from ninja import ModelSchema


class BookOut(ModelSchema):
    class Meta:
        model = models.Book
        fields = '__all__'


class BookIn(ModelSchema):
    class Meta:
        model = models.Book
        exclude = ['id']


class UserIn(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'password']
