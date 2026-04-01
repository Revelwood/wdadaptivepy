"""wdadaptivepy base model for Adaptive's metadata."""

import sys
from abc import ABC
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from json import loads
from typing import Annotated, Any, ClassVar, Literal, cast
from xml.etree import ElementTree as ET

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PrivateAttr,
    SerializerFunctionWrapHandler,
    computed_field,
    field_serializer,
    model_serializer,
)

if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

from wdadaptivepy.models.list import MetadataList
from wdadaptivepy.utils.parsers import int_to_str, str_to_str
from wdadaptivepy.utils.validators import (
    int_or_none,
    nullable_int_or_none,
    str_or_none,
)


def remove_empty_elements(data: Any) -> Any:  # noqa: ANN401
    """Recursively removes None, empty lists, and empty dicts."""
    if isinstance(data, dict):
        cleaned = {k: remove_empty_elements(v) for k, v in data.items()}
        return {k: v for k, v in cleaned.items() if v is not None and v not in [[], {}]}
    if isinstance(data, list):
        cleaned = [remove_empty_elements(v) for v in data]
        return [v for v in cleaned if v is not None and v not in [[], {}]]
    return data


@dataclass(frozen=True)
class ClassXMLMetadata:
    """Define Class for XML serialization.

    Attributes:
        xml_version: XML API Version
        default_parent_tag: Parent XML Element's Tag
        default_tag: XML Element's Tag
        default_children: Field name and Data Type of children XML Elements
        create_parent_tag: Parent XML Element Tag used for create API calls
        create_tag: XML Element Tag used for create API calls
        create_children: Field and Type of children XML Elements for create API calls
        read_parent_tag: Parent XML Element Tag used for read API calls
        read_tag: XML Element Tag used for read API calls
        read_children: Field and Type of children XML Elements for read API calls
        update_parent_tag: Parent XML Element Tag used for update API calls
        update_tag: XML Element Tag used for update API calls
        update_children: Field and Type of children XML Elements for update API calls
        delete_parent_tag: XML Parent Element Tag used for delete API calls
        delete_tag: XML Element Tag used for delete API calls
        delete_children: Field and Type of children XML Elements for delete API calls

    """

    xml_version: float | Literal["default"] = "default"
    default_parent_tag: str | None = None
    default_tag: str | None = None
    default_children: dict[str, type["BaseMetadata"]] | None = None
    create_parent_tag: str | None = None
    create_tag: str | None = None
    create_children: dict[str, type["BaseMetadata"]] | None = None
    read_parent_tag: str | None = None
    read_tag: str | None = None
    read_children: dict[str, type["BaseMetadata"]] | None = None
    update_parent_tag: str | None = None
    update_tag: str | None = None
    update_children: dict[str, type["BaseMetadata"]] | None = None
    delete_parent_tag: str | None = None
    delete_tag: str | None = None
    delete_children: dict[str, type["BaseMetadata"]] | None = None


@dataclass(frozen=True)
class FieldXMLMetadata:
    """Define field for XML serialization.

    Attributes:
        xml_version: XML API version
        default_tag: XML Element Tag to use
        create_tag: XML Element Tag to use for create API calls
        read_tag: XML Element Tag to use for read API calls
        update_tag: XML Element Tag to use for update API calls
        delete_tag: XML Element Tag to use for delete API calls
        serializer: XML Element Tag to use for data serializer to XML
        is_child: Flag if field are XML Element children

    """

    xml_version: float | Literal["default"] = "default"
    default_tag: str | None = None
    create_tag: str | None = None
    read_tag: str | None = None
    update_tag: str | None = None
    delete_tag: str | None = None
    serializer: Callable[[Any], str | None] | None = None
    is_child: bool | None = None


@dataclass(frozen=True)
class FieldMetadata:
    """Define field information.

    Attributes:
        xml: XML serializer for XML API

    """

    xml: list[FieldXMLMetadata] = field(default_factory=list)


