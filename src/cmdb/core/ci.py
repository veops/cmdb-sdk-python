from urllib.parse import urlparse
from typing import Optional

import requests

from cmdb.core.auth import build_api_key
from cmdb.core.models import *
from cmdb.core.policy import RetKey
from cmdb.core.exc import CMDBError


class CIClient:
    """
    CMDB CI object handle client

    Attributes:
        opt: initialize arugument, if None input, will initiallize with enviroment arguments

    Example:

        1. initialize with arguments

            > opt = Option(url="https://yourhost.com/api/v0.1", key=your_key, secret=your_secret)

            > client = CIClient(opt)

        2. initialize with enviorment arguments
        
            > client = CIClient()

    """

    def __init__(self, opt: Optional[Option] = None):
        self.opt = opt if opt else Option()
        self.session = requests.Session()
        self.url = f"{self.opt.url}/ci"

    def _build_api_key(self, url: str, payload: dict) -> dict:
        return build_api_key(self.opt.key, self.opt.secret, urlparse(url).path, payload)
    
    def _check_err(self, resp: dict):
        msg = resp.get("message")
        if msg:
            raise CMDBError(msg)
    
    def _add_ci(self, params: CICreateReq) -> CICreateRsp:
        url = self.url
        payload = self._build_api_key(url, params.to_params())
        resp = self.session.post(url, json=payload).json()
        self._check_err(resp)
        return CICreateRsp(**resp)

    def _get_ci(self, params: CIRetrieveReq) -> CIRetrieveRsp:
        url = f"{self.url}/s"
        payload = params.to_params()
        payload = self._build_api_key(url, payload)
        resp = self.session.get(url, params=payload).json()
        self._check_err(resp)
        return CIRetrieveRsp(**resp)
    
    def _update_ci(self, ci_id: Optional[int], params: CIUpdateReq) -> CIUpdateRsp:
        if ci_id:
            url = f"{self.url}/{ci_id}"
        else:
            if not params.unique_key.keys():
                raise CMDBError("if not use ci_id, unique key must in request params")
            url = self.opt.url
        payload = self._build_api_key(url, params.to_params())
        resp = self.session.put(url, json=payload).json()
        self._check_err(resp)
        return CIUpdateRsp(**resp)
    
    def _delete_ci(self, params: CIDeleteReq) -> CIDeleteRsp:
        url = f"{self.url}/{params.ci_id}"
        payload = self._build_api_key(url, {})
        resp = self.session.delete(url, json=payload).json()
        return CIDeleteRsp(**resp)
    
    def add_ci(
            self,
            ci_type: str,
            attrs: dict,
            no_attribute_policy: NoAttributePolicy = NoAttributePolicy.default(),
            exist_policy: ExistPolicy = ExistPolicy.default(),
        ) -> CICreateRsp:
        """
        create new ci instance

        eg: suppose a ci model with fields [id, name, age], and its ci_type is "Human"

            > client.add_ci("Human", {"id": 1, "name": "a", "age": 10})

        Args:
            ci_type: ci model type
            attrs: fields of ci to add
            no_attribute_policy: default to ignore not existed attributes update operation, optional value include IGNORE|REJECT
            exist_policy: default to reject add new ci if exists, optional value include NEED|REJECT|REPLACE

        Retrurns:
            CMDB create operation result
        """
        param = CICreateReq(ci_type, no_attribute_policy, exist_policy, attrs)
        return self._add_ci(param)
    
    def get_ci(
            self, 
            q: str, 
            fl: Optional[str] = None,
            facet: Optional[str] = None,
            count: int = 25,
            page: int = 1,
            sort: Optional[str] = None,
            ret_key: RetKey = RetKey.default(),
        ) -> CIRetrieveRsp:
        """
        get ci instance

        get target results by search expression
        for more information, please refrence to veops cmdb guidance [here](https://github.com/veops/cmdb/blob/master/docs/cmdb_api.md).

        Args:
            q: search expression, may looks like "_type:Human,name:a"
            fl: ret attrubute, split by comma
            facet: staticstics
            count: ci count per page
            page: target page num
            sort: sort by target attribute, use `-attr` for descending
            ret_key: ret field name, optional values include ID|NAME|ALIAS

        Returns:
            target ci results
        """
        params = CIRetrieveReq(q, fl, facet, count, page, sort, ret_key)
        return self._get_ci(params)
    
    def update_ci(
            self,
            ci_type: str,
            *,
            ci_id: Optional[int] = None,
            attrs: Optional[dict] = None,
            no_attribute_policy: NoAttributePolicy = NoAttributePolicy.default(),
            **kwargs,
        ) -> CIUpdateRsp:
        """
        update ci attrs

        eg: suppose a ci model with fields [id, name, age], and its ci_type is "Human"
        a ci is ci(id=1, name="a", age=10)
        update operation may like:

            > client.update_ci("Human", ci_id=1, attrs={"age": 11})

            or

            > client.update_ci("Human", attrs={"age": 11}, name="a")  # in this case, name must be unique in ci model

        Args:
            ci_type: ci model type
            ci_id: keyword agument only, the id of ci
            attrs: keyword agument only, fields to update
            no_attribute_policy: default to ignore not existed attributes update operation, optional value include IGNORE|REJECT

        Retrurns:
            CMDB update operation result
        """
        param = CIUpdateReq(ci_type, no_attribute_policy, attrs or {})
        if not ci_id:
            param.unique_key = kwargs
        return self._update_ci(ci_id, param)
    
    def delete_ci(self, ci_id: int) -> CIDeleteRsp:
        """
        delete a ci by its ci_id

        eg: suppose a ci model with fields [id, name, age], and its ci_type is "Human"
        a ci is ci(id=1, name="a", age=10)
        delete operation may like:
        
            > client.delete(1)

        Args:
            ci_id: ci id for the ci want to delete
        
        Retrurns:
            CMDB delete operation result
        """
        param = CIDeleteReq(ci_id)
        return self._delete_ci(param)
