PyFunceble - Web Worker
=======================

This is the PyFunceble Web Worker. It tries to bring the PyFunceble project to
you through a Web API.

If you don't know what PyFunceble is, please report to the
`PyFunceble repository`_.

___________________________________________

Differences with the PyFunceble CLI
-----------------------------------

This project is not intended to fully replace the official PyFunceble Command
Line Interface provided by `@funilrys`_.

This project is intended for those who don't necessarily use Python for their
projects, but still want to use PyFunceble to check the availability, syntax, or
reputation of a domain, IP, or URL. In other words, this project only provides
the core functions of PyFunceble, but behind a Web API.

When you use the :code:`PyFunceble` CLI, it is just
an implementation of functionalities on top of the core ideas of PyFunceble.
In fact, if one wants to implement or create their CLI on top of the core
capabilities of PyFunceble, they are welcome to do so. They can even submit it
so that it may become the standard or an alternative documented implementation.

You won't find the following inside this project (to only list a few):

- Almost everything specially implemented by the CLI of PyFunceble.
    - The output file(s).
    - The inactive datasets.
    - The auto continue datasets.
    - All form of decoding (or output) of any form of input: hosts, AdBlock, RPZ,
      Wildcard, etc.
    - The continuous integration module.

Instead, you will find the following:

- Web endpoints to test the availability of a domain, IP, or URL.
- Web endpoints to test the syntax of a domain, IP, or URL.
- Web endpoints to test the reputation of a domain, IP, or URL.
- Web endpoint to get the complement of a given subject.

___________________________________________

Installation
------------

**Please be informed that we recommend you to use docker as much as possible.**

Manual
""""""

To manually install this project, simply run the following:

::

    $ git clone https://github.com/PyFunceble/web-worker.git pyfunceble-web-worker
    $ cd pyfunceble-web-worker
    $ pip3 install --user --pre PyFunceble-dev
    $ pip3 install --user uvicorn[standard]
    $ pip3 install --user .

GitHub Packages
"""""""""""""""

To pull the docker image, simply run the following:

::

    $ docker pull ghcr.io/pyfunceble/web-worker/web-worker:latest

Docker (self-build)
"""""""""""""""""""

To build the Dockerfile provided, simply run or adapt the following:

::

    $ docker build -t pyfunceble_webworker -f [Dockerfile] .

By default, this project will be built against the latest available version of
PyFunceble. If you want to change that behavior, simply add the following
build arguments:

::

    --build-arg PYFUNCEBLE_VERSION=[PyFunceble Version]

___________________________________________

Usage
-----

Please choose your method to start the project.

Once the project running, you may visit the :code:`/v1/docs`
or :code:`/v1/rdocs` endpoint from your browser to document yourself about
all available endpoints.

Manual
""""""

To start the project, simply run or adapt the following:

::

    $ cd pyfunceble-web-worker
    $ uvicorn pyfunceble_webworker.main:app --host 0.0.0.0 --port 80

GitHub Packages
"""""""""""""""

To start the project after pulling it from the GitHub Packages, simply run or
adapt the following:

::

    $ docker run -v pyfunceble-worker-data:/data -d --name [my-awesome-name] -p [my-port]:80 ghcr.io/pyfunceble/web-worker/web-worker:latest

Docker (self-built)
"""""""""""""""""""

To start the project, simply run or adapt the following:

::

    $ docker run -v pyfunceble-worker-data:/data -d --name [my-awesome-name] -p [my-port]:80 pyfunceble_webworker:latest

___________________________________________

Configuration
-------------

Supported Environment Variables
"""""""""""""""""""""""""""""""

In addition to any PyFunceble environment variable, the following are also
available for you to use.

If you chose to manually run this project, you are invited to use a
:code:`.env` file to declare your environment variables.

+-----------------------------+---------------------------------------------------------------------------------------------------------------------+
| Name                        | Description                                                                                                         |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------+
| BACKEND_CORS_ORIGINS        | Allows CORS origin only through the given list of URLs.                                                             |
|                             |                                                                                                                     |
|                             |                                                                                                                     |
|                             | Default: None                                                                                                       |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------+
| ALLOW_WHOIS_LOOKUP          | Allows the usage of WHOIS lookups to gather the status - when applicable.                                           |
|                             |                                                                                                                     |
|                             | Default: False                                                                                                      |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------+
| ALLOW_WHOIS_LOOKUP_PARAM    | Allows end-user to define and control if they want to use the WHOIS lookup to gather the status - when applicable.  |
|                             |                                                                                                                     |
|                             | Default: false                                                                                                      |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------+
| PYFUNCEBLE_WORKERS_DATA_DIR | Sets the data directory.                                                                                            |
|                             |                                                                                                                     |
|                             | Default: /data under docker container, current location otherwise.                                                  |
+-----------------------------+---------------------------------------------------------------------------------------------------------------------+


PyFunceble
""""""""""

To configure PyFunceble, simply create a :code:`.PyFunceble.overwrite.yaml`
file at the root of the given data directory.
The data directory is by default :code:`/data` under the docker container.

The :code:`.PyFunceble.overwrite.yaml`, will be automatically merged into the
PyFunceble configuration module. Meaning that you can define anything that
PyFunceble knows.

For example:

::

    dns:
        server:
            - 192.168.1.1

Will overwrite the DNS server used by PyFunceble with the given one.


___________________________________________

Supporting the project
----------------------


This project and all other analog projects written by Nissar are powered by free
time and a lot of coffee!

This project helps you and/or you like it? Support me!

GitHub Sponsor
""""""""""""""
I am part of the GitHub Sponsor program!

.. image:: https://github.com/PyFunceble/logo/raw/master/pyfunceble_github.png
    :target: https://github.com/sponsors/funilrys
    :height: 70px

`Sponsor me`_!

Ko-Fi
"""""

Don't want to use the GitHub Sponsor program ?
Single donations are welcome too!

.. image:: https://az743702.vo.msecnd.net/cdn/kofi3.png
    :target: https://ko-fi.com/V7V3EH2Y
    :height: 70px

`Buy me a coffee`_!

___________________________________________

License
-------

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

.. _PyFunceble repository: https://github.com/funilrys/PyFunceble
.. _Sponsor me: https://github.com/sponsors/funilrys
.. _Buy me a coffee: https://ko-fi.com/V7V3EH2Y
.. _@funilrys: https://github.com/funilrys