class BaseMetadata(BaseModel, ABC):
    """Base class for all Adaptive Metadata."""

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")

    def __hash__(self) -> int:
        """Create a hash for a BaseMetadata instance.

        Returns:
            int hash value

        """
        return hash(getattr(self, f, None) for f, _ in type(self).model_fields)

    def __eq__(self, other: object) -> bool:
        """Check if two BaseMetadata objects are equal.

        Args:
            other: Object to compare with

        Returns:
            True if equal, False otherwise

        """
        if other is None:
            return self is None

        if not isinstance(other, type(self)):
            return NotImplemented
        for self_field in type(self).model_fields:
            self_value = getattr(self, self_field, None)
            other_value = getattr(other, self_field, None)
            if self_value != other_value:
                return False

        self_parent = getattr(self, "adaptive_parent", None)
        other_parent = getattr(other, "adaptive_parent", None)
        if self_parent != other_parent:
            return False

        self_attributes = getattr(self, "adaptive_attributes", None)
        other_attributes = getattr(other, "adaptive_attributes", None)
        return self_attributes == other_attributes

    @classmethod
    def _get_from_xml_element(cls, xml_element: ET.Element) -> Self:
        metadata_data = {}
        for field_name in cls.model_fields:
            field_xml_tag = cls._get_field_xml_tag(
                field=field_name, tag="read", version="default"
            )
            if field_xml_tag is not None:
                metadata_data[field_name] = xml_element.get(
                    field_xml_tag,
                    None,
                )
        return cls(**metadata_data)

    @classmethod
    def _set_children_from_xml_element(
        cls,
        metadata_member: Self,
        xml_children: dict[str, type["BaseMetadata"]],
        xml_element: ET.Element,
    ) -> None:
        for field_name, data_type in xml_children.items():
            child_xml_parent_tag, child_xml_tag = data_type._get_class_xml_for_version(  # noqa: SLF001
                "read",
                "default",
            )
            if child_xml_tag is None or child_xml_parent_tag is None:
                raise ValueError
            search_xml_tag = (
                child_xml_tag
                if child_xml_parent_tag == xml_element.tag
                else child_xml_parent_tag
            )
            children_members = MetadataList()
            for child_element in xml_element.findall(f"./{search_xml_tag}"):
                children_members.extend(data_type.from_xml(child_element))
            if children_members:
                setattr(metadata_member, field_name, children_members)

    @classmethod
    def _set_adaptive_attribute_from_xml_element(
        cls, metadata_member: Self, xml_element: ET.Element
    ) -> None:
        parent_xml_tag, _ = MetadataAttribute._get_class_xml_for_version(  # noqa: SLF001
            "read", "default"
        )
        if not parent_xml_tag:
            raise ValueError
        for metadata_element in xml_element.findall(parent_xml_tag):
            adaptive_metadata_members = MetadataAttribute.from_xml(
                metadata_element,
            )
            for adaptive_metadata_member in adaptive_metadata_members:
                set_adaptive_attribute = getattr(
                    metadata_member,
                    "set_adaptive_attribute",
                    None,
                )
                if set_adaptive_attribute is None:
                    error_message = "Cannot access set_adaptive_attribute"
                    raise RuntimeError(error_message)
                set_adaptive_attribute(adaptive_metadata_member)

    @classmethod
    def _set_adaptive_children_from_xml_element(  # noqa: PLR0913
        cls,
        metadata_member: Self,
        metadata_members: MetadataList[Self],
        xml_element: ET.Element,
        xml_tag: str,
        xml_children: dict[str, type["BaseMetadata"]] | None,
        parent: Self | None,
        processed_xml_elements: list[ET.Element],
    ) -> None:
        if parent is not None:
            set_adaptive_parent: Callable | None = getattr(
                metadata_member, "set_adaptive_parent", None
            )
            if set_adaptive_parent is not None:
                set_adaptive_parent(parent)
        for xml_child_element in xml_element.findall(path=xml_tag):
            metadata_members.extend(
                cls._serialize_from_xml(
                    xml_element=xml_child_element,
                    xml_tag=xml_tag,
                    xml_children=xml_children,
                    parent=metadata_member,
                    processed_xml_elements=processed_xml_elements,
                )
            )

    @classmethod
    def _serialize_from_xml(
        cls: type[Self],
        xml_element: ET.Element,
        xml_tag: str,
        xml_children: dict[str, type["BaseMetadata"]] | None,
        parent: Self | None,
        processed_xml_elements: list[ET.Element],
    ) -> MetadataList[Self]:
        processed_xml_elements.append(xml_element)
        metadata_member = cls._get_from_xml_element(xml_element=xml_element)
        metadata_members = MetadataList[Self]([metadata_member])
        if xml_children:
            cls._set_children_from_xml_element(
                metadata_member=metadata_member,
                xml_children=xml_children,
                xml_element=xml_element,
            )
        if hasattr(metadata_member, "adaptive_attributes"):
            cls._set_adaptive_attribute_from_xml_element(
                metadata_member=metadata_member,
                xml_element=xml_element,
            )
        if hasattr(metadata_member, "adaptive_parent"):
            cls._set_adaptive_children_from_xml_element(
                metadata_member=metadata_member,
                metadata_members=metadata_members,
                xml_element=xml_element,
                xml_tag=xml_tag,
                xml_children=xml_children,
                parent=parent,
                processed_xml_elements=processed_xml_elements,
            )

        return metadata_members

    @classmethod
    def _get_field_xml_tag(
        cls,
        field: str,
        tag: Literal["create", "read", "update", "delete"],
        version: float | Literal["default"],
    ) -> str | None:
        return cls._get_field_xml_tag_for_version(
            field_xml_metadata=cls._get_field_xml_metadata(field),
            tag=tag,
            version=version,
        )

    @classmethod
    def _get_field_xml_tag_from_tags(
        cls,
        xml_tags: FieldXMLMetadata,
        tag: Literal["create", "read", "update", "delete"],
    ) -> str | None:
        field_xml_tag = None
        if xml_tags.default_tag is not None:
            field_xml_tag = xml_tags.default_tag
        if tag == "create" and xml_tags.create_tag is not None:
            field_xml_tag = xml_tags.create_tag
        elif tag == "read" and xml_tags.read_tag is not None:
            field_xml_tag = xml_tags.read_tag
        elif tag == "update" and xml_tags.update_tag is not None:
            field_xml_tag = xml_tags.update_tag
        elif tag == "delete" and xml_tags.delete_tag is not None:
            field_xml_tag = xml_tags.delete_tag
        return field_xml_tag

    @classmethod
    def _get_field_xml_tag_for_version(
        cls,
        field_xml_metadata: list[FieldXMLMetadata],
        tag: Literal["create", "read", "update", "delete"],
        version: float | Literal["default"] = "default",
    ) -> str | None:
        xml_versions = [x.xml_version for x in field_xml_metadata]
        field_xml_tag = None
        if "default" in xml_versions:
            default_xml_tags = field_xml_metadata[xml_versions.index("default")]
            if default_xml_tags.is_child is not True:
                field_xml_tag = cls._get_field_xml_tag_from_tags(default_xml_tags, tag)
        if not isinstance(version, float):
            tagged_xml_versions = [x for x in xml_versions if isinstance(x, float)]
        else:
            tagged_xml_versions = [
                x for x in xml_versions if isinstance(x, float) and x <= version
            ]
        tagged_xml_version = max(tagged_xml_versions) if tagged_xml_versions else None
        if tagged_xml_version:
            tagged_xml_tags = field_xml_metadata[xml_versions.index(tagged_xml_version)]
            if tagged_xml_tags.is_child is not True:
                field_xml_tag = cls._get_field_xml_tag_from_tags(tagged_xml_tags, tag)
        return field_xml_tag

    @classmethod
    def _get_field_xml_metadata(cls, field: str) -> list[FieldXMLMetadata]:
        class_fields = cls.model_fields
        for field_name, field_info in class_fields.items():
            if field_name != field:
                continue
            for metadata in field_info.metadata:
                if isinstance(metadata, FieldMetadata):
                    return metadata.xml
        return []

    @classmethod
    def _get_class_xml_metadata(cls) -> list[ClassXMLMetadata]:
        try:
            xml_tags_info = cls._xml_tags  # pyright: ignore[reportAttributeAccessIssue]
        except AttributeError as e:
            raise AttributeError from e
        if not xml_tags_info:
            raise ValueError
        return xml_tags_info

    @classmethod
    def _get_class_xml_parent_xml_tag(
        cls,
        xml_tags: ClassXMLMetadata,
        tag: str,
    ) -> str | None:
        parent_xml_tag = None
        if xml_tags.default_parent_tag is not None:
            parent_xml_tag = xml_tags.default_parent_tag
        if tag == "default":
            pass
        elif tag == "create" and xml_tags.create_parent_tag is not None:
            parent_xml_tag = xml_tags.create_parent_tag
        elif tag == "read" and xml_tags.read_parent_tag is not None:
            parent_xml_tag = xml_tags.read_parent_tag
        elif tag == "update" and xml_tags.update_parent_tag is not None:
            parent_xml_tag = xml_tags.update_parent_tag
        elif tag == "delete" and xml_tags.delete_parent_tag is not None:
            parent_xml_tag = xml_tags.delete_parent_tag
        return parent_xml_tag

    @classmethod
    def _get_class_xml_children_xml_tag(
        cls,
        xml_tags: ClassXMLMetadata,
        tag: str,
    ) -> dict[str, type["BaseMetadata"]]:
        children_xml = {}
        if xml_tags.default_children is not None:
            children_xml = xml_tags.default_children
        if tag == "default":
            pass
        elif tag == "create" and xml_tags.create_children is not None:
            children_xml = xml_tags.create_children
        elif tag == "read" and xml_tags.read_children is not None:
            children_xml = xml_tags.read_children
        elif tag == "update" and xml_tags.update_children is not None:
            children_xml = xml_tags.update_children
        elif tag == "delete" and xml_tags.delete_children is not None:
            children_xml = xml_tags.delete_children
        return children_xml

    @classmethod
    def _get_class_xml_children_for_version(
        cls,
        tag: Literal["create", "read", "update", "delete"],
        version: float | Literal["default"] = "default",
    ) -> dict[str, type["BaseMetadata"]]:
        class_xml_metadata = cls._get_class_xml_metadata()
        xml_versions = [x.xml_version for x in class_xml_metadata]
        xml_children = {}
        if "default" in xml_versions:
            default_xml_tags = class_xml_metadata[xml_versions.index("default")]
            xml_children = cls._get_class_xml_children_xml_tag(default_xml_tags, tag)
        if not isinstance(version, float):
            tagged_xml_versions = [x for x in xml_versions if isinstance(x, float)]
        else:
            tagged_xml_versions = [
                x for x in xml_versions if isinstance(x, float) and x <= version
            ]
        tagged_xml_version = max(tagged_xml_versions) if tagged_xml_versions else None
        if tagged_xml_version:
            tagged_xml_tags = class_xml_metadata[xml_versions.index(tagged_xml_version)]
            xml_children = cls._get_class_xml_children_xml_tag(tagged_xml_tags, tag)

        return xml_children

    @classmethod
    def _get_class_xml_xml_tag(
        cls,
        xml_tags: ClassXMLMetadata,
        tag: str,
    ) -> str | None:
        xml_tag = None
        if xml_tags.default_tag is not None:
            xml_tag = xml_tags.default_tag
        if tag == "default":
            pass
        elif tag == "create" and xml_tags.create_tag is not None:
            xml_tag = xml_tags.create_tag
        elif tag == "read" and xml_tags.read_tag is not None:
            xml_tag = xml_tags.read_tag
        elif tag == "update" and xml_tags.update_tag is not None:
            xml_tag = xml_tags.update_tag
        elif tag == "delete" and xml_tags.delete_tag is not None:
            xml_tag = xml_tags.delete_tag

        return xml_tag

    @classmethod
    def _get_class_xml_for_version(
        cls,
        tag: Literal["create", "read", "update", "delete"],
        version: float | Literal["default"] = "default",
    ) -> tuple[str | None, str | None]:
        class_xml_metadata = cls._get_class_xml_metadata()
        xml_versions = [x.xml_version for x in class_xml_metadata]
        parent_xml_tag = None
        xml_tag = None
        if "default" in xml_versions:
            default_xml_tags = class_xml_metadata[xml_versions.index("default")]
            parent_xml_tag = cls._get_class_xml_parent_xml_tag(default_xml_tags, tag)
            xml_tag = cls._get_class_xml_xml_tag(default_xml_tags, tag)
        if not isinstance(version, float):
            tagged_xml_versions = [x for x in xml_versions if isinstance(x, float)]
        else:
            tagged_xml_versions = [
                x for x in xml_versions if isinstance(x, float) and x <= version
            ]
        tagged_xml_version = max(tagged_xml_versions) if tagged_xml_versions else None
        if tagged_xml_version:
            tagged_xml_tags = class_xml_metadata[xml_versions.index(tagged_xml_version)]
            parent_xml_tag = cls._get_class_xml_parent_xml_tag(tagged_xml_tags, tag)
            xml_tag = cls._get_class_xml_xml_tag(tagged_xml_tags, tag)

        return parent_xml_tag, xml_tag

    @classmethod
    def from_xml(
        cls: type[Self],
        xml: ET.Element,
    ) -> MetadataList[Self]:
        """Create wdadaptivepy object from XML.

        Args:
            cls: Metadata Base Class
            xml: XML to convert to MetadataList of wdadaptivepy metadata objects

        Returns:
            wdadaptivepy MetadataList

        Raises:
            RuntimeError: Unexpected value
            ValueError: Unexpected value

        """
        metadata_members = MetadataList[Self]()

        _, xml_tag = cls._get_class_xml_for_version("read", "default")

        xml_children = cls._get_class_xml_children_for_version(
            "read",
            "default",
        )
        if xml_tag is not None:
            processed_xml_elements: list[ET.Element] = []
            for xml_element in xml.iter(tag=xml_tag):
                if xml_element not in processed_xml_elements:
                    metadata_members.extend(
                        cls._serialize_from_xml(
                            xml_element=xml_element,
                            xml_tag=xml_tag,
                            xml_children=xml_children,
                            parent=None,
                            processed_xml_elements=processed_xml_elements,
                        )
                    )

        return metadata_members

    @classmethod
    def to_xml(cls: type[Self], xml_type: str, members: Sequence[Self]) -> ET.Element:  # NOQA: PLR0912 PLR0915 C901
        """Convert BaseMetadata to XML.

        Args:
            cls: BaseMetadata
            xml_type: Adaptive XML API call type
            members: BaseMetadata members

        Returns:
            XML Element

        Raises:
            RuntimeError: Unexpected value

        """
        xml_parent_tag, xml_tag = cls._get_class_xml_for_version("create", "default")
        if not xml_parent_tag or not xml_tag:
            raise ValueError
        xml_children = cls._get_class_xml_children_for_version("create", "default")
        root_element = ET.Element(xml_parent_tag)
        parent_elements: list[ET.Element] = []
        parent_members = MetadataList()
        if hasattr(cls, "adaptive_parent"):
            get_common_ancestors = getattr(cls, "get_common_ancestors", None)
            if get_common_ancestors is None:
                error_message = "Missing get_common_ancestors"
                raise RuntimeError(error_message)
            parent_members = get_common_ancestors(members=members)
            for index, parent in enumerate(parent_members):
                parent_element = ET.Element(
                    xml_tag,
                    {"id": str(parent.id)},
                )
                parent_elements.append(parent_element)
                if index == 0 or parent.adaptive_parent is None:
                    root_element.append(parent_element)
                else:
                    parent_index = parent_members.index(parent.adaptive_parent)
                    parent_elements[parent_index].append(parent_element)
        for member in members:
            member_element = ET.Element(xml_tag)
            for field_name, field_def in cls.__dataclass_fields__.items():
                xml_name = field_def.metadata.get(f"xml_{xml_type}")
                xml_parser = field_def.metadata.get("xml_parser")
                if xml_name is None or xml_name == "" or xml_parser is None:
                    continue
                xml_value = xml_parser(getattr(member, field_name))
                if xml_value is not None:
                    member_element.attrib[xml_name] = xml_value
            for field_name, data_type in xml_children.items():
                if getattr(member, field_name) not in [None, [], {}]:
                    children = data_type.to_xml(xml_type, getattr(member, field_name))
                    if children.tag == xml_tag:
                        member_element.extend(children)
                    else:
                        member_element.append(children)
            if adaptive_attributes := getattr(member, "adaptive_attributes", None):
                attributes = MetadataAttribute.to_xml(xml_type, adaptive_attributes)
                member_element.extend(attributes)
            if hasattr(member, "adaptive_parent"):
                if member in parent_members:
                    index = parent_members.index(member)
                    parent_elements[index].attrib = member_element.attrib
                    parent_elements[index].extend(member_element)
                else:
                    adaptive_parent = getattr(member, "adaptive_parent", None)
                    if adaptive_parent is None:
                        index = 0
                    else:
                        index = parent_members.index(adaptive_parent)
                    parent_elements[index].append(member_element)
            else:
                root_element.append(member_element)

        return root_element

    @classmethod
    def from_json(cls: type[Self], data: str) -> MetadataList[Self]:
        """Convert JSON to MetadataList.

        Args:
            cls: BaseMetadata
            data: JSON string

        Returns:
            MetadataList

        """
        vals = loads(s=data)
        return cls.from_dict(data=vals)

    @classmethod
    def from_dict(
        cls: type[Self],
        data: dict | Sequence[dict],
    ) -> MetadataList[Self]:
        """Convert Python Dictionary to MetadataList.

        Args:
            cls: BaseMetadata
            data: Python Dictionary

        Returns:
            MetadataList

        """
        members = MetadataList[Self]()
        if isinstance(data, Sequence):
            for record in data:
                member = cls(**record)
                members.append(member)
        elif isinstance(data, dict):
            member = cls(**data)
            members.append(member)

        return members

    @model_serializer(mode="wrap")
    def clean_empty_fields(
        self,
        handler: SerializerFunctionWrapHandler,
    ) -> dict[str, object]:
        """Remove fields with None or empty values.

        Args:
            handler: Serializer object

        Returns:
            Cleaned object

        """
        raw_dict = handler(self)

        return remove_empty_elements(raw_dict)


