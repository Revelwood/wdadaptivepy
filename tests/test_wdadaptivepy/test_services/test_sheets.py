"""Tests for wdadaptivepy's service for Adaptive's Sheets."""

# Code using pytest-mock
from unittest.mock import MagicMock
from xml.etree import ElementTree as ET

import pytest
from pytest_mock import MockerFixture

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models import (
    ColumnValue,
    CubeSheet,
    CubeSheetAccount,
    CubeSheetAccounts,
    CubeSheetAttribute,
    CubeSheetDimension,
    CubeSheetDimensionValue,
    CubeSheetLevels,
    CubeSheetTime,
    CubeSheetUser,
    CubeSheetUsers,
    DateColumn,
    DimensionColumn,
    DisplayColumn,
    InitialBalanceColumn,
    LevelCurrencyColumn,
    LevelRef,
    LevelsColumn,
    MetadataList,
    ModeledSheet,
    NumberColumn,
    Sheet,
    StandardSheet,
    TextColumn,
    TextSelectorColumn,
    TimespanColumn,
)
from wdadaptivepy.services import SheetService

# exportSheets #################################################################

get_all_tests: list[tuple[ET.Element, MetadataList[Sheet]]] = []

# TEST 1 -- empty response
get_all_xml_empty = ET.fromstring("""<?xml version='1.0' encoding='UTF-8'?>
<response success="true">
  <output>
  </output>
</response>""")
get_all_tests.append((get_all_xml_empty, MetadataList([])))

# TEST 2 -- one of each sheet type
get_all_xml = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
  <output>
    <sheets>
      <modeled-sheet id="1" name="Personnel" code="Personnel" description="Personnel Sheet" isGlobal="0" recalculateOnDemand="1" />
      <standard-sheet id="6" name="Model Summary" code="" description="Configurable Model Summary Sheet" isGlobal="1" recalculateOnDemand="0" />
      <cube-sheet id="17" name="Expense Cube" code="ExpenseCube" description="" isGlobal="1" recalculateOnDemand="1" />
    </sheets>
  </output>
