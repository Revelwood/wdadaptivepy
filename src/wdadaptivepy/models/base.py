"""wdadaptivepy base model for Adaptive's metadata."""

from collections.abc import Callable, Sequence
from dataclasses import InitVar, dataclass, field, fields
from json import loads
from typing import Any, ClassVar, Self
from xml.etree import ElementTree as ET

from wdadaptivepy.models.list import MetadataList


def bool_or_none(value: str | int | bool | None) -> bool | None:  # NOQA: FBT001
    """Convert a value to either boolean or None.

    Args:
        value: Value to convert to boolean or None

    Returns:
        Boolean value or None

    Raises:
        ValueError: Unexpected value
        TypeError: Unexpected type

    """
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        if value == 1:
            return True
        if value == 0:
            return False
        error_message = "Invalid boolean value"
        raise ValueError(error_message)
    if isinstance(value, str):
        if value.lower() in ["true", "t", "y", "yes", "1"]:
            return True
        if value.lower() in ["false", "f", "n", "no", "0"]:
            return False
        if value == "":
            return None
        error_message = "Invalid boolean value"
        raise ValueError(error_message)
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def bool_to_str_one_zero(value: bool | None) -> str | None:  # NOQA: FBT001
    """Convert boolean to string value of 1 or 0.

    Args:
        value: Value to convert to 1 or 0

    Returns:
        1 or 0 or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if value is True:
        return "1"
    if value is False:
        return "0"
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def bool_to_str_true_false(value: bool | None) -> str | None:  # NOQA: FBT001
    """Convert boolean to string of true or false.

    Args:
        value: Value to convert to true or fale

    Returns:
        true or false or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if value is True:
        return "true"
    if value is False:
        return "false"
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def bool_to_str_y_n(value: bool | None) -> str | None:  # NOQA: FBT001
    """Convert boolean to y or n.

    Args:
        value: Value to convert to y or n

    Returns:
        y or n or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if value is True:
        return "y"
    if value is False:
        return "n"
    error_message = "Unexpected type for boolean"
    raise TypeError(error_message)


def int_or_none(value: str | int | None) -> int | None:
    """Convert value to an integer or None.

    Args:
        value: Value to convert to integer or None

    Returns:
        integer or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(value)
    error_message = "Unexpected type for integer"
    raise TypeError(error_message)


def int_to_str(value: int | str | None) -> str | None:
    """Convert integer to string.

    Args:
        value: Value to convert to a string

    Returns:
        String

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        try:
            int_value = int(value)
            return str(int_value)
        except TypeError as e:
            error_message = "Unable to convert to integer"
            raise TypeError(error_message) from e
    error_message = "Unexpected type for integer"
    raise TypeError(error_message)


def nullable_int_or_none(value: str | int | None) -> str | None:
    """Convert integer to string.

    Args:
        value: Value to convert to string

    Returns:
        String or None

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        if value == "":
            return value
        return str(int(value))
    error_message = "Unexpected type for integer"
    raise TypeError(error_message)


def str_or_none(value: str | None) -> str | None:
    """Convert value to string.

    Args:
        value: Value to convert to string

    Returns:
        String

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    error_message = "Unexpected type for string"
    raise TypeError(error_message)


def str_to_str(value: str | None) -> str | None:
    """Convert string to string.

    Args:
        value: Value to convert to string

    Returns:
        String

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    error_message = "Unexpected type for string"
    raise TypeError(error_message)


def int_list_or_none(
    value: str | int | Sequence[int] | Sequence[str] | None,
) -> list[int] | None:
    """Convert to list of integers.

    Args:
        value: Value to convert to list of integers

    Returns:
       List of integers

    Raises:
        TypeError: Unexpected type

    """
    if value is None:
        return None
    if isinstance(value, str):
        return [int(value)]
    if isinstance(value, int):
        return [value]
    if isinstance(value, Sequence):
        return [int(x) for x in value]
    error_message = "unexpected type for integer list"
    raise TypeError(error_message)


def int_list_to_str(value: Sequence[int] | None) -> str | None:
    """Convert list of integers to string.

    Args:
        value: Value to convert to string

    Returns:
        Joined string from list of integers or None

    """
    if value is None:
        return value
    return ",".join([str(x) for x in value])


