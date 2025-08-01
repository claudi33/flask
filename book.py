
class Book:
    all_books = []

    def __init__(self, name, author, pages):
        self.name = name
        self.author = author
        self.pages = int(pages)

    def __str__(self):
        return f'{self.name}, {self.author}, {self.pages}'
    @classmethod
    def add_book(cls, book: object):
        cls.all_books.append(book)

    @classmethod
    def show_books(cls):
        for i in cls.all_books:
            print(i)

    @classmethod
    def look_for_author(slc, author):
        for book in slc.all_books:
            if book.author == author:
                print(book)

    @classmethod
    def sum_of_pages(cls):
        res = 0
        for book in cls.all_books:
            res += book.pages
        return res

    @classmethod
    def longest_book(cls):
        return max(cls.all_books, key=lambda b: b.pages)