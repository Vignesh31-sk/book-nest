from ninja import Schema


class BookOut(Schema):
    id : int
    name : str
    author :str

class BookIn(Schema):
    name : str
    author : str