</response>""")  # noqa: E501
# The service returns all modeled sheets, then standard, then cube.
get_all_tests.append(
    (
        get_all_xml,
        MetadataList(
            [
                ModeledSheet(
                    id=1,
                    name="Personnel",
                    code="Personnel",
                    description="Personnel Sheet",
                    is_global=False,
                    recalculate_on_demand=True,
                ),
                StandardSheet(
                    id=6,
                    name="Model Summary",
                    code="",
                    description="Configurable Model Summary Sheet",
                    is_global=True,
                    recalculate_on_demand=False,
                ),
                CubeSheet(
                    id=17,
                    name="Expense Cube",
                    code="ExpenseCube",
                    description="",
                    is_global=True,
                    recalculate_on_demand=True,
                ),
            ],
        ),
    ),
)


# exportSheetDefinition -- modeled sheet ######################################

modeled_definition_tests: list[tuple[ET.Element, ModeledSheet]] = []

modeled_definition_xml = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <modeled-sheet id="11" code="Personnel" name="Personnel"
                      description="Personnel Sheet" available-in-actuals="false"
                      allow-splits="true" split-column-title="Is Split Child Row"
                      strataId="51">
            <columns>
                <levels code="Plan" name="Plan" read-only="false"
                       splittable="false" required="true">
                    <level id="1" />
                    <level id="7" />
                </levels>
                <text code="LastName" name="Last Name" read-only="false"
                     splittable="false" required="false" />
                <dimension code="JobCode" name="JobCode" read-only="false"
                          splittable="false" required="false" id="9">
                    <value id="19" name="E1" />
                </dimension>
                <text-selector code="BenefitsSelector" name="Benefits"
                              read-only="false" splittable="false"
                              required="true" id="27">
                    <value id="208" name="No" />
                </text-selector>
                <date code="StartDate" name="Start" read-only="false"
                     splittable="false" required="false" />
                <number code="HoursPerWeek" name="Hr/Week" read-only="false"
                       splittable="false" required="false" />
                <initial-balance code="PayRate" name="Pay Rate"
                                read-only="false" splittable="false"
                                required="false" id="143" />
                <display code="PayRate" name="Pay Rate Display Column"
                        read-only="true" splittable="false"
                        required="false" id="7" />
                <level-currency code="" name="Currency" read-only="true"
                               splittable="false" required="false" id="8" />
                <timespan code="MyColumn" name="My Column" read-only="false"
                         splittable="true" required="false" id="42" />
            </columns>
        </modeled-sheet>
    </output>
</response>""")
modeled_definition_tests.append(
    (
        modeled_definition_xml,
        ModeledSheet(
            id=11,
            code="Personnel",
            name="Personnel",
            description="Personnel Sheet",
            available_in_actuals=False,
            allow_splits=True,
            split_column_title="Is Split Child Row",
            strata_id=51,
            levels_columns=MetadataList(
                [
                    LevelsColumn(
                        order=0,
                        code="Plan",
                        name="Plan",
                        read_only=False,
                        splittable=False,
                        required=True,
                        levels=MetadataList([LevelRef(id=1), LevelRef(id=7)]),
                    ),
                ]
            ),
            text_columns=MetadataList(
                [
                    TextColumn(
                        order=1,
                        code="LastName",
                        name="Last Name",
                        read_only=False,
                        splittable=False,
                        required=False,
                    ),
                ]
            ),
            dimension_columns=MetadataList(
                [
                    DimensionColumn(
                        order=2,
                        code="JobCode",
                        name="JobCode",
                        read_only=False,
                        splittable=False,
                        required=False,
                        id=9,
                        values=MetadataList([ColumnValue(id=19, name="E1")]),
                    ),
                ]
            ),
            text_selector_columns=MetadataList(
                [
                    TextSelectorColumn(
                        order=3,
                        code="BenefitsSelector",
                        name="Benefits",
                        read_only=False,
                        splittable=False,
                        required=True,
                        id=27,
                        values=MetadataList([ColumnValue(id=208, name="No")]),
                    ),
                ]
            ),
            date_columns=MetadataList(
                [
                    DateColumn(
                        order=4,
                        code="StartDate",
                        name="Start",
                        read_only=False,
                        splittable=False,
                        required=False,
                    ),
                ]
            ),
            number_columns=MetadataList(
                [
                    NumberColumn(
                        order=5,
                        code="HoursPerWeek",
                        name="Hr/Week",
                        read_only=False,
                        splittable=False,
                        required=False,
                    ),
                ]
            ),
            initial_balance_columns=MetadataList(
                [
                    InitialBalanceColumn(
                        order=6,
                        code="PayRate",
                        name="Pay Rate",
                        read_only=False,
                        splittable=False,
                        required=False,
                        id=143,
                    ),
                ]
            ),
            display_columns=MetadataList(
                [
                    DisplayColumn(
                        order=7,
                        code="PayRate",
                        name="Pay Rate Display Column",
                        read_only=True,
                        splittable=False,
                        required=False,
                        id=7,
                    ),
                ]
            ),
            level_currency_columns=MetadataList(
                [
                    LevelCurrencyColumn(
                        order=8,
                        code="",
                        name="Currency",
                        read_only=True,
                        splittable=False,
                        required=False,
                        id=8,
                    ),
                ]
            ),
            timespan_columns=MetadataList(
                [
                    TimespanColumn(
                        order=9,
                        code="MyColumn",
                        name="My Column",
                        read_only=False,
                        splittable=True,
                        required=False,
                        id=42,
                    ),
                ]
            ),
        ),
    ),
)

