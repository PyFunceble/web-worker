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

This is the setuptool of the project.

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

import os
import re
from typing import List
from setuptools import find_packages, setup

MODULE_NAME = "pyfunceble_webworker"


def get_requirements() -> List[str]:
    """
    Extracts all requirements from requirements.txt.
    """

    result = set()

    with open("requirements.txt", "r", encoding="utf-8") as file_stream:
        for line in file_stream:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "#" in line:
                line = line[: line.find("#")]

            line = line.strip()

            if not line:
                continue

            result.add(line)

    return list(result)


def get_version() -> str:
    """
    Provides the project version.
    """

    to_match = re.compile(r'__version__\s+=\s+"(.*)"')

    with open(
        os.path.join(MODULE_NAME, "__init__.py"), "r", encoding="utf-8"
    ) as file_stream:
        return to_match.findall(file_stream.read())[0]


def get_long_description():
    """
    Provides the long description.
    """

    with open("README.rst", "r", encoding="utf-8") as file_stream:
        return file_stream.read()


if __name__ == "__main__":
    setup(
        name=MODULE_NAME,
        version=get_version(),
        python_requires=">=3.7, <4",
        install_requires=get_requirements(),
        description="The PyFunceble project behind a REST API.",
        long_description=get_long_description(),
        author="funilrys",
        author_email="contact@funilrys.com",
        license="Apache 2.0",
        url="https://github.com/PyFunceble/web-worker",
        project_urls={
            "Funding": "https://github.com/sponsors/funilrys",
            "Source": "https://github.com/PyFunceble/web-worker/tree",
            "Tracker": "https://github.com/PyFunceble/web-worker/issues",
        },
        platforms=["any"],
        packages=find_packages(exclude=("*.tests", "*.tests.*", "tests.*", "tests")),
        include_package_data=True,
        keywords=[
            "PyFunceble",
            "syntax-checker",
            "reputation-checker",
            "availability-checker",
        ],
        classifiers=[
            "Topic :: Internet",
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved",
        ],
    )