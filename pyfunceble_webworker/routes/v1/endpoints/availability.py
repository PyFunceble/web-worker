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

This is the module that provides the endpoints related to the availability checker.

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

from typing import Optional

from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from PyFunceble import (
    DomainAndIPAvailabilityChecker,
    DomainAvailabilityChecker,
    IPAvailabilityChecker,
    URLAvailabilityChecker,
)

from pyfunceble_webworker.core.settings import core_settings
from pyfunceble_webworker.models.availability import (
    AvailabilityStatus,
    CheckerParams,
    URLCheckerParams,
)

router = APIRouter()


@router.post(
    "/domain",
    response_model=AvailabilityStatus,
    summary="Domain Availability Checker",
    description="Checks the availability of the given subject against our domain "
    "availability checker.",
)
def domain_availability(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the availability of the given domain.
    """

    if core_settings.ALLOW_WHOIS_LOOKUP_PARAM:
        use_whois_lookup = params.use_whois_lookup
    else:
        use_whois_lookup = core_settings.ALLOW_WHOIS_LOOKUP

    return AvailabilityStatus(
        **DomainAvailabilityChecker(
            subject,
            use_extra_rules=params.use_extra_rules,
            use_whois_lookup=use_whois_lookup,
            use_dns_lookup=params.use_dns_lookup,
            use_netinfo_lookup=params.use_netinfo_lookup,
            use_http_code_lookup=params.use_http_code_lookup,
            use_reputation_lookup=params.use_reputation_lookup,
            do_syntax_check_first=params.do_syntax_check_first,
            use_whois_db=False,
        )
        .get_status()
        .to_dict()
    )


@router.post(
    "/url",
    response_model=AvailabilityStatus,
    summary="URL Availability Checker",
    description="Checks the availability of the given subject against our url "
    "availability checker.",
)
def url_availability(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: URLCheckerParams = Depends()
):
    """
    Checks the availability of the given domain.
    """

    if core_settings.ALLOW_WHOIS_LOOKUP_PARAM:
        use_whois_lookup = params.use_whois_lookup
    else:
        use_whois_lookup = core_settings.ALLOW_WHOIS_LOOKUP

    return AvailabilityStatus(
        **URLAvailabilityChecker(
            subject,
            use_extra_rules=False,
            use_whois_lookup=use_whois_lookup,
            use_dns_lookup=False,
            use_netinfo_lookup=False,
            use_http_code_lookup=True,
            use_reputation_lookup=params.use_reputation_lookup,
            do_syntax_check_first=params.do_syntax_check_first,
            use_whois_db=False,
        )
        .get_status()
        .to_dict()
    )


@router.post(
    "/ip",
    response_model=AvailabilityStatus,
    summary="IP Availability Checker",
    description="Checks the availability of the given subject against our IP "
    "(v4 & v6) availability checker.",
)
def ip_availability(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the availability of the given IP.
    """

    if core_settings.ALLOW_WHOIS_LOOKUP_PARAM:
        use_whois_lookup = params.use_whois_lookup
    else:
        use_whois_lookup = core_settings.ALLOW_WHOIS_LOOKUP

    return AvailabilityStatus(
        **IPAvailabilityChecker(
            subject,
            use_extra_rules=params.use_extra_rules,
            use_whois_lookup=use_whois_lookup,
            use_dns_lookup=params.use_dns_lookup,
            use_netinfo_lookup=params.use_netinfo_lookup,
            use_http_code_lookup=params.use_http_code_lookup,
            use_reputation_lookup=params.use_reputation_lookup,
            do_syntax_check_first=params.do_syntax_check_first,
            use_whois_db=False,
        )
        .get_status()
        .to_dict()
    )


@router.post(
    "/domain-and-ip",
    response_model=AvailabilityStatus,
    summary="Domain & IP Availability Checker",
    description="Checks the availability of the given subject against our "
    "domain and IP (v4 & v6) availability checker.",
)
def domain_ip_availability(
    *,
    subject: str = Body(
        ..., embed=True, summary="Subject", description="The subject to work with."
    ),
    params: CheckerParams = Depends()
):
    """
    Checks the availability of the given domain or IP.
    """

    if core_settings.ALLOW_WHOIS_LOOKUP_PARAM:
        use_whois_lookup = params.use_whois_lookup
    else:
        use_whois_lookup = core_settings.ALLOW_WHOIS_LOOKUP

    return AvailabilityStatus(
        **DomainAndIPAvailabilityChecker(
            subject,
            use_extra_rules=params.use_extra_rules,
            use_whois_lookup=use_whois_lookup,
            use_dns_lookup=params.use_dns_lookup,
            use_netinfo_lookup=params.use_netinfo_lookup,
            use_http_code_lookup=params.use_http_code_lookup,
            use_reputation_lookup=params.use_reputation_lookup,
            do_syntax_check_first=params.do_syntax_check_first,
            use_whois_db=False,
        )
        .get_status()
        .to_dict()
    )
