# CMDB sdk for Python

[English](READMEn.md) / [中文](README_cn.md)

CMDB python客户端工具

```shell
> from cmdb import get_client
> cli = get_client()
> books = cli.get_ci(q="_type:book")
```

## 编译

以下为编译和安装脚本，编译前需要安装依赖*build*、*wheel*和*setuptools*

```shell
# 克隆源码
> git clone https://github.com/veops/cmdb-sdk-python.git
> cd cmdb-sdk-python

# 安装依赖
> pip install build wheel setuptools  # requirements

# 打包wheel -n指不在独立的虚拟环境中编译
> python -m build -n
```

**veops_cmdb-0.0.1-py3-none-any.whl** 将会在 *cmdb-sdk-python/dist/*目录创建，使用pip安装即可

## 测试

在测试代码之前，需要正在CMDB中创建如下两个CI模型:

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

然后你需要为book和rank创建关联关系，一切准备就绪后，使用如下代码来执行测试：

```shell
> pytest -s
```

## 使用

Client初始化需要传入配置参数，配置参数封装在`Option`类中，主要包含 __url__、__key__ 和 __secret__ 参数，如果你能保证当前环境为个人使用的安全环境，也可以直接将上述信息加入环境变量，这样可以省去每次初始化的参数传入

```plain
CMDB_HOST=[your host]
CMDB_KEY=[your_key]
CMDB_SECRET=[your secret]
```

### 1.CI

```python3
"""
suppose a ci model is Book(id, book_id, book_name, author)
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
            "author": "路遥",
        }
        if self.find_by_name("平凡的世界"):
            return
        resp = self.client.add_ci("book", ci)
        print("add")
        print(resp)

    def test_update(self):
        ci = self.find_by_name("平凡的世界")
        resp = self.client.update_ci("book", ci_id=ci["_id"], attrs={"author": "yao.lu"})
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
suppose a CI model book with field id, name and author,
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
            os.environ["XDATA_KEY"],
            os.environ["XDATA_SECRET"],
        )
        self.ci_client = CIClient(opt=opt)
        self.client = CIRelationClient(opt=opt)
        # self.add_ci()
    
    def add_ci(self):
        book = {
            "id": 1,
            "book_id": 1,
            "book_name": "平凡的世界",
            "author": "路遥",
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

完整示例代码可以访问[exmaples](./exmaples/)查看.
