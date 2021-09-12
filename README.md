<h1 align="center">
    forku
    <br>
    <sup><sub><sup>quickly push a patch</sup></sub></sup>
    <br>
</h1>


## forku

If you patch a python lib in your local virtual env. 
forku ("fork you") tries to fork the repo and apply the patch.

(This only works if a repo can be found for that library.)


THIS PROJECT REQUIRES GITHUB CLI INSTALLED

https://cli.github.com/


## requirements

forku requires the following:

- python3
- git
- gh (github cli) : https://cli.github.com/
- virtualenv


### install

```bash
python3 -m pip install forku
```

### usesage

Pass forku the library you have patched. i.e. `python3 -m forku -l theirlib`

```bash
cd someproject
. venv/bin/activate
python3 -m forku -l domonic
```

i.e. This would fork the domonic library from github, then move the patches you made to venv/lib/python3.9/site-packages/domonic to the fork and push it back to github.


#### status

It currently makes a lot of assumption, so wont work for many cases.

- assumes git
- assumes latest version of lib. Careful. If not this could result in reverting code in the target library.
- assumes you have virtualenv
- assumes you are in the correct directory
- assume a dist-info folder exists with METADATA with a Home-page
- assumes you have a github account 
- assumes linux?? not sure

See README.md for more information.


### TODO -
    - add support for other git repos like bitbucket
    - add support for other python libs
    - add support for other os
    - add support for other packing systems


## Disclaimer

This is a work in progress. use at your own risk.