"""Class to connect to Adaptive's XML API."""

from collections.abc import Sequence
from dataclasses import dataclass
from xml.etree import ElementTree as ET

import requests

from wdadaptivepy.connectors.xml_api.constants import (
    BASE_URL,
    DEFAULT_CALLER_NAME,
    MINIMUM_VERSION,
)
from wdadaptivepy.connectors.xml_api.exceptions import (
    FailedRequestError,
    InvalidCredentialsError,
)


@dataclass
class XMLApi:
    """Class to handle all XML API related methods.

    Attributes:
        login: Adaptive username/login
        password: Adaptive password
        locale: Locale for text translations and data formats
        instance_code: Adaptive tenant/instance code
        caller_name: Identifier used within Adaptive's logs
        version: Version of Adaptive's XML API

    """

    login: str
    password: str
    locale: str | None = None  # add default Locale and make it an enum
    instance_code: str | None = None
    caller_name: str = DEFAULT_CALLER_NAME
    version: int = MINIMUM_VERSION

    def __generate_xml_call(
        self,
        method: str,
        payload: ET.Element | Sequence[ET.Element] | None,
    ) -> ET.Element:
        call = ET.Element(
            "call",
            attrib={"method": method, "callerName": self.caller_name},
        )
        credentials = ET.Element(
            "credentials",
            attrib={
                "login": self.login,
                "password": self.password,
            },
        )
        if self.locale:
            credentials.attrib["locale"] = self.locale
        if self.instance_code:
            credentials.attrib["instanceCode"] = self.instance_code
        call.append(credentials)
        if payload is not None:
            if isinstance(payload, ET.Element):
                call.append(payload)
            elif isinstance(payload, Sequence):
                if not all(isinstance(element, ET.Element) for element in payload):
                    error_message = "Expected XML Element Tree Element"
                    raise TypeError(error_message)
                call.extend(payload)
        return call

    def preview_xml_request(
        self,
        method: str,
        payload: ET.Element | Sequence[ET.Element] | None,
        *,
        hide_password: bool = True,
    ) -> ET.Element:
        """Generate XML call body (does not send to Adaptive) for review.

        Args:
            method: Adaptive XML API name
            payload: Body of XML API call
            hide_password: Hide password from output

        Returns:
            XML Element of API call

        """
        call = self.__generate_xml_call(method, payload)
        credentials = call.find("credentials")
        if hide_password is True and credentials is not None:
            credentials.attrib["password"] = "*" * len(credentials.attrib["password"])
        return call

    def make_xml_request(
        self,
        method: str,
        payload: ET.Element | Sequence[ET.Element] | None,
    ) -> ET.Element:
        """Send API call to Adaptive.

        Args:
            method: Adaptive XML API name
            payload:Body of XML API call

        Returns:
            XML Element of API response

        Raises:
            InvalidCredentialsError: Exception indicating the credentials are invalid
            FailedRequestError: Exception indicating the API request was unsuccessful

        """
        call = self.__generate_xml_call(method, payload)

        request_headers = {"Content-Type": "application/xml"}
        response = requests.post(
            url=BASE_URL + "v" + str(MINIMUM_VERSION),
            data=ET.tostring(call),
            headers=request_headers,
            timeout=(10, 30 * 60),
        )

        tree = ET.fromstring(text=response.text)  # NOQA: S314

        messages = tree.find(path="messages")
        if messages is not None:
            for message in messages.findall(path="message"):
                if (
                    "key" in message.attrib
                    and message.attrib["key"] == "error-authentication-failure"
                ):
                    error_message = (
                        "The provided credentials are either incorrect "
                        "or the associated account does not "
                        "have access to the requested resource"
                    )
                    raise InvalidCredentialsError(error_message)
        if "success" in tree.attrib and tree.attrib["success"] != "true":
            raise FailedRequestError(
                message="The API request failed to complete successfully",
                method=method,
            )

        return tree
