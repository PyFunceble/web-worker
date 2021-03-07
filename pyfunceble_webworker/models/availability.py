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

This is the module that provides our availability checker models.

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

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from fastapi import Query
from pydantic import BaseModel

from pyfunceble_webworker.core.settings import core_settings
from pyfunceble_webworker.models.records import (
    StatusDNSLookupRecord,
    StatusWhoisLookupRecord,
)


class CheckerParams(BaseModel):
    use_extra_rules: bool = Query(
        True,
        embed=True,
        summary="Use extra rules",
        description="Asks PyFunceble to use - or not - its extra rules.",
    )

    if core_settings.ALLOW_WHOIS_LOOKUP_PARAM:
        use_whois_lookup: bool = Query(
            core_settings.ALLOW_WHOIS_LOOKUP,
            embed=True,
            summary="Process WHOIS lookup",
            description="Asks PyFunceble to process and use - or not - the result "
            "of the WHOIS lookup.",
        )

    use_dns_lookup: bool = Query(
        True,
        embed=True,
        summary="Process DNS lookup",
        description="Asks PyFunceble to process and use - or not - the result "
        "of the DNS lookup",
    )

    use_netinfo_lookup: bool = Query(
        False,
        embed=True,
        summary="Process NETINFO lookup",
        description="Asks PyFunceble to process and use - or not - the result "
        "of the NETINFO lookup.",
    )

    use_http_code_lookup: bool = Query(
        True,
        embed=True,
        summary="Process HTTP CODE lookup",
        description="Asks PyFunceble to process and use - or not - the result "
        "of the HTTP CODE lookup.",
    )

    use_reputation_lookup: bool = Query(
        False,
        embed=True,
        summary="Process REPUTATION lookup",
        description="Asks PyFunceble to process and use - or not - the result "
        "of the REPUTATION lookup.",
    )

    do_syntax_check_first: bool = Query(
        True,
        embed=True,
        summary="Process SYNTAX check first",
        description="Asks PyFunceble to first check the syntax first.",
    )


class URLCheckerParams(BaseModel):
    use_reputation_lookup: bool = Query(
        False,
        embed=True,
        summary="Process REPUTATION lookup",
        description="Asks PyFunceble to process and use - or not - the result "
        "of the REPUTATION lookup.",
    )

    do_syntax_check_first: bool = Query(
        True,
        embed=True,
        summary="Process SYNTAX check first",
        description="Asks PyFunceble to first check the syntax first.",
    )


class Status(Enum):
    active: str = "ACTIVE"
    inactive: str = "INACTIVE"
    invalid: str = "INVALID"


class StatusParams(BaseModel):
    do_syntax_check_first: Optional[bool] = None
    use_extra_rules: Optional[bool] = None
    use_whois_lookup: Optional[bool] = None
    use_dns_lookup: Optional[bool] = None
    use_netinfo_lookup: Optional[bool] = None
    use_http_code_lookup: Optional[bool] = None
    use_reputation_lookup: Optional[bool] = None
    use_whois_db: Optional[bool] = None


class AvailabilityStatusBase(BaseModel):
    subject: str
    idna_subject: str
    status: Status
    status_source: str
    tested_at: datetime


class AvailabilityStatusExtended(AvailabilityStatusBase):

    domain_syntax: Optional[bool] = None
    second_level_domain_syntax: Optional[bool] = None
    subdomain_syntax: Optional[bool] = None

    ip_syntax: Optional[bool] = None
    ipv4_syntax: Optional[bool] = None
    ipv6_syntax: Optional[bool] = None
    ipv4_range_syntax: Optional[bool] = None
    ipv6_range_syntax: Optional[bool] = None
    url_syntax: Optional[bool] = None

    expiration_date: Optional[str] = None

    status_before_extra_rules: Optional[str] = None
    status_after_extra_rules: Optional[str] = None

    status_source_before_extra_rules: Optional[str] = None
    status_source_after_extra_rules: Optional[str] = None

    dns_lookup: Optional[Dict[str, Optional[List[str]]]] = None
    netinfo: Optional[Dict[str, Optional[List[str]]]] = None
    http_status_code: Optional[int] = None

    dns_lookup_record: Optional[StatusDNSLookupRecord] = None
    whois_lookup_record: Optional[StatusWhoisLookupRecord] = None


class AvailabilityStatus(AvailabilityStatusExtended):
    params: StatusParams
