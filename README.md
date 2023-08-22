# CMDB sdk for Python

[中文](README_cn.md) / [English](READMEn.md)

## build

build and install

```shell
> git clone https://github.com/veops/cmdb-sdk-python.git
> cd cmdb-sdk-python

> pip install build wheel setuptools  # requirements
> python -m build -n
```

**veops_cmdb-0.0.1-py3-none-any.whl** will be created at *cmdb-sdk-python/dist/*

## tests

before running tests, please make sure you have created the ci model book and rank,
them may looks like:

```plain
book
    id: int, unique
    book_id: int, unique, not null
    book_name: string, not null,
    author: string

rank:
    id: int, unique
    rank_id: int, unique, not null
    rank: int, not null,
```

and you alse need to form relationship bewteen book and rank, and then you can run tests.

```shell
> pytest -s
```

## usage

If you can ensure the security of your account, you can set the following parameters to environment variables,
this way, you won't need to manually pass the initial parameters every time to set up the client.

```plain
CMDB_HOST=[your host]
CMDB_KEY=[your_key]
CMDB_SECRET=[your secret]
```

### 1.CI

```python3
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

```

### 2.CIRelation

```python3
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
        # self.add_ci()
    
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

```

## examples

for full usage examples, please visit [exmaples](./exmaples/) .
