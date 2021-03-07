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

This is the module that provides all our entrypoints.

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

from fastapi import APIRouter, Request
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from PyFunceble.storage import PROJECT_VERSION
from starlette.responses import HTMLResponse

import pyfunceble_webworker.storage
from pyfunceble_webworker import __session_id__, __version__
from pyfunceble_webworker.core.defaults import assets as assets_defaults
from pyfunceble_webworker.models.info import CoreLocation, CoreVersion, SystemInfo
from pyfunceble_webworker.models.links import (
    DocumentationURL,
    Links,
    ProjectsURL,
    SupportURL,
)
from pyfunceble_webworker.routes.v1.endpoints import (
    availability,
    reputation,
    syntax,
    tools,
)

api_router = APIRouter()


@api_router.get("/docs", include_in_schema=False)
def custom_doc() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=assets_defaults.PROJECT_NAME,
        swagger_favicon_url=assets_defaults.FAVICON_URL,
    )


@api_router.get("/rdocs", include_in_schema=False)
def custom_redoc() -> HTMLResponse:
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=assets_defaults.PROJECT_NAME,
        redoc_favicon_url=assets_defaults.FAVICON_URL,
    )


@api_router.get(
    "/",
    response_model=Links,
    name="Home Sweet Home",
    description="Provides our relevant URL.",
)
def root(request: Request) -> Links:
    """
    Provides the root of our project.
    """

    return Links(
        documentation=DocumentationURL(
            swagger_ui=request.url_for("custom_doc"),
            redoc=request.url_for("custom_redoc"),
        ),
        projects=ProjectsURL(),
        support=SupportURL(),
    )


@api_router.get(
    "/info",
    response_model=SystemInfo,
    name="Information",
    description="Provides some information about the current node.",
)
def info() -> SystemInfo:
    """
    Provides the information about the running projects.
    """

    return SystemInfo(
        version=CoreVersion(worker=__version__, pyfunceble=PROJECT_VERSION),
        id=__session_id__,
        location=CoreLocation(**pyfunceble_webworker.storage.LOCATION),
    )


api_router.include_router(
    availability.router, prefix="/availability", tags=["availability"]
)
api_router.include_router(syntax.router, prefix="/syntax", tags=["syntax"])
api_router.include_router(reputation.router, prefix="/reputation", tags=["reputation"])
api_router.include_router(tools.router, prefix="/tools", tags=["tools"])
