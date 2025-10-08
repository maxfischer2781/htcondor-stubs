# HTCondor Python binding stubs

This repo contains experimental [type stubs](https://typing.python.org/en/latest/spec/distributing.html) for the [HTCondor Python Bindings](https://htcondor.readthedocs.io/en/24.x/apis/python-bindings/).
**These stubs are third-party and not officially provided by the HTCondor developers.**

Coverage of stubs:

- Mostly complete [HTCondor 24 bindings](https://htcondor.readthedocs.io/en/24.x/apis/python-bindings/) `classad` and `htcondor`
- Experimental [HTCondor 25 bindings](https://htcondor.readthedocs.io/en/25.x/apis/python-bindings/) `classad2`

## Installation

If you have a virtual environment used for development and type checking (e.g. in VSCode) simply install this module into it:

    # release version from pypi
    (venv) ~$ python -m pip install htcondor-stubs-contrib
    # dev version from github
    (venv) ~$ python -m pip install git+https://github.com/maxfischer2781/htcondor-stubs.git@main
