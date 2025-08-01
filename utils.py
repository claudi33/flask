def save_book_to_file(books, filename):
    with open(filename, 'a') as f:
        for book in books:
            f.write(f'{book.name}, {book.author}, {book.pages}\n')

def load_books_from_title(filename, book_class):
    with open(filename, 'r') as f:
        for line in f:
            name, author, pages = line.strip().split(',')
            book_class(name, author, pages)