class BaseHierarchialMetadata(BaseModel, ABC):
    """Base class for hierarchial Adaptive metadata.

    Attributes:
        parent: wdadaptivepy BaseHierarchialMetadata parent
        children: wdadaptivepy BaseHierarchialMetadata children

    """

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")

    parent: Self | None = Field(default=None, exclude=True)
    children: Sequence[Self] = Field(default_factory=MetadataList[Self], exclude=True)
    _adaptive_parent: Self | None = PrivateAttr(default=None)
    _adaptive_children: MetadataList[Self] = PrivateAttr(
        default_factory=MetadataList[Self]
    )

    def model_post_init(self, context: Any) -> None:  # noqa: ANN401
        """Cleanup BaseHierarchialMetadata instance."""
        self.set_adaptive_parent(self.parent)
        for child in self.children:
            self._add_adaptive_child(child)
        del self.parent
        del self.children
        if hasattr(super(), "model_post_init"):
            super().model_post_init(context)

    @computed_field
    @property
    def adaptive_parent(self) -> Self | None:
        """Adaptive parent from hierarchy.

        Returns:
            wdadaptivepy parent

        """
        return self._adaptive_parent

    @field_serializer("adaptive_parent", when_used="json", mode="wrap")
    def strip_parent_data(
        self,
        adaptive_parent: Self | None,
        handler: SerializerFunctionWrapHandler,
    ) -> None | int | str:
        """Remove fields from parent object for JSON serialization.

        Args:
            adaptive_parent: Adaptive parent object
            handler: Serializer object

        Returns:
            Identifier for parent, if it exists

        """
        raw_adaptive_parent = handler(adaptive_parent)
        if raw_adaptive_parent is None:
            return None
        if self._adaptive_parent is None:
            return None
        adaptive_id = cast("int | None", getattr(self._adaptive_parent, "id", None))
        if adaptive_id is not None:
            # if adaptive_id := self._adaptive_parent.get("id", None) is not None:
            # if adaptive_id := getattr(raw_adaptive_parent, "id", None) is not None:
            return adaptive_id
        code = cast("str | None", getattr(self._adaptive_parent, "code", None))
        if code is not None:
            # if code := self._adaptive_parent.get("code", None) is not None:
            # if code := getattr(raw_adaptive_parent, "code", None) is not None:
            return code
        name = raw_adaptive_parent.name
        if name is not None:
            # if name := raw_adaptive_parent.get("name", None) is not None:
            # if name := getattr(raw_adaptive_parent, "name", None) is not None:
            return name
        return None

    @property
    def adaptive_children(self) -> MetadataList[Self]:
        """Adaptive children from hierarchy.

        Returns:
            wdadaptivepy MetadataList of children

        """
        return self._adaptive_children

    def set_adaptive_parent(self, adaptive_parent: Self | None) -> None:
        """Assign parent of wdadaptivepy member.

        Args:
            adaptive_parent: wdadaptivepy parent member

        """
        if self == adaptive_parent:
            raise ValueError
        if self._adaptive_parent != adaptive_parent:
            if adaptive_parent is not None:
                adaptive_parent._add_adaptive_child(adaptive_child=self)  # noqa: SLF001
                if (
                    adaptive_parent.adaptive_parent is not None
                    and self == adaptive_parent.adaptive_parent
                ):
                    adaptive_parent.set_adaptive_parent(
                        adaptive_parent=self.adaptive_parent,
                    )
            if self._adaptive_parent is not None:
                self._adaptive_parent._remove_adaptive_child(adaptive_child=self)  # noqa: SLF001
            self._adaptive_parent = adaptive_parent

    def _add_adaptive_child(self, adaptive_child: Self) -> None:
        if adaptive_child not in self._adaptive_children:
            self._adaptive_children.append(adaptive_child)

    def _remove_adaptive_child(self, adaptive_child: Self) -> None:
        self._adaptive_children.remove(adaptive_child)

    def get_ancestors(self, nodes: int = -1) -> MetadataList[Self]:
        """Retrieve MetadataList of all ancestors of wdadaptivepy member.

        Args:
            nodes: Number of nodes in the hierarchy to traverse

        Returns:
            MetadataList of all ancestors

        """
        ancestors = MetadataList[Self]()
        if self.adaptive_parent:
            ancestors.append(self.adaptive_parent)
            if nodes != 0:
                ancestors.extend(self.adaptive_parent.get_ancestors(nodes=nodes - 1))
        return ancestors

    def get_descendents(self, nodes: int = -1) -> MetadataList[Self]:
        """Retrieve MetadataList of all descendents of wdadaptivepy member.

        Args:
            nodes: Number of nodes in the hierarchy to traverse

        Returns:
            MetadataList of all descendents

        """
        descendents = MetadataList[Self]()
        if self.adaptive_children:
            descendents.extend(self.adaptive_children)
            if nodes != 0:
                for child in self.adaptive_children:
                    descendents.extend(child.get_descendents(nodes=nodes - 1))
        return descendents

    @classmethod
    def get_common_ancestors(cls, members: Sequence[Self]) -> MetadataList[Self]:  # NOQA: PLR0912 C901
        """Retrieve MetadataList of shared ancestors of all given members.

        Args:
            members: wdadaptivepy members to check for common ancestors

        Returns:
            MetadataList of common ancestors

        """
        common_ancestor = None
        common_ancestors = MetadataList[Self]()
        for member in members:
            if common_ancestor:
                member_ancestors = member.get_ancestors()
                found = False
                for index, ancestor in enumerate(member_ancestors):
                    if ancestor in common_ancestors:
                        found = True
                        if index > 0:
                            common_ancestors.extend(member_ancestors[:index])
                        break
                if not found:
                    if member.adaptive_parent is None:
                        common_ancestors.insert(0, member)
                    new_ancestors = common_ancestors[0].get_ancestors()
                    for index, new_ancestor in enumerate(new_ancestors):
                        if new_ancestor in member_ancestors:
                            common_ancestor = new_ancestor
                            common_ancestors = (
                                common_ancestors + new_ancestors[: index + 1]
                            )
                            common_ancestors = (
                                common_ancestors
                                + member_ancestors[
                                    : member_ancestors.index(new_ancestor) + 1
                                ]
                            )
                            break
            else:
                if member.adaptive_parent is None:
                    common_ancestor = member
                else:
                    common_ancestor = member.adaptive_parent
                common_ancestors.append(common_ancestor)
        if common_ancestor is None or common_ancestors == []:
            raise ValueError

        ordered_ancestors = MetadataList[Self]([common_ancestor])
        common_ancestors.remove(common_ancestor)
        while common_ancestors:
            for ancestor in reversed(common_ancestors):
                if ancestor in ordered_ancestors:
                    common_ancestors.remove(ancestor)
                elif ancestor.adaptive_parent is None:
                    common_ancestors.remove(ancestor)
                    ordered_ancestors.append(ancestor)
                elif ancestor.adaptive_parent in ordered_ancestors:
                    common_ancestors.remove(ancestor)
                    index = ordered_ancestors.index(ancestor.adaptive_parent) + 1
                    ordered_ancestors.insert(index, ancestor)
        return ordered_ancestors


