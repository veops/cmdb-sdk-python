import abc
import dataclasses
import os
from typing import Optional

from cmdb.core.policy import ExistPolicy, NoAttributePolicy, RetKey


class Request(abc.ABC):
    """cmdb request"""
    pass

    @abc.abstractmethod
    def to_params(self) -> dict:
        raise NotImplemented("")
    

class Response(abc.ABC):
    """response of cmdb request"""
    pass


@dataclasses.dataclass
class Option:
    """
    cmdb configure option

    all attributes default initialize with empty str if no argument input,
    and then will check the enviorment arguments
    """
    url: str = ""
    key: str = ""
    secret: str = ""

    def __post_init__(self) -> None:
        if not self.url:
            self.url = os.environ["CMDB_HOST"]
        if not self.key:
            self.key = os.environ["CMDB_KEY"]
        if not self.secret:
            self.secret = os.environ["CMDB_SECRET"]


@dataclasses.dataclass
class CICreateReq(Request):
    """ci create request"""
    ci_type: str
    no_attribute_policy: NoAttributePolicy = NoAttributePolicy.default()
    exist_policy: ExistPolicy = ExistPolicy.default()
    attrs: dict = dataclasses.field(default_factory=dict)

    def to_params(self) -> dict:
        p = {
            "ci_type": self.ci_type,
            "no_attribute_policy": self.no_attribute_policy.value,
            "exist_policy": self.exist_policy.value
        }
        p.update(self.attrs)
        return p
    

@dataclasses.dataclass
class CICreateRsp(Response):
    """response of ci create requet"""
    ci_id: int


@dataclasses.dataclass
class CIRetrieveReq(Request):
    """ci retrieve requet"""
    q: str
    fl: Optional[str] = None
    facet: Optional[str] = None
    count: int = 25
    page: int = 1
    sort: Optional[str] = None
    ret_key: RetKey = RetKey.default()

    def to_params(self) -> dict:
        p = dataclasses.asdict(self)
        p.update({"ret_key": self.ret_key.value})
        return p


@dataclasses.dataclass
class CIRetrieveRsp(Response):
    """response of ci retrieve requet"""
    numfound: int
    total: int
    page: int
    result: list
    facet: dict
    counter: dict


@dataclasses.dataclass
class CIUpdateReq(Request):
    """ci update requet"""
    ci_type: str
    no_attribute_policy: NoAttributePolicy = NoAttributePolicy.default()
    attrs: dict = dataclasses.field(default_factory=dict)
    unique_key: dict = dataclasses.field(default_factory=dict)

    def to_params(self) -> dict:
        p = {
            "ci_type": self.ci_type,
            "no_attribute_policy": self.no_attribute_policy.value,
            "exist_policy": ExistPolicy.REPLACE.value,
            **self.unique_key,
        }
        p.update(self.attrs)
        return p


@dataclasses.dataclass
class CIUpdateRsp(Response):
    """response of ci update requet"""
    ci_id: int
    

@dataclasses.dataclass
class CIDeleteReq(Request):
    """ci delete requet"""
    ci_id: int

    def to_params(self) -> dict:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class CIDeleteRsp(Response):
    """response of ci delete requet"""
    message: str


@dataclasses.dataclass
class CIRelationCreateReq(Request):
    """ci_relation create request"""
    src_ci_id: int
    dst_ci_id: int

    def to_params(self) -> dict:
        return {}


@dataclasses.dataclass
class CIRelationCreateRsp(Response):
    """response of ci_relation create request"""
    cr_id: int


@dataclasses.dataclass
class CIRelationRetrieveReq(Request):
    """ci_relation retrieve request"""
    root_id: int
    level: Optional[str] = None
    reverse: int = 0
    q: Optional[str] = None
    fl: Optional[str] = None
    facet: Optional[str] = None
    count: int = 25
    page: int = 1
    sort: Optional[str] = None
    ret_key: RetKey = RetKey.default()

    def to_params(self) -> dict:
        p = dataclasses.asdict(self)
        p.update({"ret_key": self.ret_key.value})
        return p


@dataclasses.dataclass
class CIRelationRetrieveRsp(Response):
    """response of ci_relation retrieve requet"""
    numfound: int
    total: int
    page: int
    result: list
    facet: dict
    counter: dict
    

@dataclasses.dataclass
class CIRelationDeleteReq(Request):
    """ci_relation delete requet"""
    cr_id: int

    def to_params(self) -> dict:
        return {}


@dataclasses.dataclass
class CIRelationDeleteRsp(Response):
    """response of ci_relation delete requet"""
    message: str