from urllib.parse import urlparse
from typing import Optional

import requests

from cmdb.core.auth import build_api_key
from cmdb.core.models import *
from cmdb.core.policy import RetKey
from cmdb.core.exc import CMDBError


class CIRelationClient:
    """
    CMDB CIRelation Relation object handle client

    Attributes:
        opt: initialize arugument, if None input, will initiallize with enviroment arguments

    Example:

        1. initialize with arguments

            > opt = Option(url="https://yourhost.com/api/v0.1", key=your_key, secret=your_secret)

            > client = CIRelationRelationClient(opt)

        2. initialize with enviorment arguments
        
            > client = CIRelationRelationClient()

    """

    def __init__(self, opt: Optional[Option] = None):
        self.opt = opt if opt else Option()
        self.session = requests.Session()
        self.url = f"{self.opt.url}/ci_relations"

    def _build_api_key(self, url: str, payload: dict) -> dict:
        return build_api_key(self.opt.key, self.opt.secret, urlparse(url).path, payload)
    
    def _check_err(self, resp: dict):
        msg = resp.get("message")
        if msg:
            raise CMDBError(msg)
    
    def _add_ci_relation(self, params: CIRelationCreateReq) -> CIRelationCreateRsp:
        url = f"{self.url}/{params.src_ci_id}/{params.dst_ci_id}"
        payload = self._build_api_key(url, params.to_params())
        resp = self.session.post(url, json=payload).json()
        self._check_err(resp)
        return CIRelationCreateRsp(**resp)

    def _get_ci_relation(self, params: CIRelationRetrieveReq) -> CIRelationRetrieveRsp:
        url = f"{self.url}/s"
        payload = params.to_params()
        payload = self._build_api_key(url, payload)
        resp = self.session.get(url, params=payload).json()
        self._check_err(resp)
        return CIRelationRetrieveRsp(**resp)
    
    def _delete_ci_relation(self, params: CIRelationDeleteReq) -> CIRelationDeleteRsp:
        url = f"{self.url}/{params.cr_id}"
        payload = self._build_api_key(url, params.to_params())
        resp = self.session.delete(url, json=payload).json()
        return CIRelationDeleteRsp(**resp)
    
    def add_ci_relation(
            self,
            src_ci_id: int,
            dst_ci_id: int,
        ) -> CIRelationCreateRsp:
        """
        create new ci_relation instance

        Args:
            src_ci_id: id of source ci
            src_ci_id: id of destination ci

        Retrurns:
            ci_relation create operation result
        """
        param = CIRelationCreateReq(src_ci_id, dst_ci_id)
        return self._add_ci_relation(param)
    
    def get_ci_relation(
            self,
            root_id: int,
            level: Optional[str] = None,
            reverse: int = 0,
            q: Optional[str] = None, 
            fl: Optional[str] = None,
            facet: Optional[str] = None,
            count: int = 25,
            page: int = 1,
            sort: Optional[str] = None,
            ret_key: RetKey = RetKey.default(),
        ) -> CIRelationRetrieveRsp:
        """
        get ci_relation instance

        get target relation by root id
        for more information, please reference to veops cmdb guidance [here](https://github.com/veops/cmdb/blob/master/docs/cmdb_api.md).

        Args:
            root_id: ci id of root node
            level: levels of relationship, split by comma
            reverse: Reverse search or not, 0 for no and 1 for yes, default is 0
            q: search expression, may looks like "_type:Human,name:a"
            fl: ret attrubute, split by comma
            facet: staticstics
            count: ci count per page
            page: target page num
            sort: sort by target attribute, use `-attr` for descending
            ret_key: ret field name, optional values include ID|NAME|ALIAS

        Returns:
            target ci_relation results
        """
        params = CIRelationRetrieveReq(root_id, level, reverse, q, fl, facet, count, page, sort, ret_key)
        return self._get_ci_relation(params)
    
    def delete_ci_relation(self, cr_id: int) -> CIRelationDeleteRsp:
        """
        delete a ci_relation by its cr id

        Args:
            cr_id: cr id for the ci_relation want to delete
        
        Retrurns:
            CMDB delete operation result
        """
        param = CIRelationDeleteReq(cr_id)
        return self._delete_ci_relation(param)