@dataclass(eq=False)
class BaseMetadata:
    """Base class for all Adaptive Metadata."""

    def __hash__(self) -> int:
        """Create a hash for a BaseMetadata instance.

        Returns:
            int hash value

        """
        return hash(getattr(self, f.name, None) for f in fields(self))

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
        for self_field in fields(self):
            self_value = getattr(self, self_field.name, None)
            other_value = getattr(other, self_field.name, None)
            if self_value != other_value:
                return False

        self_parent = getattr(self, "adaptive_parent", None)
        other_parent = getattr(other, "adaptive_parent", None)
        if self_parent != other_parent:
            return False

        self_attributes = getattr(self, "adaptive_attributes", None)
        other_attributes = getattr(other, "adaptive_attributes", None)
        return self_attributes == other_attributes

        # return True

    def __post_init__(self) -> None:
        """Cleanup BaseMetadata instance."""

    def __setattr__(self, name: str, value: Any, /) -> None:  # noqa: ANN401
        """Force data to appropriate data type.

        Args:
            name: Name of field to modify
            value: Value to modify

        Raises:
            RuntimeError: Unexpected value

        """
        if name not in self.__dataclass_fields__:
            super().__setattr__(name, value)
            return
        field_def = self.__dataclass_fields__[name]
        validator: Callable[[Any], Any] = field_def.metadata.get(
            "validator",
            lambda x: x,
        )
        new_value = validator(value)
        if (
            name == "id"
            and getattr(self, "id", None) is not None
            and getattr(self, "id", None) != new_value
        ):
            error_message = "Cannot change value of id"
            raise RuntimeError(error_message)
        super().__setattr__(name, validator(value))

    @classmethod
    def __parse_xml_to_metadata(
        cls: type[Self],
        xml_element: ET.Element,
        xml_tag: str,
        xml_children: dict | None,
        parent: Self | None,
        processed_xml_elements: list[ET.Element],
    ) -> MetadataList[Self]:
        processed_xml_elements.append(xml_element)
        metadata_data = {
            field_name: xml_element.get(field_def.metadata.get("xml_read"))
            for field_name, field_def in cls.__dataclass_fields__.items()
            if field_def.metadata.get("xml_read") in xml_element.attrib
        }
        metadata_member = cls(**metadata_data)
        metadata_members = MetadataList[Self]([metadata_member])
        if xml_children:
            for field_name, data_type in xml_children.items():
                child_xml_parent_tag = data_type.__dataclass_fields__[
                    f"_{data_type.__name__}__xml_tags"
                ].default["xml_read_parent_tag"]
                child_xml_tag = data_type.__dataclass_fields__[
                    f"_{data_type.__name__}__xml_tags"
                ].default["xml_read_tag"]
                if child_xml_tag is None or child_xml_parent_tag is None:
                    continue
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
        if hasattr(metadata_member, "adaptive_attributes"):
            adaptive_metadata_instance = MetadataAttribute()
            for metadata_element in xml_element.findall(
                f"./{adaptive_metadata_instance.__dataclass_fields__['_MetadataAttribute__xml_tags'].default['xml_read_parent_tag']}",
            ):
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
        if hasattr(metadata_member, "adaptive_parent"):
            if parent is not None:
                set_adaptive_parent: Callable | None = getattr(
                    metadata_member, "set_adaptive_parent", None
                )
                if set_adaptive_parent is not None:
                    set_adaptive_parent(parent)
            for xml_child_element in xml_element.findall(path=xml_tag):
                metadata_members.extend(
                    cls.__parse_xml_to_metadata(
                        xml_element=xml_child_element,
                        xml_tag=xml_tag,
                        xml_children=xml_children,
                        parent=metadata_member,
                        processed_xml_elements=processed_xml_elements,
                    )
                )

        return metadata_members

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

        cls_name = cls.__name__
        # xml_parent_tag = cls.__dataclass_fields__[f"_{cls_name}__xml_tags"].default[
        #     "xml_read_parent_tag"
        # ]
        xml_tag = cls.__dataclass_fields__[f"_{cls_name}__xml_tags"].default[
            "xml_read_tag"
        ]
        xml_children = cls.__dataclass_fields__[f"_{cls_name}__xml_tags"].default[
            "xml_read_children"
        ]
        if xml_tag is not None:
            processed_xml_elements: list[ET.Element] = []
            for xml_element in xml.iter(tag=xml_tag):
                if xml_element not in processed_xml_elements:
                    metadata_members.extend(
                        cls.__parse_xml_to_metadata(
                            xml_element=xml_element,
                            xml_tag=xml_tag,
                            xml_children=xml_children,
                            parent=None,
                            processed_xml_elements=processed_xml_elements,
                        )
                    )

        return metadata_members

    @classmethod
    def to_xml(cls: type[Self], xml_type: str, members: Sequence[Self]) -> ET.Element:  # NOQA: PLR0912, PLR0915
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
        cls_name = cls.__name__
        xml_parent_tag = cls.__dataclass_fields__[f"_{cls_name}__xml_tags"].default[
            f"xml_{xml_type}_parent_tag"
        ]
        xml_tag = cls.__dataclass_fields__[f"_{cls_name}__xml_tags"].default[
            f"xml_{xml_type}_tag"
        ]
        xml_children = cls.__dataclass_fields__[f"_{cls_name}__xml_tags"].default[
            f"xml_{xml_type}_children"
        ]
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


