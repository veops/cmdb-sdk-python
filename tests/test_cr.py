"""
suppose a CI model book with field id, name and auther,
suppose a CI model rank with field rank_id, book_id, rank
"""


import os

from cmdb.core.ci import CIClient, Option
from cmdb.core.ci_relations import CIRelationClient


CR_ID = None


class TestCI:

    def setup_method(self) -> None:
        opt = Option(
            os.environ["CMDB_HOST"],
            os.environ["CMDB_KEY"],
            os.environ["CMDB_SECRET"],
        )
        self.ci_client = CIClient(opt=opt)
        self.client = CIRelationClient(opt=opt)
        self.add_ci()
    
    def add_ci(self):
        book = {
            "id": 1,
            "book_id": 1,
            "book_name": "平凡的世界",
            "auther": "路遥",
        }
        rank = {
            "id": 1,
            "rank_id": 1,
            "rank": 5,
        }
        self.ci_client.add_ci("book", book)
        self.ci_client.add_ci("rank", rank)

    def find_ci(self, q: str):
        resp = self.ci_client.get_ci(q=q).result
        if not resp:
            return
        return resp[0]

    def test_add_ci_relation(self):
        book = self.find_ci(q="_type:book,book_id:1")
        rank = self.find_ci(q="_type:rank,rank_id:1")
        resp = self.client.add_ci_relation(book["_id"], rank["_id"])
        global CR_ID
        CR_ID = resp.cr_id
        print("add result", resp)

    def test_get_cli_relation(self):
        book = self.find_ci(q="_type:book,book_id:1")
        resp = self.client.get_ci_relation(root_id=book["_id"]).result
        print("get result", resp)

    def test_delete(self):
        global CR_ID
        print(CR_ID)
        resp = self.client.delete_ci_relation(cr_id=CR_ID)
        print("delete result", resp)
