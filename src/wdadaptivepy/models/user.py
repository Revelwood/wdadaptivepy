"""wdadaptivepy model for Adaptive's Users."""

from datetime import datetime
from functools import partial
from typing import Annotated, ClassVar

from pydantic import AfterValidator, BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    Metadata,
)
from wdadaptivepy.utils.parsers import (
    bool_to_str_one_zero,
    bool_to_str_true_false,
    datetime_to_str,
    int_list_to_str,
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    bool_or_none,
    custom_type_or_none,
    datetime_tz_or_none,
    int_list_or_none,
    int_or_none,
    nullable_int_or_none,
    str_or_none,
)


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

    """

    no_subscriptions: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="nosubscriptions",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    sysem_alerts_and_updates: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="systemAlertsAndUpdates",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    customer_news_letter: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="customerNewsLetter",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    local_events: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="localEvents",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    education_training: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="educationTraining",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    customer_webinars: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="customerWebinars",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    new_products_and_enhancements: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="newProductsAndEnhancements",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    partner_news_letter: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="partnerNewsLetter",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    partner_webinars: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="partnerWebinars",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    user_groups: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="userGroups",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    surveys: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="surveys",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="subscriptions",
            default_tag="subscriptions",
        )
    ]


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
        group_ids: Adaptive User Group IDs
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

    """

    id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="id",
                    create_tag="",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    guid: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="guid",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    login: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="login",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    email: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="email",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="name",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    position: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="position",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    permission_set_ids: Annotated[
        list[int] | None,
        BeforeValidator(int_list_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="permissionSetIds",
                    serializer=int_list_to_str,
                )
            ]
        ),
    ] = None
    group_ids: Annotated[
        list[int] | None,
        BeforeValidator(int_list_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="groupIds",
                    serializer=int_list_to_str,
                )
            ]
        ),
    ] = None
    alternate_email: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="alternateEmail",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    saml_fed_id: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="samlFedId",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    time_zone: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="timeZone",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    homepage: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="homepage",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    country: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="country",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    us_state: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="usState",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    perspective: Annotated[
        str | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="perspective",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    perspective_name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="perspectiveName",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    dashboard: Annotated[
        str | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="dashboard",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    dashboard_name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="dashboardName",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    netsuite_login: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="netsuiteLogin",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    salesforce_login: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="salesforceLogin",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    created_date: Annotated[
        datetime | None,
        AfterValidator(datetime_tz_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="createdDate",
                    serializer=datetime_to_str,
                )
            ]
        ),
    ] = None
    last_login: Annotated[
        datetime | None,
        AfterValidator(datetime_tz_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="lastLogin",
                    serializer=datetime_to_str,
                )
            ]
        ),
    ] = None
    failed_attempts: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="failedAttempts",
                    serializer=int_to_str,
                )
            ]
        ),
    ] = None
    locked: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="locked",
                    serializer=bool_to_str_true_false,
                )
            ]
        ),
    ] = None
    subscriptions: Annotated[
        Subscription | None,
        BeforeValidator(partial(custom_type_or_none, data_type=Subscription)),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="subscriptions",
                    serializer=None,
                )
            ]
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="users",
            default_tag="user",
            default_children={"subscriptions": Subscription},
        )
    ]
