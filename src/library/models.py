from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Q


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='Secondary key',
                violation_error_message='This book with this author already exsists.'
            ),
            models.CheckConstraint(
                check=~Q(name=F('author')),
                name='Author_Name_Check',
                violation_error_message='Author name cannot be same as book name'
            )
        ]

    def __str__(self) -> str:
        return self.name


class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE)
    due = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self) -> str:
        return f"{self.book.name}-{self.user.username}"
