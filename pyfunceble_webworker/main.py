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

This is the application provider.

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

import importlib.resources
import logging
import os
import secrets

import inflection
import PyFunceble.facility
import PyFunceble.storage
import requests
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import RedirectResponse
from fastapi_utils.tasks import repeat_every
from PyFunceble.config.loader import ConfigLoader
from PyFunceble.downloader.iana import IANADownloader
from PyFunceble.downloader.ipv4_reputation import IPV4ReputationDownloader
from PyFunceble.downloader.public_suffix import PublicSuffixDownloader
from PyFunceble.downloader.user_agents import UserAgentsDownloader
from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.merge import Merge
from starlette.middleware.cors import CORSMiddleware

import pyfunceble_webworker.storage
from pyfunceble_webworker import __version__
from pyfunceble_webworker.core.defaults import assets as assets_defaults
from pyfunceble_webworker.core.defaults import pyfunceble as pyfunceble_defaults
from pyfunceble_webworker.core.defaults import routes as routes_defaults
from pyfunceble_webworker.core.settings import core_settings
from pyfunceble_webworker.models.info import CoreLocation
from pyfunceble_webworker.models.links import Links
from pyfunceble_webworker.routes.v1.api import api_router as v1_api_router

env_var_helper = EnvironmentVariableHelper()

if not env_var_helper.set_name("PYFUNCEBLE_WORKERS_DATA_DIR").exists():
    raise RuntimeError(
        "Could not find PYFUNCEBLE_WORKERS_DATA_DIR environment variable."
    )

pyfunceble_webworker.storage.CONFIG_DIRECTORY = env_var_helper.get_value()

PyFunceble.storage.CONFIG_DIRECTORY = os.path.join(
    pyfunceble_webworker.storage.CONFIG_DIRECTORY,
    secrets.token_hex(8),
)

DirectoryHelper(PyFunceble.storage.CONFIG_DIRECTORY).create()

file_helper = FileHelper()
pyfunceble_config_loader = ConfigLoader()

if file_helper.set_path(
    os.path.join(
        pyfunceble_webworker.storage.CONFIG_DIRECTORY,
        assets_defaults.OVERWRITE_CONFIG_FILE,
    )
).exists():
    local = DictHelper().from_yaml_file(file_helper.path)

    if local:
        pyfunceble_config_loader.custom_config = local
    else:
        pyfunceble_config_loader.custom_config = dict()

pyfunceble_config_loader.custom_config = Merge(
    pyfunceble_defaults.PERSISTENT_CONFIG
).into(pyfunceble_config_loader.custom_config)
pyfunceble_config_loader.start()


app = FastAPI(
    title=assets_defaults.PROJECT_NAME,
    description=assets_defaults.PROJECT_DESCRIPTION,
    version=__version__,
    docs_url=None,
    redoc_url=None,
)


with importlib.resources.path(
    "pyfunceble_webworker.data", "logger.yaml"
) as logger_config_path:
    logger_data = DictHelper.from_yaml_file(str(logger_config_path))

    logger_data["handlers"]["file"]["filename"] = os.path.join(
        pyfunceble_webworker.storage.CONFIG_DIRECTORY,
        logger_data["handlers"]["file"]["filename"],
    )

    logging.config.dictConfig(logger_data)


if core_settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(x) for x in core_settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(v1_api_router, prefix=routes_defaults.V1_URL_PREFIX)


def custom_openapi():
    """
    Customizes the openapi schema for our usage.
    """

    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        description=app.description,
        version=app.version,
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema

    paths_to_delete = {x for x in app.openapi_schema["paths"] if x.endswith("$")}

    for path in paths_to_delete:
        app.openapi_schema["paths"][path[:-1]] = app.openapi_schema["paths"][path]
        del app.openapi_schema["paths"][path]

    openapi_schema["info"]["x-logo"] = {"url": assets_defaults.LOGO_URL}

    return app.openapi_schema


app.openapi = custom_openapi


@app.on_event("shutdown")
def cleanup_data_dir() -> None:
    """
    Cleanup our data directory on shutdown.
    """

    DirectoryHelper(PyFunceble.storage.CONFIG_DIRECTORY).delete()


@app.on_event("startup")
@repeat_every(seconds=60 * 60 * 24, wait_first=False)
def periodic_data_update() -> None:
    """
    Process a periodic update of PyFunceble internal files.
    """

    logging.info("Starting to update PyFunceble's reputation dataset.")
    IPV4ReputationDownloader().start()
    logging.info("Finished to update PyFunceble's reputation dataset.")

    logging.info("Starting to update PyFunceble's user-agent dataset.")
    UserAgentsDownloader().start()
    PyFunceble.storage.USER_AGENTS = dict()
    logging.info("Finished to update PyFunceble's user-agent dataset.")

    logging.info("Starting to update PyFunceble's PSL dataset.")
    PublicSuffixDownloader().start()
    PyFunceble.storage.PUBLIC_SUFFIX = dict()
    logging.info("Finished to update PyFunceble's PSL dataset.")

    logging.info("Starting to update PyFunceble's IANA dataset.")
    IANADownloader().start()
    PyFunceble.storage.IANA = dict()
    logging.info("Finished to update PyFunceble's IANA dataset.")


@app.on_event("startup")
@repeat_every(seconds=60 * 70, wait_first=False, raise_exceptions=True)
def periodic_location_update():
    """
    Process a periodic update of our location.
    """

    logging.info("Starting to fetch location data.")

    req = requests.get(
        "http://ip-api.com/json",
        params={
            "fields": ",".join(
                [
                    inflection.camelize(x, uppercase_first_letter=False)
                    for x in CoreLocation().__dict__.keys()
                ]
            )
        },
    )

    if req.status_code != 200:
        logging.critical(
            "Could not fetch location information. (status_code: %s)", req.status_code
        )
    else:

        for key, value in req.json().items():
            pyfunceble_webworker.storage.LOCATION[inflection.underscore(key)] = value

        logging.info("Finished to fetch location data.")


@app.get(
    "/",
    name="Hello World",
    description="Hello, World!",
    include_in_schema=False,
)
def hello_world() -> Links:
    """
    Hello, World!
    """

    return RedirectResponse(routes_defaults.URL_PREFIX)