@dataclass(eq=False)
class BaseHierarchialMetadata:
    """Base class for hierarchial Adaptive metadata.

    Attributes:
        parent: wdadaptivepy BaseHierarchialMetadata parent
        children: wdadaptivepy BaseHierarchialMetadata children

    """

    parent: InitVar[Self | None] = None
    children: InitVar[Sequence[Self] | None] = None

    def __post_init__(
        self,
        parent: Self | None = None,  # NOQA: RUF033
        children: Sequence[Self] | None = None,  # NOQA: RUF033
    ) -> None:
        """Cleanup BaseHierarchialMetadata instance.

        Args:
            parent: Parent of BaseHierarchialMetadata member
            children: Children of BaseHierarchialMetadata member

        """
        self.__adaptive_parent = None
        self.__adaptive_children = MetadataList[Self]()
        self.set_adaptive_parent(parent)
        if children:
            for child in children:
                self.__add_adaptive_child(child)

    @property
    def adaptive_parent(self) -> Self | None:
        """Adaptive parent from hierarchy.

        Returns:
            wdadaptivepy parent

        """
        return self.__adaptive_parent

    @property
    def adaptive_children(self) -> MetadataList[Self]:
        """Adaptive children from hierarchy.

        Returns:
            wdadaptivepy MetadataList of children

        """
        return self.__adaptive_children

    def set_adaptive_parent(self, adaptive_parent: Self | None) -> None:
        """Assign parent of wdadaptivepy member.

        Args:
            adaptive_parent: wdadaptivepy parent member

        """
        if self == adaptive_parent:
            raise ValueError
        if self.__adaptive_parent != adaptive_parent:
            if adaptive_parent is not None:
                adaptive_parent.__add_adaptive_child(adaptive_child=self)  # noqa: SLF001
                if (
                    adaptive_parent.adaptive_parent is not None
                    and self == adaptive_parent.__adaptive_parent  # noqa: SLF001
                ):
                    adaptive_parent.set_adaptive_parent(
                        adaptive_parent=self.adaptive_parent,
                    )
            if self.__adaptive_parent is not None:
                self.__adaptive_parent.__remove_adaptive_child(adaptive_child=self)  # noqa: SLF001
            self.__adaptive_parent = adaptive_parent

    def __add_adaptive_child(self, adaptive_child: Self) -> None:
        if adaptive_child not in self.__adaptive_children:
            self.__adaptive_children.append(adaptive_child)

    def __remove_adaptive_child(self, adaptive_child: Self) -> None:
        self.__adaptive_children.remove(adaptive_child)

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
    def get_common_ancestors(cls, members: Sequence[Self]) -> MetadataList[Self]:  # NOQA: PLR0912
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


