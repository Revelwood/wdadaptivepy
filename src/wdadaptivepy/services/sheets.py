"""wdadaptivepy service for Adaptive's Sheets."""

from collections.abc import Sequence
from xml.etree import ElementTree as ET

from wdadaptivepy.connectors.xml_api.xml_api import XMLApi
from wdadaptivepy.models.base import bool_to_str_true_false
from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.models.sheet import (
    CubeSheet,
    ModeledSheet,
    Sheet,
    StandardSheet,
)


class SheetService:
    """Retrieve Adaptive Sheets and their definitions.

    Attributes:
        Sheet: wdadaptivepy Sheet
        ModeledSheet: wdadaptivepy ModeledSheet
        StandardSheet: wdadaptivepy StandardSheet
        CubeSheet: wdadaptivepy CubeSheet

    """

    def __init__(self, xml_api: XMLApi) -> None:
        """Initialize SheetService.

        Args:
            xml_api: wdadaptivepy XMLApi

        """
        self.__xml_api = xml_api
        self.Sheet = Sheet
        self.ModeledSheet = ModeledSheet
        self.StandardSheet = StandardSheet
        self.CubeSheet = CubeSheet

    def get_all(self) -> MetadataList[Sheet]:
        """Retrieve all Sheets from Adaptive via ``exportSheets``.

        Returns:
            Adaptive Sheets (modeled, standard, and cube), each as its
            corresponding wdadaptivepy Sheet subclass.

        """
        response = self.__xml_api.make_xml_request(
            method="exportSheets",
            payload=None,
        )
        sheets = MetadataList[Sheet]()
        sheets.extend(ModeledSheet.from_xml(xml=response))
        sheets.extend(StandardSheet.from_xml(xml=response))
        sheets.extend(CubeSheet.from_xml(xml=response))
        return sheets

    def __resolve_sheet_id(
        self,
        sheet: ModeledSheet | CubeSheet | int | str,
        expected_type: type[ModeledSheet] | type[CubeSheet],
    ) -> int:
        """Resolve a sheet identifier to an Adaptive internal sheet ID.

        Args:
            sheet: A wdadaptivepy sheet of ``expected_type`` (whose ``id`` is
                used), an int used directly as the ID, or a str treated as a
                sheet code and looked up across all sheets via ``exportSheets``.
            expected_type: The wdadaptivepy sheet class accepted as an object.

        Returns:
            The resolved Adaptive internal sheet ID.

        Raises:
            ValueError: The given sheet object has no ``id``, or no sheet was
                found with the given code.
            TypeError: ``sheet`` is not a supported type.

        """
        if isinstance(sheet, expected_type):
            if sheet.id is None:
                error_message = f"{expected_type.__name__} does not have an id"
                raise ValueError(error_message)
            return sheet.id
        if isinstance(sheet, int):
            return sheet
        if isinstance(sheet, str):
            match = self.get_all().get_member(code=sheet)
            if match is None:
                error_message = f"No Sheet found with code {sheet!r}"
                raise ValueError(error_message)
            if match.id is None:
                error_message = f"Sheet with code {sheet!r} does not have an id"
                raise ValueError(error_message)
            return match.id
        error_message = f"Unexpected type for sheet: {type(sheet).__name__}"
        raise TypeError(error_message)

    def get_modeled_definition(
        self,
        sheet: ModeledSheet | int | str,
        *,
        display_name_enabled: bool = True,
    ) -> ModeledSheet | None:
        """Retrieve the definition of a modeled sheet via ``exportSheetDefinition``.

        Args:
            sheet: The modeled sheet to retrieve. May be a ``ModeledSheet``
                (its ``id`` is used), an int used directly as the internal ID,
                or a str treated as the sheet code and looked up across all
                sheets via ``exportSheets``.
            display_name_enabled: Adaptive Display Name Enabled

        Returns:
            The modeled sheet definition, or None if not found.

        Raises:
            ValueError: ``sheet`` is a ``ModeledSheet`` without an ``id``, or is
                a code with no matching sheet.
            TypeError: ``sheet`` is not a supported type.

        """
        sheet_id = self.__resolve_sheet_id(sheet, ModeledSheet)
        modeled_sheet = ET.Element(
            "modeled-sheet",
            attrib={
                "id": str(sheet_id),
                "displayNameEnabled": str(
                    bool_to_str_true_false(display_name_enabled),
                ),
            },
        )
        response = self.__xml_api.make_xml_request(
            method="exportSheetDefinition",
            payload=modeled_sheet,
        )
        sheets = ModeledSheet.from_xml(xml=response)
        if len(sheets) == 0:
            return None
        return sheets[0]

    def get_cube_definition(self, sheet: CubeSheet | int | str) -> CubeSheet | None:
        """Retrieve the definition of a cube sheet via ``exportSheetDefinition``.

        Args:
            sheet: The cube sheet to retrieve. May be a ``CubeSheet`` (its
                ``id`` is used), an int used directly as the internal ID, or a
                str treated as the sheet code and looked up across all sheets
                via ``exportSheets``.

        Returns:
            The cube sheet definition, or None if not found.

        Raises:
            ValueError: ``sheet`` is a ``CubeSheet`` without an ``id``, or is a
                code with no matching sheet.
            TypeError: ``sheet`` is not a supported type.

        """
        sheet_id = self.__resolve_sheet_id(sheet, CubeSheet)
        cube_sheet = ET.Element("cube-sheet", attrib={"id": str(sheet_id)})
        response = self.__xml_api.make_xml_request(
            method="exportSheetDefinition",
            payload=cube_sheet,
        )
        sheets = CubeSheet.from_xml(xml=response)
        if len(sheets) == 0:
            return None
        return sheets[0]

    def from_json(self, data: str) -> MetadataList[Sheet]:
        """Convert JSON to MetadataList of Sheets.

        Args:
            data: JSON string

        Returns:
            MetadataList of Sheets

        """
        return MetadataList[Sheet](Sheet.from_json(data=data))

    def from_dict(self, data: Sequence[dict] | dict) -> MetadataList[Sheet]:
        """Convert Python Dictionary to MetadataList of Sheets.

        Args:
            data: Python Dictionary

        Returns:
            MetadataList of Sheets

        """
        return MetadataList[Sheet](Sheet.from_dict(data=data))