# A modeled sheet requested with displayNameEnabled="true": values carry the
# optional code and displayName attributes.
modeled_definition_display_names_xml = ET.fromstring(
    """<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <modeled-sheet id="11" code="Personnel" name="Personnel"
                      available-in-actuals="false" allow-splits="false"
                      strataId="51">
            <columns>
                <dimension code="JobCode" name="JobCode" read-only="false"
                          splittable="false" required="false" id="9">
                    <value id="19" name="E1" code="E1" displayName="E1 - Engineer" />
                    <value id="20" name="E2" />
                </dimension>
                <text-selector code="BenefitsSelector" name="Benefits"
                              read-only="false" splittable="false"
                              required="true" id="27">
                    <value id="208" name="No" code="N" displayName="N - No" />
                </text-selector>
            </columns>
        </modeled-sheet>
    </output>
</response>""",
)
modeled_definition_tests.append(
    (
        modeled_definition_display_names_xml,
        ModeledSheet(
            id=11,
            code="Personnel",
            name="Personnel",
            available_in_actuals=False,
            allow_splits=False,
            strata_id=51,
            dimension_columns=MetadataList(
                [
                    DimensionColumn(
                        order=0,
                        code="JobCode",
                        name="JobCode",
                        read_only=False,
                        splittable=False,
                        required=False,
                        id=9,
                        values=MetadataList(
                            [
                                ColumnValue(
                                    id=19,
                                    name="E1",
                                    code="E1",
                                    display_name="E1 - Engineer",
                                ),
                                ColumnValue(id=20, name="E2"),
                            ],
                        ),
                    ),
                ]
            ),
            text_selector_columns=MetadataList(
                [
                    TextSelectorColumn(
                        order=1,
                        code="BenefitsSelector",
                        name="Benefits",
                        read_only=False,
                        splittable=False,
                        required=True,
                        id=27,
                        values=MetadataList(
                            [
                                ColumnValue(
                                    id=208,
                                    name="No",
                                    code="N",
                                    display_name="N - No",
                                ),
                            ],
                        ),
                    ),
                ]
            ),
        ),
    ),
)


# exportSheetDefinition -- cube sheet #########################################

cube_definition_tests: list[tuple[ET.Element, CubeSheet]] = []

cube_definition_xml = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <cube-sheet id="24" code="SummaryCube" name="Summary Cube"
                   isGlobal="0" description="" strataId="1"
                   horizontalAxis="-3" verticalAxis="-2" maxColumnWidth="0"
                   suppressZeroRows="0" rearrangeGLAndCustomAccounts="0"
                   hideRollupTotals="0">
            <dimensions>
                <dimension id="3" uncategorized="false" rollup="false"
                          name="Company" newValueBehavior="parent"
                          editableOnSheet="false">
                    <value id="35" />
                </dimension>
                <levels>
                    <level id="1" />
                </levels>
                <accounts>
                    <account id="455" code="" isAssumption="false" />
                </accounts>
                <time initialBalance="true" visibleTimeStratumCodes="month" />
            </dimensions>
            <users isExcludedFromWorkflow="true">
                <user id="11" />
            </users>
        </cube-sheet>
    </output>
</response>""")
cube_definition_tests.append(
    (
        cube_definition_xml,
        CubeSheet(
            id=24,
            code="SummaryCube",
            name="Summary Cube",
            description="",
            is_global=False,
            strata_id=1,
            horizontal_axis=-3,
            vertical_axis=[-2],
            max_column_width=0,
            suppress_zero_rows=False,
            rearrange_gl_and_custom_accounts=False,
            hide_rollup_totals=False,
            dimensions=MetadataList(
                [
                    CubeSheetDimension(
                        id=3,
                        uncategorized=False,
                        rollup=False,
                        name="Company",
                        new_value_behavior="parent",
                        editable_on_sheet=False,
                        values=MetadataList([CubeSheetDimensionValue(id=35)]),
                    ),
                ]
            ),
            levels=MetadataList(
                [CubeSheetLevels(levels=MetadataList([LevelRef(id=1)]))],
            ),
            accounts=MetadataList(
                [
                    CubeSheetAccounts(
                        accounts=MetadataList(
                            [
                                CubeSheetAccount(
                                    id=455,
                                    code="",
                                    is_assumption=False,
                                ),
                            ],
                        ),
                    ),
                ]
            ),
            time=MetadataList(
                [
                    CubeSheetTime(
                        initial_balance=True,
                        visible_time_stratum_codes="month",
                    ),
                ]
            ),
            users=MetadataList(
                [
                    CubeSheetUsers(
                        is_excluded_from_workflow=True,
                        users=MetadataList([CubeSheetUser(id=11)]),
                    ),
                ]
            ),
        ),
    ),
)

# A cube sheet whose dimension values carry rollup/uncategorized flags. The
# same value id can appear on several <value> rows distinguished only by the
# flags.
cube_definition_value_flags_xml = ET.fromstring(
    """<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <cube-sheet id="24" code="SummaryCube" name="Summary Cube"
                   isGlobal="0" description="" strataId="1"
                   horizontalAxis="-3" verticalAxis="-2" maxColumnWidth="0"
                   suppressZeroRows="0" rearrangeGLAndCustomAccounts="0"
                   hideRollupTotals="0">
            <dimensions>
                <dimension id="4" name="CountryRegion">
                    <value id="144" />
                    <value id="133" uncategorized="true" />
                    <value id="133" rollup="true" />
                </dimension>
            </dimensions>
        </cube-sheet>
    </output>