class MetadataAttribute(BaseMetadata, BaseModel):
    """Attributes of BaseMetadata members.

    Attributes:
        attribute_id: Adaptive Attribute ID
        name: Adaptive Attribute Name
        value_id: Adaptive Attribute Value ID
        value: Adaptive Attribute Value Name

    """

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")

    attribute_id: Annotated[
        int | None,
        BeforeValidator(int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="attributeId",
                    serializer=int_to_str,
                ),
            ],
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
                ),
            ],
        ),
    ] = None
    value_id: Annotated[
        int | None,
        BeforeValidator(nullable_int_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="valueId",
                    serializer=int_to_str,
                ),
            ],
        ),
    ] = None
    value: Annotated[
        str | None,
        BeforeValidator(str_or_none),
        FieldMetadata(
            xml=[
                FieldXMLMetadata(
                    xml_version="default",
                    default_tag="value",
                    serializer=str_to_str,
                ),
            ],
        ),
    ] = None

    _xml_tags: ClassVar[list[ClassXMLMetadata]] = [
        ClassXMLMetadata(
            xml_version="default",
            default_parent_tag="attributes",
            default_tag="attribute",
        )
    ]


class BaseAttributtedMetadata(BaseModel, ABC):
    """Base class for all Adaptive metadata with attributes.

    Attributes:
        attributes: Adaptive Attributes

    """

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")

    attributes: Sequence[MetadataAttribute] = Field(
        default_factory=MetadataList[MetadataAttribute],
        exclude=True,
    )
    _adaptive_attributes: MetadataList[MetadataAttribute] = PrivateAttr(
        default_factory=MetadataList[MetadataAttribute]
    )

    def model_post_init(self, context: Any) -> None:  # noqa: ANN401
        """Cleanup BaseAttributtedMetadata instance."""
        for attribute in self.attributes:
            self.set_adaptive_attribute(attribute)
        del self.attributes
        if hasattr(super(), "model_post_init"):
            super().model_post_init(context)

    @computed_field
    @property
    def adaptive_attributes(self) -> MetadataList[MetadataAttribute]:
        """Adaptive Attributes of member.

        Returns:
            MetadataList of Attributes

        """
        return self._adaptive_attributes

    def set_adaptive_attribute(self, adaptive_attribute: MetadataAttribute) -> None:
        """Set Adaptive Attribute for member.

        Args:
            adaptive_attribute: Adaptive Attribute

        """
        if adaptive_attribute not in self._adaptive_attributes:
            for index, attribute in enumerate(iterable=self._adaptive_attributes):
                if attribute.attribute_id == adaptive_attribute.attribute_id:
                    self._adaptive_attributes[index] = adaptive_attribute
                    return
            self._adaptive_attributes.append(adaptive_attribute)

    def remove_adaptive_attribute(
        self,
        adaptive_attribute: MetadataAttribute | None = None,
        adaptive_attribute_id: int | None = None,
        adaptive_attribute_name: str | None = None,
    ) -> None:
        """Remove Adaptive Attribute from member.

        Args:
            adaptive_attribute: Adaptive Attribute
            adaptive_attribute_id: Adaptive Attribute ID
            adaptive_attribute_name: Adaptive Attribute Name

        """
        attribute_id = 0
        if adaptive_attribute is not None:
            attribute_id = adaptive_attribute.attribute_id
        elif adaptive_attribute_id is not None:
            attribute_id = adaptive_attribute_id
        for index, attribute in enumerate(iterable=self._adaptive_attributes):
            if (attribute.attribute_id == attribute_id) or (
                attribute_id == 0 and attribute.name == adaptive_attribute_name
            ):
                self._adaptive_attributes[index] = MetadataAttribute(
                    attribute_id=self._adaptive_attributes[index].attribute_id,
                    name=self._adaptive_attributes[index].name,
                    value_id=0,
                    value="",
                )
                return


class Metadata(BaseMetadata, BaseModel):
    """Class for Adaptive Metadata."""

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")


class HierchialMetadata(BaseHierarchialMetadata, BaseMetadata, BaseModel):
    """Calss for Hierarchial Adaptive Metadata."""

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")


class AttributedMetadata(BaseAttributtedMetadata, BaseMetadata):
    """Class for Attributed Adaptive Metadata."""

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")


class HierarchialAttributedMetadata(
    BaseHierarchialMetadata,
    BaseAttributtedMetadata,
    BaseMetadata,
    BaseModel,
):
    """Class for Hierarchial, Attributed Adaptive Metadata."""

    model_config = ConfigDict(validate_assignment=True, strict=False, extra="ignore")
