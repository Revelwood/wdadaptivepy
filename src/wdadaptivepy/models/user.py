"""wdadaptivepy model for Adaptive's Users."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import ClassVar

from wdadaptivepy.models.base import (
    Metadata,
    bool_or_none,
    bool_to_str_one_zero,
    bool_to_str_true_false,
    datetime_or_none,
    datetime_to_str,
    int_list_or_none,
    int_list_to_str,
    int_or_none,
    int_to_str,
    nullable_int_or_none,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
class Subscription(Metadata):
    """wdadaptivepy model for Adaptive's Subscriptions.

    Attributes:
        no_subscriptions: Adaptive Subscription No Subscriptions
        sysem_alerts_and_updates: Adaptive Subscription System Alerts and Updates
        customer_news_letter: Adaptive Subscription Custom News Letter
        local_event: Adaptive Subscription Local Event
        education_training: Adaptive Subscription Education Training
        customer_webinars: Adaptive Subscription Customer Webinars
        new_products_and_enhancements: Adaptive Subscription New Products / Enhancements
        partner_news_letter: Adaptive Subscription Partner News Letter
        partner_webinars: Adaptive Subscription Partner Webinars
        user_groups: Adaptive Subscription User Groups
        surveys: Adaptive Subscription Surveys
        __xml_tags: wdadaptivepy XML tags

    """

    no_subscriptions: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "noSubscriptions",
            "xml_read": "noSubscriptions",
            "xml_update": "noSubscriptions",
            "xml_delete": "noSubscriptions",
        },
    )
    sysem_alerts_and_updates: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "systemAlertsAndUpdates",
            "xml_read": "systemAlertsAndUpdates",
            "xml_update": "systemAlertsAndUpdates",
            "xml_delete": "systemAlertsAndUpdates",
        },
    )
    customer_news_letter: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "customerNewsLetter",
            "xml_read": "customerNewsLetter",
            "xml_update": "customerNewsLetter",
            "xml_delete": "customerNewsLetter",
        },
    )
    local_event: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "localEvent",
            "xml_read": "localEvent",
            "xml_update": "localEvent",
            "xml_delete": "localEvent",
        },
    )
    education_training: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "educationTraining",
            "xml_read": "educationTraining",
            "xml_update": "educationTraining",
            "xml_delete": "educationTraining",
        },
    )
    customer_webinars: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "customerWebinars",
            "xml_read": "customerWebinars",
            "xml_update": "customerWebinars",
            "xml_delete": "customerWebinars",
        },
    )
    new_products_and_enhancements: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "newProductsAndEnhancements",
            "xml_read": "newProductsAndEnhancements",
            "xml_update": "newProductsAndEnhancements",
            "xml_delete": "newProductsAndEnhancements",
        },
    )
    partner_news_letter: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "partnerNewsLetter",
            "xml_read": "partnerNewsLetter",
            "xml_update": "partnerNewsLetter",
            "xml_delete": "partnerNewsLetter",
        },
    )
    partner_webinars: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "partnerWebinars",
            "xml_read": "partnerWebinars",
            "xml_update": "partnerWebinars",
            "xml_delete": "partnerWebinars",
        },
    )
    user_groups: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "userGroups",
            "xml_read": "userGroups",
            "xml_update": "userGroups",
            "xml_delete": "userGroups",
        },
    )
    surveys: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "surveys",
            "xml_read": "surveys",
            "xml_update": "surveys",
            "xml_delete": "surveys",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "subscriptions",
        "xml_create_tag": "subscription",
        "xml_create_children": {},
        "xml_read_parent_tag": "subscriptions",
        "xml_read_tag": "subscription",
        "xml_read_children": {},
        "xml_update_parent_tag": "subscriptions",
        "xml_update_tag": "subscription",
        "xml_update_children": {},
        "xml_delete_parent_tag": "subscriptions",
        "xml_delete_tag": "subscription",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class User(Metadata):
    """wdadaptivepy model for Adaptive's Users.

    Attributes:
        id: Adaptive User ID
        guid: Adaptive User GUID
        login: Adaptive User Login
        email: Adaptive User Email
        name: Adaptive User Name
        position: Adaptive User Position
        permission_set_ids: Adaptive User Permission Set IDs
        alternate_email: Adaptive User Alternate Email
        saml_fed_id: Adaptive User SAML Federation ID
        time_zone: Adaptive User Time Zone
        homepage: Adaptive User Homepage
        country: Adaptive User Country
        us_state: Adaptive User US State
        perspective: Adaptive User Perspective
        perspective_name: Adaptive User Perspective Name
        dashboard: Adaptive User Dashboard
        dashboard_name:Adaptive User Dashboard Name
        netsuite_login: Adaptive User NetSuite Login
        salesforce_login: Adaptive User Salesforce Login
        created_date: Adaptive User Created Date
        last_login: Adaptive User Last Login
        failed_attempts: Adaptive User Failed Attempts
        locked: Adaptive User Locked
        subscriptions: Adaptive User Subscriptions
        __xml_tags: wdadaptivepy XML tags

    """

    id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "",
            "xml_read": "id",
            "xml_update": "id",
            "xml_delete": "id",
        },
    )
    guid: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "guid",
            "xml_read": "guid",
            "xml_update": "guid",
            "xml_delete": "guid",
        },
    )
    login: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "login",
            "xml_read": "login",
            "xml_update": "login",
            "xml_delete": "login",
        },
    )
    email: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "email",
            "xml_read": "email",
            "xml_update": "email",
            "xml_delete": "email",
        },
    )
    name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "name",
            "xml_read": "name",
            "xml_update": "name",
            "xml_delete": "name",
        },
    )
    position: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "position",
            "xml_read": "position",
            "xml_update": "position",
            "xml_delete": "position",
        },
    )
    permission_set_ids: list[int] | None = field(
        default=None,
        metadata={
            "validator": int_list_or_none,
            "xml_parser": int_list_to_str,
            "xml_create": "permissionSetIds",
            "xml_read": "permissionSetIds",
            "xml_update": "permissionSetIds",
            "xml_delete": "permissionSetIds",
        },
    )
    alternate_email: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "alternateEmail",
            "xml_read": "alternateEmail",
            "xml_update": "alternateEmail",
            "xml_delete": "alternateEmail",
        },
    )
    saml_fed_id: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "samlFedId",
            "xml_read": "samlFedId",
            "xml_update": "samlFedId",
            "xml_delete": "samlFedId",
        },
    )
    time_zone: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "timeZone",
            "xml_read": "timeZone",
            "xml_update": "timeZone",
            "xml_delete": "timeZone",
        },
    )
    homepage: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "homepage",
            "xml_read": "homepage",
            "xml_update": "homepage",
            "xml_delete": "homepage",
        },
    )
    country: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "country",
            "xml_read": "country",
            "xml_update": "country",
            "xml_delete": "country",
        },
    )
    us_state: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "usState",
            "xml_read": "usState",
            "xml_update": "usState",
            "xml_delete": "usState",
        },
    )
    perspective: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "perspective",
            "xml_read": "perspective",
            "xml_update": "perspective",
            "xml_delete": "perspective",
        },
    )
    perspective_name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "perspectiveName",
            "xml_read": "perspectiveName",
            "xml_update": "perspectiveName",
            "xml_delete": "perspectiveName",
        },
    )
    dashboard: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "dashboard",
            "xml_read": "dashboard",
            "xml_update": "dashboard",
            "xml_delete": "dashboard",
        },
    )
    dashboard_name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "dashboardName",
            "xml_read": "dashboardName",
            "xml_update": "dashboardName",
            "xml_delete": "dashboardName",
        },
    )
    netsuite_login: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "netsuiteLogin",
            "xml_read": "netsuiteLogin",
            "xml_update": "netsuiteLogin",
            "xml_delete": "netsuiteLogin",
        },
    )
    salesforce_login: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "salesforceLogin",
            "xml_read": "salesforceLogin",
            "xml_update": "salesforceLogin",
            "xml_delete": "salesforceLogin",
        },
    )
    created_date: datetime | None = field(
        default=None,
        metadata={
            "validator": datetime_or_none,
            "xml_parser": datetime_to_str,
            "xml_create": "createdDate",
            "xml_read": "createdDate",
            "xml_update": "createdDate",
            "xml_delete": "createdDate",
        },
    )
    last_login: datetime | None = field(
        default=None,
        metadata={
            "validator": datetime_or_none,
            "xml_parser": datetime_to_str,
            "xml_create": "lastLogin",
            "xml_read": "lastLogin",
            "xml_update": "lastLogin",
            "xml_delete": "lastLogin",
        },
    )
    failed_attempts: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "failedAttempts",
            "xml_read": "failedAttempts",
            "xml_update": "failedAttempts",
            "xml_delete": "failedAttempts",
        },
    )
    locked: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_true_false,
            "xml_create": "locked",
            "xml_read": "locked",
            "xml_update": "locked",
            "xml_delete": "locked",
        },
    )
    subscriptions: Subscription | None = field(
        default=None,
        metadata={
            # "validator": ,
            # "xml_parser": ,
            "xml_create": "subscriptions",
            "xml_read": "subscriptions",
            "xml_update": "subscriptions",
            "xml_delete": "subscriptions",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "users",
        "xml_create_tag": "user",
        "xml_create_children": {"subscriptions": Subscription},
        "xml_read_parent_tag": "users",
        "xml_read_tag": "user",
        "xml_read_children": {"subscriptions": Subscription},
        "xml_update_parent_tag": "users",
        "xml_update_tag": "user",
        "xml_update_children": {"subscriptions": Subscription},
        "xml_delete_parent_tag": "users",
        "xml_delete_tag": "user",
        "xml_delete_children": {"subscriptions": Subscription},
    }
