from typing import Optional

from cmdb.core.ci import CIClient
from cmdb.core.ci_relations import CIRelationClient
from cmdb.core.models import *


class Client:
    """
    CMDB handle client

    Attributes:
        opt: initialize arugument, if None input, will initiallize with enviroment arguments

    Example:

        1. initialize with arguments

            > opt = Option(url="https://yourhost.com/api/v0.1", key=your_key, secret=your_secret)

            > client = Client(opt)

        2. initialize with enviorment arguments
        
            > client = Client()

    """

    def __init__(self, opt: Optional[Option] = None):
        self.ci = CIClient(opt)
        self.cr = CIRelationClient(opt)

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
        return self.ci.add_ci(ci_type, attrs, no_attribute_policy, exist_policy)
    
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
        for more information, please reference to veops cmdb guidance [here](https://github.com/veops/cmdb/blob/master/docs/cmdb_api.md).

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
        return self.ci.get_ci(q, fl, facet, count, page, sort, ret_key)
    
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
        return self.ci.update_ci(ci_type, ci_id=ci_id, attrs=attrs, no_attribute_policy=no_attribute_policy, **kwargs)
    
    def delete_ci(self, ci_id: int) -> CIDeleteRsp:
        """
        delete a ci by its ci_id

        eg: suppose a ci model with fields [id, name, age], and its ci_type is "Human"
        a ci is ci(id=1, name="a", age=10)
        delete operation may like:
            > client.delete(1)

        Args:
            ci_id: ci id for the ci to delete
        
        Retrurns:
            CMDB delete operation result
        """
        return self.ci.delete_ci(ci_id)
    
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
        return self.cr.add_ci_relation(src_ci_id, dst_ci_id)
    
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
        for more information, please refrence to veops cmdb guidance [here](https://github.com/veops/cmdb/blob/master/docs/cmdb_api.md).

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
        return self.cr.get_ci_relation(root_id, level, reverse, q, fl, facet, count, page, sort, ret_key)
    
    def delete_ci_relation(
            self,
            *,
            cr_id: Optional[int] = None,
            src_ci_id: Optional[int] = None,
            dst_ci_id: Optional[int] = None,
    ) -> CIRelationDeleteRsp:
        """
        to delete the cr, either the cr_id or a combination of dst_ci_id and src_ci_id can be used

        example:

            1. delete by cr_id

                > client.delete_ci_relation(cr_id=1)

            2. delete by src_ci_id and dst_ci_id

                > client.delete_ci_relation(src_ci_id=1, dst_ci_id=2)

        Args:
            cr_id: cr id for the ci_relation want to delete
            src_ci_id: id of source ci
            src_ci_id: id of destination ci

        Retrurns:
            CMDB delete operation result
        """
        return self.cr.delete_ci_relation(cr_id=cr_id, src_ci_id=src_ci_id, dst_ci_id=dst_ci_id)


def get_client(opt: Optional[Option] = None) -> Client:
    """
    get CMDB handle client for ci and ci_relation

    Args:
        opt: option for client, if not support, get required info from enviroment
    """
    return Client(opt)
