"""wdadaptivepy model for Adaptive's Accounts."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    HierarchialAttributedMetadata,
)
from wdadaptivepy.utils.parsers import (
    bool_to_str_one_zero,
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    bool_or_none,
    int_or_none,
    nullable_int_or_none,
    str_or_none,
)


class Account(HierarchialAttributedMetadata):
    """wdadaptivepy model for Adaptive's Accounts.

    Attributes:
        id: Adaptive Account ID
        code: Adaptive Account Code
        name: Adaptive Account Name
        account_type_code: Adaptive Account Type Code
        description: Adaptive Account Description
        short_name: Adaptive Account Short Name
        time_stratum: Adaptive Account Time Stratum
        display_as: Adaptive Account Dispay As
        is_assumption: Adaptive Account Is Assumption
        suppress_zeroes: Adaptive Account Suprress Zeroes
        is_default_root: Adaptive Account Is Default Root
        decimal_precision: Adaptive Account Decimal Precision
        plan_by: Adaptive Account Plan By
        exchange_rate_type: Adaptive Account Exchange Rate Type
        is_importable: Adaptive Account Is Importable
        balance_type: Adaptive Account Balance Type
        data_entry_type: Adaptive Account Data Entry Type
        time_roll_up: Adaptive Account Time Roll Up
        time_weight_acct_id: Adaptive Account Time Weight Account ID
        has_salary_detail: Adaptive Account Has Salary Detail
        data_privacy: Adaptive Account Data Privacy
        sub_type: Adaptive Account Sub Type
        start_expanded: Adaptive Account Start Expanded
        is_breakback_eligible: Aadaptive Account Is Breakback Eligibile
        level_dim_rollup: Adaptive Account Level Dim Rollup
        rollup_text: Adaptive Account Rollup Text
        enable_actuals: Adaptive Account Enable Actuals
        is_group: Adaptive Account Is Group
        is_intercompany: Adaptive Account Is Intercompany
        formula: Adaptive Account Formula
        is_linked: Adaptive Account Is Linked
        is_system: Adaptive Account Is System
        owning_sheet_id: Adaptive Account Owning Sheet ID
        _xml_tags: wdadaptivepy Account XML tags

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
    code: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="code",
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
    account_type_code: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="accountTypeCode",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    description: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="description",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    short_name: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="shortName",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    time_stratum: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="timeStratum",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    display_as: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="displayAs",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_assumption: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isAssumption",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    suppress_zeroes: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="suppressZeroes",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_default_root: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isDefaultRoot",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    decimal_precision: Annotated[
        str | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="decimalPrecision",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    plan_by: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="planBy",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    exchange_rate_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="exchangeRateType",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_importable: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isImportable",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    balance_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="balanceType",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    data_entry_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="dataEntryType",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    time_roll_up: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="timeRollUp",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    time_weight_acct_id: Annotated[
        str | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="timeWeightAcctId",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    has_salary_detail: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="hasSalaryDetail",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    data_privacy: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="dataPrivacy",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    sub_type: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="subType",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    start_expanded: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="startExpanded",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_breakback_eligible: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isBreakbackEligible",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    level_dim_rollup: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="levelDimRollup",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    rollup_text: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="rollupText",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    enable_actuals: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="enableActuals",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_group: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isGroup",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_intercompany: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isIntercompany",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    formula: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="formula",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    is_linked: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isLinked",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    is_system: Annotated[
        bool | None,
        BeforeValidator(bool_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="isSystem",
                    serializer=bool_to_str_one_zero,
                )
            ]
        ),
    ] = None
    owning_sheet_id: Annotated[
        str | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="owningSheetId",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="accounts",
            default_tag="account",
        )
    ]
