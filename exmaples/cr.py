"""
@date: 2023-08-21
@desc:
suppose a CI model book with field id, book_id, book_name and author,
suppose a CI model rank with field id, rank_id, rank
this file show how to form a relationship between book and rank.
"""

from cmdb import Option, get_client


URL = ""
KEY =""
SECRET = ""


def add_relation():
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    book = {"id": 1,"book_id": 1, "book_name": "平凡的世界", "author": "路遥"}
    rank = {"id": 1, "rank_id": 5, rank: 11}
    book_add_resp = cli.add_ci("book", book)
    rank_add_resp = cli.add_ci("rank", rank)
    resp = cli.add_ci_relation(book_add_resp.ci_id, rank_add_resp.ci_id)
    print(resp.cr_id)  # suppose cr_id is 7, will be used in delete


def get_relation():
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    root_id = 2557  # the ci id of book, witch book's book_id==1 
    resp = cli.get_ci(root_id)
    print(resp.result)


def delete_relation():
    opt = Option(url=URL, key=KEY, secret=SECRET)
    cli = get_client(opt)
    resp = cli.delete_ci_relation(cr_id=7)
    print(resp.message)
