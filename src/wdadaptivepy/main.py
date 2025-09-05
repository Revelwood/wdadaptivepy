"""wdadaptivepy main entry."""

from dataclasses import dataclass
from typing import Any

from wdadaptivepy.connectors.xml_api.constants import (
    DEFAULT_CALLER_NAME,
    MINIMUM_VERSION,
)
from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.services.accounts import AccountService
from wdadaptivepy.services.attribute_values import AttributeValueService
from wdadaptivepy.services.attributes import AttributeService
from wdadaptivepy.services.currencies import CurrencyService
from wdadaptivepy.services.data import DataService
from wdadaptivepy.services.dimension_values import DimensionValueService
from wdadaptivepy.services.dimensions import DimensionService
from wdadaptivepy.services.groups import GroupService
from wdadaptivepy.services.levels import LevelService
from wdadaptivepy.services.permission_sets import PermissionSetService
from wdadaptivepy.services.time import TimeService
from wdadaptivepy.services.users import UserService
from wdadaptivepy.services.versions import VersionService


@dataclass
class AdaptiveConnection:
    """wdadaptivepy client for connection to Adaptive.

    Attributes:
        login: Adaptive Login
        password: Adaptive Password
        instance_code: Adaptive Instance Code
        caller_name: Adaptive Caller Name
        locale: Adaptive Locale
        xml_api_version: Adaptive XML API Version
        accounts (AccountService): wdadaptivepy AccountService
        attributes (AttributeService): wdadaptivepy AttributeService
        attribute_values (AttributeValueService): wdadaptivepy AttributeValueService
        currencies (CurrencyService): wdadaptivepy CurrencyService
        data (DataService): wdadaptivepy DataService
        dimensions (DimensionService): wdadaptivepy DimensionService
        dimension_values (DimensionValueService): wdadaptivepy DimensionValueService
        groups (GroupService): wdadaptivepy GroupService
        levels (LevelService): wdadaptivepy LevelService
        permission_sets (PermissionSetService): wdadaptivepy PermissionSetService
        time (TimeService): wdadaptivepy TimeService
        users (UserService): wdadaptivepy UserService
        versions (VersionService): wdadaptivepy VersionService

    """

    login: str
    password: str
    instance_code: str | None = None
    caller_name: str = DEFAULT_CALLER_NAME
    locale: str | None = None
    xml_api_version: int = MINIMUM_VERSION

    def __post_init__(self) -> None:
        """Clean up AdaptiveConnection instance."""
        self.__xml_api = XMLApi(
            login=self.login,
            password=self.password,
            locale=self.locale,
            instance_code=self.instance_code,
            caller_name=self.caller_name,
            version=self.xml_api_version,
        )

        self.accounts = AccountService(xml_api=self.__xml_api)
        self.attributes = AttributeService(xml_api=self.__xml_api)
        self.attribute_values = AttributeValueService(xml_api=self.__xml_api)
        self.currencies = CurrencyService(xml_api=self.__xml_api)
        self.data = DataService(xml_api=self.__xml_api)
        self.dimensions = DimensionService(xml_api=self.__xml_api)
        self.dimension_values = DimensionValueService(xml_api=self.__xml_api)
        self.groups = GroupService(xml_api=self.__xml_api)
        self.levels = LevelService(xml_api=self.__xml_api)
        self.permission_sets = PermissionSetService(xml_api=self.__xml_api)
        self.time = TimeService(xml_api=self.__xml_api)
        self.users = UserService(xml_api=self.__xml_api)
        self.versions = VersionService(xml_api=self.__xml_api)

    def __setattr__(self, name: str, value: Any, /) -> None:  # NOQA: ANN401
        """Force data to appropriate data type.

        Args:
            name: Name of field to modify
            value: Value to modify

        Raises:
            RuntimeError: Unexpected value

        """
        if getattr(self, "_AdaptiveConnection__xml_api", None):
            if getattr(self.__xml_api, name.removeprefix("xml_api_"), None):
                setattr(self.__xml_api, name.removeprefix("xml_api_"), value)
            if getattr(self.__xml_api, name, None):
                setattr(self.__xml_api, name, value)
        super().__setattr__(name, value)
