"""
@date: 2023-08-21
@desc:
suppose a CI model book with field book_id, name and author,
this file show how to add, get, update and delete books.
"""

from cmdb import Option, get_client


URL = ""
KEY =""
SECRET = ""


def add_book():
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    book = {"id": 1, "book_id": 1, "book_name": "平凡的世界", "author": "路遥"}
    resp = cli.add_ci("book", book)
    print(resp.ci_id)  # suppose the return ci_id is 2, will be used in update and delete


def update_book():
    """update with ci_id"""
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    book = {"book_name": "《平凡的世界》"}
    cli.update_ci("book", ci_id=2, attrs=book)


def update_book2():
    """update with unique key in model"""
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    # suppose book_id is the unique key of book
    book = {"book_name": "《平凡的世界》"}
    cli.update_ci("book", attrs=book, book_id=1)


def get_book():
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    resp = cli.get_ci(q="_type:book")
    books = resp.result
    print(books)


def delete_book():
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    resp = cli.delete_ci(ci_id=2)
    print(resp.message)
