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

This is the module that provides the endpoints related to the syntax checker.

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


    Copyright 2017, 2018, 2019, 2020, 2021 Nissar Chababy

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

from fastapi import APIRouter, Body
from PyFunceble import DomainSyntaxChecker, IPSyntaxChecker, URLSyntaxChecker

from pyfunceble_webworker.models.syntax import SyntaxStatus

router = APIRouter(prefix="/syntax")


@router.post(
    "/domain",
    response_model=SyntaxStatus,
    summary="Domain Syntax Checker",
    description="Checks the syntax of the given subject against our domain "
    "syntax checker.",
)
def domain_syntax(
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    )
):
    """
    Checks the syntax of the given domain.
    """

    return DomainSyntaxChecker(subject).get_status().to_dict()


@router.post(
    "/ip",
    response_model=SyntaxStatus,
    summary="IP Syntax Checker",
    description="Checks the syntax of the given subject against our IP "
    "(v4 & v6) syntax checker.",
)
def ip_syntax(
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    )
):
    """
    Checks the syntax of the given IP (v4 or v6).
    """

    return IPSyntaxChecker(subject).get_status().to_dict()


@router.post(
    "/url",
    response_model=SyntaxStatus,
    summary="URL Syntax Checker",
    description="Checks the syntax of the given subject against our url "
    "syntax checker.",
)
def url_syntax(
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    )
):
    """
    Checks the syntax of the given URL.
    """

    return URLSyntaxChecker(subject).get_status().to_dict()