</response>""",
)
cube_definition_tests.append(
    (
        cube_definition_value_flags_xml,
        CubeSheet(
            id=24,
            code="SummaryCube",
            name="Summary Cube",
            description="",
            is_global=False,
            strata_id=1,
            horizontal_axis=-3,
            vertical_axis=[-2],
            max_column_width=0,
            suppress_zero_rows=False,
            rearrange_gl_and_custom_accounts=False,
            hide_rollup_totals=False,
            dimensions=MetadataList(
                [
                    CubeSheetDimension(
                        id=4,
                        name="CountryRegion",
                        values=MetadataList(
                            [
                                CubeSheetDimensionValue(id=144),
                                CubeSheetDimensionValue(
                                    id=133,
                                    uncategorized=True,
                                ),
                                CubeSheetDimensionValue(id=133, rollup=True),
                            ],
                        ),
                    ),
                ]
            ),
        ),
    ),
)

# A cube sheet with <attribute> elements between its dimensions and levels.
cube_definition_attributes_xml = ET.fromstring(
    """<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <cube-sheet id="24" code="SummaryCube" name="Summary Cube"
                   isGlobal="0" description="" strataId="1"
                   horizontalAxis="-3" verticalAxis="-2" maxColumnWidth="0"
                   suppressZeroRows="0" rearrangeGLAndCustomAccounts="0"
                   hideRollupTotals="0">
            <dimensions>
                <dimension id="3" uncategorized="false" rollup="false"
                          name="Company" newValueBehavior="parent"
                          editableOnSheet="false">
                    <value id="35" />
                </dimension>
                <attribute id="12" uncategorized="true" rollup="false"
                          name="Region" newValueBehavior="available">
                    <value id="101" />
                    <value id="102" rollup="true" />
                </attribute>
                <attribute id="13" uncategorized="false" rollup="true"
                          name="Segment" newValueBehavior="unavailable">
                    <value id="201" />
                </attribute>
                <levels>
                    <level id="1" />
                </levels>
            </dimensions>
        </cube-sheet>
    </output>
</response>""",
)
cube_definition_tests.append(
    (
        cube_definition_attributes_xml,
        CubeSheet(
            id=24,
            code="SummaryCube",
            name="Summary Cube",
            description="",
            is_global=False,
            strata_id=1,
            horizontal_axis=-3,
            vertical_axis=[-2],
            max_column_width=0,
            suppress_zero_rows=False,
            rearrange_gl_and_custom_accounts=False,
            hide_rollup_totals=False,
            dimensions=MetadataList(
                [
                    CubeSheetDimension(
                        id=3,
                        uncategorized=False,
                        rollup=False,
                        name="Company",
                        new_value_behavior="parent",
                        editable_on_sheet=False,
                        values=MetadataList([CubeSheetDimensionValue(id=35)]),
                    ),
                ]
            ),
            attributes=MetadataList(
                [
                    CubeSheetAttribute(
                        id=12,
                        uncategorized=True,
                        rollup=False,
                        name="Region",
                        new_value_behavior="available",
                        values=MetadataList(
                            [
                                CubeSheetDimensionValue(id=101),
                                CubeSheetDimensionValue(id=102, rollup=True),
                            ],
                        ),
                    ),
                    CubeSheetAttribute(
                        id=13,
                        uncategorized=False,
                        rollup=True,
                        name="Segment",
                        new_value_behavior="unavailable",
                        values=MetadataList([CubeSheetDimensionValue(id=201)]),
                    ),
                ]
            ),
            levels=MetadataList(
                [CubeSheetLevels(levels=MetadataList([LevelRef(id=1)]))],
            ),
        ),
    ),
)

# A cube sheet whose verticalAxis lists multiple dimension ids.
cube_definition_multi_axis_xml = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <cube-sheet id="24" code="SummaryCube" name="Summary Cube"
                   isGlobal="0" description="" strataId="1"
                   horizontalAxis="-3" verticalAxis="-2,5,8" maxColumnWidth="0"
                   suppressZeroRows="0" rearrangeGLAndCustomAccounts="0"
                   hideRollupTotals="0">
        </cube-sheet>
    </output>
</response>""")
cube_definition_tests.append(
    (
        cube_definition_multi_axis_xml,
        CubeSheet(
            id=24,
            code="SummaryCube",
            name="Summary Cube",
            description="",
            is_global=False,
            strata_id=1,
            horizontal_axis=-3,
            vertical_axis=[-2, 5, 8],
            max_column_width=0,
            suppress_zero_rows=False,
            rearrange_gl_and_custom_accounts=False,
            hide_rollup_totals=False,
        ),
    ),
)


