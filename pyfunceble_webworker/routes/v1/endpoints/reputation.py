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

This is the module that provides the endpoints related to the reputation checker.

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

from fastapi import APIRouter, Body, Depends
from PyFunceble import (
    DomainAndIPReputationChecker,
    DomainReputationChecker,
    IPReputationChecker,
    URLReputationChecker,
)

from pyfunceble_webworker.models.reputation import CheckerParams, ReputationStatus

router = APIRouter()


@router.post(
    "/domain",
    response_model=ReputationStatus,
    summary="Domain Reputation Checker",
    description="Checks the reputation of the given subject against our domain "
    "reputation checker.",
)
def domain_reputation(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the reputation of the given domain.
    """

    return ReputationStatus(
        **DomainReputationChecker(
            subject, do_syntax_check_first=params.do_syntax_check_first
        )
        .get_status()
        .to_dict()
    )


@router.post(
    "/url",
    response_model=ReputationStatus,
    summary="URL Reputation Checker",
    description="Checks the reputation of the given URL against our URL "
    "reputation checker.",
)
def url_reputation(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the reputation of the given URL.
    """

    return ReputationStatus(
        **URLReputationChecker(
            subject, do_syntax_check_first=params.do_syntax_check_first
        )
        .get_status()
        .to_dict()
    )


@router.post(
    "/domain-and-ip",
    response_model=ReputationStatus,
    summary="Domain Reputation Checker",
    description="Checks the reputation of the given subject against our "
    "domain and IP (v4 & v6) reputation checker.",
)
def domain_ip_reputation(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the reputation of the given domain or IP.
    """

    return ReputationStatus(
        **DomainAndIPReputationChecker(
            subject, do_syntax_check_first=params.do_syntax_check_first
        )
        .get_status()
        .to_dict()
    )


@router.post(
    "/ip",
    response_model=ReputationStatus,
    summary="IP Reputation Checker",
    description="Checks the reputation of the given subject against our IP "
    "(v4 & v6) reputation checker.",
)
def ip_reputation(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the reputation of the given IP.
    """

    return ReputationStatus(
        **IPReputationChecker(
            subject, do_syntax_check_first=params.do_syntax_check_first
        )
        .get_status()
        .to_dict()
    )
