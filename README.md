# PyFunceble - Web Worker

This is the PyFunceble Web Worker. It tries to bring the PyFunceble
project to you through a Web API.

If you don't know what PyFunceble is, please report to the [PyFunceble
repository](https://github.com/funilrys/PyFunceble).

------------------------------------------------------------------------

## Differences with the PyFunceble CLI

This project is not intended to fully replace the official PyFunceble
Command Line Interface provided by
[@funilrys](https://github.com/funilrys).

This project is intended for those who don't necessarily use Python for
their projects, but still want to use PyFunceble to check the
availability, syntax, or reputation of a domain, IP, or URL. In other
words, this project only provides the core functions of PyFunceble, but
behind a Web API.

When you use the `PyFunceble` CLI, it is just an implementation of
functionalities on top of the core ideas of PyFunceble. In fact, if one
wants to implement or create their CLI on top of the core capabilities
of PyFunceble, they are welcome to do so. They can even submit it so
that it may become the standard or an alternative documented
implementation.

You won't find the following inside this project (to only list a few):

-   Almost everything specially implemented by the CLI of PyFunceble.
    -   The output file(s).
    -   The inactive datasets.
    -   The auto continue datasets.
    -   The continuous integration module.
    -   Any form of database.

Instead, you will find the following:

-   Web endpoints to test the availability of a domain, IP, or URL.
-   Web endpoints to test the syntax of a domain, IP, or URL.
-   Web endpoints to test the reputation of a domain, IP, or URL.
-   Web endpoint to get the complement of a given subject.
-   Web endpoint for the decoding or conversion from and to several
    formats.

## Installation

**Please be informed that we recommend you to use docker as much as
possible.**

### Manual

To manually install this project, simply run the following:

    $ git clone https://github.com/PyFunceble/web-worker.git pyfunceble-web-worker
    $ cd pyfunceble-web-worker

    ## Install by choosing your PyFunceble flavor.
    ## For PyFunceble run:
    $ pip3 install --user .[pyfunceble]
    ## For PyFunceble-dev run:
    $ pip3 install --user .[pyfunceble-dev]

### GitHub Packages

This project provides 2 docker images that you can pull:

1.  `ghcr.io/pyfunceble/web-worker/web-worker` is built with PyFunceble
    (stable).
2.  `ghcr.io/pyfunceble/web-worker/web-worker-dev` is built with
    PyFunceble-dev.

To pull the image that has been built on top of PyFunceble (stable):

    $ docker pull ghcr.io/pyfunceble/web-worker/web-worker:latest

To pull the image that has been built on top of PyFunceble-dev:

    $ docker pull ghcr.io/pyfunceble/web-worker/web-worker-dev:latest

### Docker (self-build)

To build the Containerfile provided, simply run or adapt the following:

    $ docker build -t pyfunceble_webworker -f [Containerfile] .

By default, this project will be built against the latest available
version of PyFunceble. If you want to change that behavior, simply add
the following build arguments:

    --build-arg PYFUNCEBLE_VERSION=[PyFunceble Version]

## Usage

Please choose your method to start the project.

Once the project running, you may visit the `/v1/docs` or `/v1/rdocs`
endpoint from your browser to document yourself about all available
endpoints.

### Manual

To start the project, simply run or adapt the following:

    $ cd pyfunceble-web-worker
    $ uvicorn pyfunceble_webworker.main:app --host 0.0.0.0 --port 80

### GitHub Packages

To start the project after pulling it from the GitHub Packages, simply
run or adapt the following:

    $ docker run -v pyfunceble-worker-data:/data -d --name [my-awesome-name] -p [my-port]:80 ghcr.io/pyfunceble/web-worker/web-worker:latest

### Docker (self-built)

To start the project, simply run or adapt the following:

    $ docker run -v pyfunceble-worker-data:/data -d --name [my-awesome-name] -p [my-port]:80 pyfunceble_webworker:latest

## Configuration

### Supported Environment Variables

In addition to:

-   any [PyFunceble environment
    variable](https://docs.pyfunceble.com/use/configuration/environment-variables.html)
-   any
    [uvicorn-gunicorn-fastapi](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker#advanced-usage)
    environment variable - when using the docker image

the following are available for you to use.

If you chose to manually run this project, you are invited to use a
`.env` file to declare your environment variables.

| Name                        | Description                                                                                                        | Default Value                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| BACKEND_CORS_ORIGINS        | A comma-separated list of origins that should be allowed to make requests to the backend API.                      | None                                                                 |
| ALLOW_WHOIS_LOOKUP          | A boolean which tells the system if it should allow the WHOIS lookup.                                              | False                                                                |
| ALLOW_WHOIS_LOOKUP_PARAM    | Allows end-user to define and control if they want to use the WHOIS lookup to gather the status - when applicable. | False                                                                |
| PYFUNCEBLE_WORKERS_DATA_DIR | The directory where the data should be stored.                                                                     | `/data` under the docker container, `${PWD}/workers_data` otherwise. |


### PyFunceble

To configure PyFunceble, simply create a `.PyFunceble.overwrite.yaml`
file at the root of the given data directory. The data directory is by
default `/data` under the docker container.

The `.PyFunceble.overwrite.yaml`, will be automatically merged into the
PyFunceble configuration module. Meaning that you can define anything
that PyFunceble knows.

For example:

```yaml
dns:
  server:
    - 192.168.1.1
```

Will overwrite the DNS server used by PyFunceble with the given one.

## Supporting the project

This project, [PyFunceble](https://github.com/funilrys/PyFunceble),
[Dead-Hosts](https://github.com/dead-hosts), [adblock-decoder](https://github.com/pyunceble/adblock-decoder)
and all other analog projects are powered by free time and a lot of coffee!

This project helps you and you have to possibility to help back financially?
Sponsor [@funilrys](https://github.com/funilrys) through the GitHub Sponsor
program by clicking the image below!

[![image](https://github.blog/de/wp-content/uploads/sites/3/2019/05/mona-heart-featured.png?w=200)](https://github.com/sponsors/funilrys)

## License

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