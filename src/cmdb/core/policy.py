from enum import Enum


class RetKey(Enum):
    ID = "id"
    NAME = "name"
    ALIAS = "alias"

    @staticmethod
    def default() -> "RetKey":
        """
        defalut ret key
        """
        return RetKey.NAME


class NoAttributePolicy(Enum):
    REJECT = "reject"
    IGNORE = "ignore"

    @staticmethod
    def default() -> "NoAttributePolicy":
        """
        defalut no_attribute_policy
        """
        return NoAttributePolicy.IGNORE


class ExistPolicy(Enum):
    NEED = "need"
    REJECT = "reject"
    REPLACE = "replace"

    @staticmethod
    def default() -> "ExistPolicy":
        """
        defalut exist_policy
        """
        return ExistPolicy.REJECT
