"""wdadaptivepy model for Adaptive's Permission Sets."""

from typing import Annotated, ClassVar

from pydantic import BeforeValidator

from wdadaptivepy.models.base import (
    ClassXMLMetadata,
    FieldMetadata,
    FieldXMLMetadata,
    Metadata,
)
from wdadaptivepy.utils.parsers import (
    int_to_str,
    str_to_str,
)
from wdadaptivepy.utils.validators import (
    int_or_none,
    str_or_none,
)


class PermissionSet(Metadata):
    """wdadaptivepy model for Adaptive's Permission Sets.

    Attributes:
        id: Adaptive Permission Set ID
        name: Adaptive Permission Set Name
        permissions: Adaptive Permission Set Permissions

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
    permissions: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="permissions",
                    serializer=str_to_str,
                )
            ]
        ),
    ] = None
    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="permission_sets",
            default_tag="permission_set",
        )
    ]
