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

This is the module that provides our reputation checker models.

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
from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel


class Status(Enum):
    sane: str = "SANE"
    malicious: str = "MALICIOUS"
    invalid: str = "INVALID"


class StatusParams(BaseModel):
    do_syntax_check_first: Optional[bool] = None


class CheckerParams(BaseModel):
    do_syntax_check_first: bool = Query(
        True,
        embed=True,
        summary="Process SYNTAX check first",
        description="Asks PyFunceble to first check the syntax first.",
    )


class ReputationStatusBase(BaseModel):
    subject: str
    idna_subject: str
    status: Status
    status_source: str
    tested_at: datetime


class ReputationStatusExtended(ReputationStatusBase):
    domain_syntax: Optional[bool] = None
    second_level_domain_syntax: Optional[bool] = None
    subdomain_syntax: Optional[bool] = None

    ip_syntax: Optional[bool] = None
    ipv4_syntax: Optional[bool] = None
    ipv6_syntax: Optional[bool] = None
    ipv4_range_syntax: Optional[bool] = None
    ipv6_range_syntax: Optional[bool] = None
    url_syntax: Optional[bool] = None

    dns_lookup: Optional[List[str]] = None


class ReputationStatus(ReputationStatusExtended):
    params: Optional[StatusParams] = None
    checker_type: str
