from django.db import models
from django.contrib.auth.models import User
from django.db.models import F, Q

""" Contains 2 Entity and 1 Relationship """


class Book(models.Model):
    """
        Book entity with attributes name and author.
    """
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)

    class Meta:
        constraints = [
            # Ensure that no book is repeated.
            models.UniqueConstraint(
                fields=['name', 'author'],
                name='Secondary key',
                violation_error_message='This book with this author already exsists.'
            ),
            # Ensure that the author name and book name are not same
            models.CheckConstraint(
                check=~Q(name=F('author')),
                name='Author_Name_Check',
                violation_error_message='Author name cannot be same as book name'
            )
        ]

    def __str__(self) -> str:
        return self.name


""" For a User entity Django's built in User Model is used. """


class Borrow(models.Model):
    """
    A relationship to represent who borrowed book.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.OneToOneField(
        Book, on_delete=models.CASCADE)
    due = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self) -> str:
        return f"{self.book.name}-{self.user.username}"
