# HTCondor Python binding stubs

This repo contains experimental [type stubs](https://typing.python.org/en/latest/spec/distributing.html) for the [HTCondor Python Bindings](https://htcondor.readthedocs.io/en/24.x/apis/python-bindings/).
**These stubs are third-party and not officially provided by the HTCondor developers.**

Coverage of stubs:

- `classad`: Everything as per docs
- `htcondor`: `Collector`, `Schedd` and corresponding types/functions

## Installation

If you have a virtual environment used for development and type checking (e.g. in VSCode) simply install this module into it:

    # release version from pypi
    (venv) ~$ python -m pip install htcondor-stubs-contrib
    # dev version from github
    (venv) ~$ python -m pip install git+https://github.com/maxfischer2781/htcondor-stubs.git@main