@pytest.fixture
def sheet_service() -> SheetService:
    """Fixture for wdadaptivepy's Sheet Service.

    Returns:
        wdadaptivepy SheetService

    """
    xml_api_instance = XMLApi("", "")
    return SheetService(xml_api=xml_api_instance)


@pytest.fixture
def mock_sheets(
    mocker: MockerFixture,
    sheet_service: SheetService,
) -> MagicMock:
    """Mock Adaptive's response from the Sheet XML APIs.

    Args:
        mocker: pytest's mocker
        sheet_service: wdadaptivepy SheetService to mock

    Returns:
        Mock of XMLApi.make_xml_request

    """
    mocked_sheets = mocker.MagicMock()
    mocker.patch.object(
        sheet_service._SheetService__xml_api,  # noqa: SLF001  # pyright: ignore[reportAttributeAccessIssue]
        "make_xml_request",
        mocked_sheets,
    )
    return mocked_sheets


@pytest.mark.parametrize(("element", "expected"), get_all_tests)
def test_get_all(
    element: ET.Element,
    expected: MetadataList[Sheet],
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that wdadaptivepy properly parses Adaptive's exportSheets response.

    Args:
        element: Adaptive's exportSheets XML API response
        expected: wdadaptivepy MetadataList of Sheets
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheets XML API response

    """
    mock_sheets.return_value = element

    sheets = sheet_service.get_all()

    assert sheets == expected


@pytest.mark.parametrize(("element", "expected"), modeled_definition_tests)
def test_get_modeled_definition(
    element: ET.Element,
    expected: ModeledSheet,
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests parsing of a modeled sheet from exportSheetDefinition.

    Args:
        element: Adaptive's exportSheetDefinition XML API response
        expected: wdadaptivepy ModeledSheet
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    mock_sheets.return_value = element

    sheet = sheet_service.get_modeled_definition(11)

    assert sheet == expected


@pytest.mark.parametrize(("element", "expected"), cube_definition_tests)
def test_get_cube_definition(
    element: ET.Element,
    expected: CubeSheet,
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests parsing of a cube sheet from exportSheetDefinition.

    Args:
        element: Adaptive's exportSheetDefinition XML API response
        expected: wdadaptivepy CubeSheet
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    mock_sheets.return_value = element

    sheet = sheet_service.get_cube_definition(24)

    assert sheet == expected


def test_get_modeled_definition_not_found(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a missing modeled sheet definition returns None.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    mock_sheets.return_value = get_all_xml_empty

    assert sheet_service.get_modeled_definition(999) is None


def test_get_cube_definition_not_found(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a missing cube sheet definition returns None.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    mock_sheets.return_value = get_all_xml_empty

    assert sheet_service.get_cube_definition(999) is None


def test_get_modeled_definition_preserves_column_order(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that ``columns`` reflects the sheet's original column order.

    The columns in the fixture are deliberately interleaved across types so
    that a type-grouped result would differ from the true document order.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    interleaved_xml = ET.fromstring("""<?xml version="1.0" encoding="UTF-8"?>
<response success="true">
    <output>
        <modeled-sheet id="11" code="P" name="P">
            <columns>
                <text code="A" name="A" read-only="false" splittable="false" required="false" />
                <number code="N1" name="N1" read-only="false" splittable="false" required="false" />
                <text code="B" name="B" read-only="false" splittable="false" required="false" />
                <number code="N2" name="N2" read-only="false" splittable="false" required="false" />
            </columns>
        </modeled-sheet>
    </output>
</response>""")  # noqa: E501
    mock_sheets.return_value = interleaved_xml

    sheet = sheet_service.get_modeled_definition(11)

    assert sheet is not None
    # Document order is A, N1, B, N2 -- not the type-grouped A, B, N1, N2.
    assert [(column.order, column.code) for column in sheet.columns] == [
        (0, "A"),
        (1, "N1"),
        (2, "B"),
        (3, "N2"),
    ]
    # Order is still tracked within each type-grouped list.
    assert [column.order for column in sheet.text_columns] == [0, 2]
    assert [column.order for column in sheet.number_columns] == [1, 3]


def test_get_modeled_definition_by_object(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a ModeledSheet object is resolved via its ``id``.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    mock_sheets.return_value = modeled_definition_xml

    sheet = sheet_service.get_modeled_definition(ModeledSheet(id=11, code="Personnel"))

    assert sheet == modeled_definition_tests[0][1]
    # A single request is sent (no exportSheets lookup) using the object's id.
    assert mock_sheets.call_count == 1
    assert mock_sheets.call_args.kwargs["payload"].get("id") == "11"


def test_get_cube_definition_by_object(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a CubeSheet object is resolved via its ``id``.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    mock_sheets.return_value = cube_definition_xml

    sheet = sheet_service.get_cube_definition(CubeSheet(id=24, code="SummaryCube"))

    assert sheet == cube_definition_tests[0][1]
    assert mock_sheets.call_count == 1
    assert mock_sheets.call_args.kwargs["payload"].get("id") == "24"


def test_get_modeled_definition_object_without_id_raises(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a ModeledSheet object without an ``id`` raises ValueError.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    with pytest.raises(ValueError, match="does not have an id"):
        sheet_service.get_modeled_definition(ModeledSheet(code="Personnel"))

    # No request is sent when resolution fails.
    assert mock_sheets.call_count == 0


def test_get_modeled_definition_by_code(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a str is treated as a code and resolved via ``exportSheets``.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's Sheet XML API responses

    """
    # First call resolves the code via exportSheets; second is the definition.
    mock_sheets.side_effect = [get_all_xml, modeled_definition_xml]

    sheet = sheet_service.get_modeled_definition("Personnel")

    assert sheet == modeled_definition_tests[0][1]
    # The code "Personnel" resolves to id 1 in the exportSheets fixture.
    # Indexing call_args_list[1] also confirms a second request was sent.
    assert mock_sheets.call_args_list[0].kwargs["method"] == "exportSheets"
    assert mock_sheets.call_args_list[1].kwargs["payload"].get("id") == "1"


def test_get_cube_definition_by_code(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that a str is treated as a code and resolved via ``exportSheets``.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's Sheet XML API responses

    """
    mock_sheets.side_effect = [get_all_xml, cube_definition_xml]

    sheet = sheet_service.get_cube_definition("ExpenseCube")

    assert sheet == cube_definition_tests[0][1]
    # The code "ExpenseCube" resolves to id 17 in the exportSheets fixture.
    # Indexing call_args_list[1] also confirms a second request was sent.
    assert mock_sheets.call_args_list[0].kwargs["method"] == "exportSheets"
    assert mock_sheets.call_args_list[1].kwargs["payload"].get("id") == "17"


def test_get_modeled_definition_unknown_code_raises(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that an unmatched code raises ValueError.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheets response

    """
    mock_sheets.return_value = get_all_xml

    with pytest.raises(ValueError, match="No Sheet found with code"):
        sheet_service.get_modeled_definition("DoesNotExist")


def test_get_modeled_definition_unsupported_type_raises(
    sheet_service: SheetService,
    mock_sheets: MagicMock,
) -> None:
    """Tests that an unsupported argument type raises TypeError.

    Args:
        sheet_service: wdadaptivepy SheetService
        mock_sheets: Mocker for Adaptive's exportSheetDefinition response

    """
    with pytest.raises(TypeError, match="Unexpected type for sheet"):
        sheet_service.get_modeled_definition(1.5)  # type: ignore[arg-type]

    assert mock_sheets.call_count == 0
