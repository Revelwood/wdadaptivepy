"""wdadaptivepy model for Adaptive's Accounts."""

from dataclasses import dataclass, field
from typing import ClassVar

from wdadaptivepy.models.base import (
    HierarchialAttributedMetadata,
    bool_or_none,
    bool_to_str_one_zero,
    int_or_none,
    int_to_str,
    nullable_int_or_none,
    str_or_none,
    str_to_str,
)


@dataclass(eq=False)
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
        __xml_tags: wdadaptivepy Account XML tags

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
    code: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "code",
            "xml_read": "code",
            "xml_update": "code",
            "xml_delete": "code",
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
    account_type_code: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "accountTypeCode",
            "xml_read": "accountTypeCode",
            "xml_update": "accountTypeCode",
            "xml_delete": "accountTypeCode",
        },
    )
    description: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "description",
            "xml_read": "description",
            "xml_update": "description",
            "xml_delete": "description",
        },
    )
    short_name: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "shortName",
            "xml_read": "shortName",
            "xml_update": "shortName",
            "xml_delete": "shortName",
        },
    )
    time_stratum: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "timeStratum",
            "xml_read": "timeStratum",
            "xml_update": "timeStratum",
            "xml_delete": "timeStratum",
        },
    )
    display_as: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "displayAs",
            "xml_read": "displayAs",
            "xml_update": "displayAs",
            "xml_delete": "displayAs",
        },
    )
    is_assumption: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isAssumption",
            "xml_read": "isAssumption",
            "xml_update": "isAssumption",
            "xml_delete": "isAssumption",
        },
    )
    suppress_zeroes: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "suppressZeroes",
            "xml_read": "suppressZeroes",
            "xml_update": "suppressZeroes",
            "xml_delete": "suppressZeroes",
        },
    )
    is_default_root: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isDefaultRoot",
            "xml_read": "isDefaultRoot",
            "xml_update": "isDefaultRoot",
            "xml_delete": "isDefaultRoot",
        },
    )
    decimal_precision: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "decimalPrecision",
            "xml_read": "decimalPrecision",
            "xml_update": "decimalPrecision",
            "xml_delete": "decimalPrecision",
        },
    )
    plan_by: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "planBy",
            "xml_read": "planBy",
            "xml_update": "planBy",
            "xml_delete": "planBy",
        },
    )
    exchange_rate_type: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "exchangeRateType",
            "xml_read": "exchangeRateType",
            "xml_update": "exchangeRateType",
            "xml_delete": "exchangeRateType",
        },
    )
    is_importable: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isImportable",
            "xml_read": "isImportable",
            "xml_update": "isImportable",
            "xml_delete": "isImportable",
        },
    )
    balance_type: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "balanceType",
            "xml_read": "balanceType",
            "xml_update": "balanceType",
            "xml_delete": "balanceType",
        },
    )
    data_entry_type: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "dataEntryType",
            "xml_read": "dataEntryType",
            "xml_update": "dataEntryType",
            "xml_delete": "dataEntryType",
        },
    )
    time_roll_up: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "timeRollUp",
            "xml_read": "timeRollUp",
            "xml_update": "timeRollUp",
            "xml_delete": "timeRollUp",
        },
    )
    time_weight_acct_id: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "timeWeightAcctId",
            "xml_read": "timeWeightAcctId",
            "xml_update": "timeWeightAcctId",
            "xml_delete": "timeWeightAcctId",
        },
    )
    has_salary_detail: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "hasSalaryDetail",
            "xml_read": "hasSalaryDetail",
            "xml_update": "hasSalaryDetail",
            "xml_delete": "hasSalaryDetail",
        },
    )
    data_privacy: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "dataPrivacy",
            "xml_read": "dataPrivacy",
            "xml_update": "dataPrivacy",
            "xml_delete": "dataPrivacy",
        },
    )
    sub_type: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "subType",
            "xml_read": "subType",
            "xml_update": "subType",
            "xml_delete": "subType",
        },
    )
    start_expanded: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "startExpanded",
            "xml_read": "startExpanded",
            "xml_update": "startExpanded",
            "xml_delete": "startExpanded",
        },
    )
    is_breakback_eligible: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isBreakbackEligible",
            "xml_read": "isBreakbackEligible",
            "xml_update": "isBreakbackEligible",
            "xml_delete": "isBreakbackEligible",
        },
    )
    level_dim_rollup: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "levelDimRollup",
            "xml_read": "levelDimRollup",
            "xml_update": "levelDimRollup",
            "xml_delete": "levelDimRollup",
        },
    )
    rollup_text: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "rollupText",
            "xml_read": "rollupText",
            "xml_update": "rollupText",
            "xml_delete": "rollupText",
        },
    )
    enable_actuals: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "enableActuals",
            "xml_read": "enableActuals",
            "xml_update": "enableActuals",
            "xml_delete": "enableActuals",
        },
    )
    is_group: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isGroup",
            "xml_read": "isGroup",
            "xml_update": "isGroup",
            "xml_delete": "isGroup",
        },
    )
    is_intercompany: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isIntercompany",
            "xml_read": "isIntercompany",
            "xml_update": "isIntercompany",
            "xml_delete": "isIntercompany",
        },
    )
    formula: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "formula",
            "xml_read": "formula",
            "xml_update": "formula",
            "xml_delete": "formula",
        },
    )
    is_linked: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isLinked",
            "xml_read": "isLinked",
            "xml_update": "isLinked",
            "xml_delete": "isLinked",
        },
    )
    is_system: bool | None = field(
        default=None,
        metadata={
            "validator": bool_or_none,
            "xml_parser": bool_to_str_one_zero,
            "xml_create": "isSystem",
            "xml_read": "isSystem",
            "xml_update": "isSystem",
            "xml_delete": "isSystem",
        },
    )
    owning_sheet_id: str | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": str_to_str,
            "xml_create": "owningSheetId",
            "xml_read": "owningSheetId",
            "xml_update": "owningSheetId",
            "xml_delete": "owningSheetId",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "accounts",
        "xml_create_tag": "account",
        "xml_create_children": {},
        "xml_read_parent_tag": "accounts",
        "xml_read_tag": "account",
        "xml_read_children": {},
        "xml_update_parent_tag": "accounts",
        "xml_update_tag": "account",
        "xml_update_children": {},
        "xml_delete_parent_tag": "accounts",
        "xml_delete_tag": "account",
        "xml_delete_children": {},
    }
