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

This is the module that provides all our links related links models.

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

from fastapi import Body
from pydantic import AnyUrl, BaseModel, HttpUrl


class DocumentationURL(BaseModel):
    swagger_ui: AnyUrl = Body(
        ..., title="Documentation URL", description="The documentation URL."
    )
    redoc: AnyUrl = Body(
        ..., title="Redoc URL", description="The ReDoc formatted documentation URL."
    )


class SupportURL(BaseModel):
    github_sponsors: HttpUrl = Body(
        "https://github.com/sponsors/funilrys",
        title="GitHub Sponsort",
        description="Sponsor @funilrys on GitHub!",
    )
    paypal: HttpUrl = Body(
        "https://paypal.me/funilrys",
        title="Paypal Donation",
        description="Make a one time donation to @funilrys on PayPal!",
    )
    kofi: HttpUrl = Body(
        "https://ko-fi.com/V7V3EH2Y",
        title="Ko-Fi",
        description="Support @funilrys on Ko-Fi!",
    )


class ProjectsURL(BaseModel):
    pyfunceble_web_worker: HttpUrl = Body(
        "https://github.com/PyFunceble/web-worker",
        title="Repository Web Worker URL",
        description="The repository of the PyFunceble web-worker project.",
    )
    pyfunceble: HttpUrl = Body(
        "https://pyfunceble.github.io",
        title="Home URL",
        description="The home page of the PyFunceble project.",
    )
    pyfunceble_github: HttpUrl = Body(
        "https://github.com/funilrys/PyFunceble",
        title="PyFunceble on GitHub",
        description="The GitHub repository of the PyFunceble project.",
    )


class Links(BaseModel):
    documentation: DocumentationURL
    projects: ProjectsURL
    support: SupportURL
