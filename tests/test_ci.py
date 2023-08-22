"""
suppose a ci model is Book(id, book_id, book_name, auther)
"""

import os

from cmdb.core.ci import CIClient, Option


class TestCI:

    def setup_method(self) -> None:
        opt = Option(
            os.environ["CMDB_HOST"],
            os.environ["CMDB_KEY"],
            os.environ["CMDB_SECRET"],
        )
        self.client = CIClient(opt=opt)

    def test_get(self):
        resp = self.client.get_ci(q="_type:book").result
        print("get")
        print(resp)

    def find_by_name(self, book_name: str):
        q = f"_type:book,book_name:{book_name}"
        resp = self.client.get_ci(q=q).result
        if not resp:
            return
        return resp[0]

    def test_add(self):
        ci = {
            "id": 1,
            "book_id": 1,
            "book_name": "平凡的世界",
            "auther": "路遥",
        }
        if self.find_by_name("平凡的世界"):
            return
        resp = self.client.add_ci("book", ci)
        print("add")
        print(resp)

    def test_update(self):
        ci = self.find_by_name("平凡的世界")
        resp = self.client.update_ci("book", ci_id=ci["_id"], attrs={"auther": "yao.lu"})
        print("update")
        print(resp)

    def test_delete(self):
        ci = self.find_by_name("平凡的世界")
        resp = self.client.delete_ci(ci["_id"])
        print("delete")
        print(resp)