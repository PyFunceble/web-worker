"""
This project is part of the PyFunceble project. The objective of this project
is to provide the PyFunceble project behind a Web REST API.

::


    ██████╗ ██╗   ██╗███████╗██╗   ██╗███╗   ██╗ ██████╗███████╗██████╗ ██╗     ███████╗
    ██╔══██╗╚██╗ ██╔╝██╔════╝██║   ██║████╗  ██║██╔════╝██╔════╝██╔══██╗██║     ██╔════╝
    ██████╔╝ ╚████╔╝ █████╗  ██║   ██║██╔██╗ ██║██║     █████╗  ██████╔╝██║     █████╗
    ██╔═══╝   ╚██╔╝  ██╔══╝  ██║   ██║██║╚██╗██║██║     ██╔══╝  ██╔══██╗██║     ██╔══╝
    ██║        ██║   ██║     ╚██████╔╝██║ ╚████║╚██████╗███████╗██████╔╝███████╗███████╗
    ╚═╝        ╚═╝   ╚═╝      ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝╚══════╝╚═════╝ ╚══════╝╚══════╝

This is the module that provides the endpoints related to the converter of
PyFunceble.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Special thanks:
    https://pyfunceble.github.io/#/special-thanks

Contributors:
    https://pyfunceble.github.io/#/contributors

PyFunceble link:
    https://github.com/funilrys/PyFunceble

PyFunceble documentation:
    https://pyfunceble.readthedocs.io/en/dev/

PyFunceble homepage:
    https://pyfunceble.github.io/

License:
::


    Copyright 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 Nissar Chababy

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from typing import List, Optional

from fastapi import APIRouter, Body, Query
from PyFunceble.checker.syntax.ip import IPSyntaxChecker
from PyFunceble.converter.adblock_input_line2subject import AdblockInputLine2Subject
from PyFunceble.converter.cidr2subject import CIDR2Subject
from PyFunceble.converter.input_line2subject import InputLine2Subject
from PyFunceble.converter.rpz_input_line2subject import RPZInputLine2Subject
from PyFunceble.converter.rpz_policy2subject import RPZPolicy2Subject
from PyFunceble.converter.subject2complements import Subject2Complements
from PyFunceble.converter.wildcard2subject import Wildcard2Subject

router = APIRouter(prefix="/converter")


@router.post(
    "/complements",
    response_model=List[str],
    summary="Complements Finder",
    description="Provides the complements of the given subject.",
)
def complements(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    include_given: bool = Query(False, summary="Include Given", description=""),
):
    """
    Provides the complements of the given subject.
    """

    return Subject2Complements(subject, include_given=include_given).get_converted()


@router.post(
    "/adblock",
    response_model=List[str],
    summary="AdBlock Filter Line Decoder",
    description="Decodes the subjects of the given AdBlock filter line",
)
def adblock(
    *,
    data: str = Body(
        ..., embed=True, summary="Data", description="The data to convert."
    ),
    aggressive: bool = Query(
        False,
        summary="Aggressive Mode",
        description="Activates the conversion in a more aggressive mater.",
    ),
) -> List[str]:
    """
    Provides the conversion of the testable subject of the given AdBlock filter
    list.
    """

    return AdblockInputLine2Subject(
        data_to_convert=data, aggressive=aggressive
    ).get_converted()


@router.post(
    "/cidr",
    response_model=List[str],
    summary="CIDR Converter",
    description="Provides the list of IPv4 from the given IPv4 range.",
)
def cidr(
    *,
    data: str = Body(
        ..., embed=True, summary="Data", description="The data to convert."
    ),
) -> List[str]:
    """
    Provides the conversion of an IPv4 range to a list of IP.
    """

    if IPSyntaxChecker(data).is_valid_v4_range():
        return CIDR2Subject(data_to_convert=data).get_converted()

    return []


@router.post(
    "/wildcard",
    response_model=str,
    summary="Wildcard Converter",
    description="Provides the single subject to test from the given wildcard.",
)
def wildcard(
    *,
    data: str = Body(
        ..., embed=True, summary="Data", description="The data to convert."
    ),
) -> List[str]:
    """
    Provides the conversion of a wildcard converter to a testable subject.
    """

    return Wildcard2Subject(data_to_convert=data).get_converted()


@router.post(
    "/hosts",
    response_model=List[str],
    summary="Hosts Line Converter",
    description="Provides the subjects from the given hosts file line.",
)
def hosts(
    *,
    data: str = Body(
        ..., embed=True, summary="Data", description="The data to convert."
    ),
) -> List[str]:
    """
    Provides the testable subjects from the given hosts file line.
    """

    return InputLine2Subject(data_to_convert=data).get_converted()


@router.post(
    "/plain",
    response_model=List[str],
    summary="Plain Line Converter",
    description="Provides the subjects from the line.",
)
def plain(
    *,
    data: str = Body(
        ..., embed=True, summary="Data", description="The data to convert."
    ),
) -> List[str]:
    """
    Provides the testable subjects from the line.
    """

    return InputLine2Subject(data_to_convert=data).get_converted()


@router.post(
    "/rpz",
    response_model=List[str],
    summary="RPZ Policy Converter",
    description="Provides the subject from the given RPZ policy.",
)
def rpz(
    *,
    data: str = Body(
        ..., embed=True, summary="Data", description="The data to convert."
    ),
    soas: Optional[List[str]] = Body(
        ...,
        embed=True,
        summary="SOAs",
        description="The list of SOAs to take into consideration.",
    ),
) -> List[str]:
    """
    Provides the testable subjects from the given RPZ policy.
    """

    rpz_inputline2subject = RPZInputLine2Subject()
    rpz_policy2subject = RPZPolicy2Subject(soas=soas)

    return [
        rpz_policy2subject.set_data_to_convert(x).get_converted()
        for x in rpz_inputline2subject.set_data_to_convert(data).get_converted()
    ]