@dataclass(eq=False)
class MetadataAttribute(BaseMetadata):
    """Attributes of BaseMetadata members.

    Attributes:
        attribute_id: Adaptive Attribute ID
        name: Adaptive Attribute Name
        value_id: Adaptive Attribute Value ID
        value: Adaptive Attribute Value Name
        __xml_tags: wdadaptivepy XML tags

    """

    attribute_id: int | None = field(
        default=None,
        metadata={
            "validator": int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "attributeId",
            "xml_read": "attributeId",
            "xml_update": "",
            "xml_delete": "attributeId",
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
    value_id: int | None = field(
        default=None,
        metadata={
            "validator": nullable_int_or_none,
            "xml_parser": int_to_str,
            "xml_create": "",
            "xml_read": "valueId",
            "xml_update": "",
            "xml_delete": "",
        },
    )
    value: str | None = field(
        default=None,
        metadata={
            "validator": str_or_none,
            "xml_parser": str_to_str,
            "xml_create": "value",
            "xml_read": "value",
            "xml_update": "value",
            "xml_delete": "value",
        },
    )
    __xml_tags: ClassVar[dict[str, str | dict[str, type]]] = {
        "xml_create_parent_tag": "attributes",
        "xml_create_tag": "attribute",
        "xml_create_children": {},
        "xml_read_parent_tag": "attributes",
        "xml_read_tag": "attribute",
        "xml_read_children": {},
        "xml_update_parent_tag": "attributes",
        "xml_update_tag": "attribute",
        "xml_update_children": {},
        "xml_delete_parent_tag": "attributes",
        "xml_delete_tag": "attribute",
        "xml_delete_children": {},
    }


@dataclass(eq=False)
class BaseAttributtedMetadata:
    """Base class for all Adaptive metadata with attributes.

    Attributes:
        attributes: Adaptive Attributes

    """

    attributes: InitVar[Sequence[MetadataAttribute] | None] = None

    def __post_init__(
        self,
        attributes: Sequence[MetadataAttribute] | None = None,  # NOQA: RUF033
    ) -> None:
        """Cleanup BaseAttributtedMetadata instance.

        Args:
            attributes: Adaptive Attributes

        """
        self.__adaptive_attributes = MetadataList[MetadataAttribute]()
        if attributes:
            for attribute in attributes:
                self.set_adaptive_attribute(attribute)

    @property
    def adaptive_attributes(self) -> MetadataList[MetadataAttribute]:
        """Adaptive Attributes of member.

        Returns:
            MetadataList of Attributes

        """
        return self.__adaptive_attributes

    def set_adaptive_attribute(self, adaptive_attribute: MetadataAttribute) -> None:
        """Set Adaptive Attribute for member.

        Args:
            adaptive_attribute: Adaptive Attribute

        """
        if adaptive_attribute not in self.__adaptive_attributes:
            for index, attribute in enumerate(iterable=self.__adaptive_attributes):
                if attribute.attribute_id == adaptive_attribute.attribute_id:
                    self.__adaptive_attributes[index] = adaptive_attribute
                    return
            self.__adaptive_attributes.append(adaptive_attribute)

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
        for index, attribute in enumerate(iterable=self.__adaptive_attributes):
            if (attribute.attribute_id == attribute_id) or (
                attribute_id == 0 and attribute.name == adaptive_attribute_name
            ):
                self.__adaptive_attributes[index] = MetadataAttribute(
                    attribute_id=self.__adaptive_attributes[index].attribute_id,
                    name=self.__adaptive_attributes[index].name,
                    value_id=0,
                    value="",
                )
                return


@dataclass(eq=False)
class Metadata(BaseMetadata):
    """Class for Adaptive Metadata."""

    def __post_init__(self) -> None:
        """Clean up Metadata instance."""
        BaseMetadata.__post_init__(self)


@dataclass(eq=False)
class HierchialMetadata(BaseHierarchialMetadata, BaseMetadata):
    """Calss for Hierarchial Adaptive Metadata."""

    def __post_init__(
        self,
        parent: Self | None = None,  # NOQA: RUF033
        children: Sequence[Self] | None = None,  # NOQA: RUF033
    ) -> None:
        """Clean up HierchialMetadata instance.

        Args:
            parent: Adaptive parent
            children: Adaptive children

        """
        BaseHierarchialMetadata.__post_init__(self, parent=parent, children=children)
        BaseMetadata.__post_init__(self)


@dataclass(eq=False)
class AttributedMetadata(BaseAttributtedMetadata, BaseMetadata):
    """Class for Attributed Adaptive Metadata."""

    def __post_init__(
        self,
        attributes: Sequence[MetadataAttribute] | None = None,  # NOQA: RUF033
    ) -> None:
        """Clean up AttributedMetadata instance.

        Args:
            attributes: Adaptive Attributes

        """
        BaseAttributtedMetadata.__post_init__(self, attributes=attributes)
        BaseMetadata.__post_init__(self)


@dataclass(eq=False)
class HierarchialAttributedMetadata(
    BaseHierarchialMetadata,
    BaseAttributtedMetadata,
    BaseMetadata,
):
    """Class for Hierarchial, Attributed Adaptive Metadata."""

    def __post_init__(
        self,
        attributes: Sequence[MetadataAttribute] | None = None,  # NOQA: RUF033
        parent: Self | None = None,  # NOQA: RUF033
        children: Sequence[Self] | None = None,  # NOQA: RUF033
    ) -> None:
        """Clean up HierarchialAttributedMetadata instance.

        Args:
            attributes: Adaptive Attributes
            parent: Adaptive parent
            children: Adaptive children

        """
        BaseHierarchialMetadata.__post_init__(self, parent=parent, children=children)
        BaseAttributtedMetadata.__post_init__(self, attributes=attributes)
        BaseMetadata.__post_init__(self)
