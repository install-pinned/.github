## Keep your CI pipeline secure and deterministic with pinned installs.
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
<!-- ⚠️auto-generated from init.py, do not edit manually ⚠️-->
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

### Deterministic

When you `pip install foo`, you are getting the latest and greatest version of `foo` and all its dependencies.
However, `foo`'s behavior (or that of its dependencies) may change over time. This introduces unexpected breakage into your CI pipeline,
usually exactly at the time when you don't want it.

### Secure

When you `pip install foo` in your CI pipeline, you trust 

 - PyPI,
 - the authors of `foo`, and 
 - all authors of all (sub)dependencies of `foo`

to not be compromised. If one of them is, an attacker may push a malicious package to PyPI which steals your code 
and your repository secrets (e.g. deployment tokens).[^1]
To mitigate this problem, you should _pin_ your dependencies, i.e. use a `requirements.txt`/`poetry.lock`/... lock file
that ensures only specific versions (with specific file hashes) are allowed. This changes the threat model from "trust 
continuously" to "trust on first use".

[^1]: This typically includes GitHub secrets that are not available to the current workflow.
      By default, `GITHUB_TOKEN` can push new commits, which can be used to rewrite workflows and obtain more secrets.

#### What are the actions here for?

The actions provided here allow you to securely (i.e. with pinning + hashes) install popular 
tools to use in your CI pipeline without any additional lock files. 

For example, you maybe want to run [black](https://github.com/psf/black) in your CI pipeline, but black is not a 
dependency for your application. Instead of adding a separate lock file to your repository, you just use the [install-pinned/black](https://github.com/install-pinned/black) action.

#### Why should I not use this?

By pinning your tools, the dependency graph becomes static. 
This means that you will not automatically get new (security) updates.
To mitigate this, you can [set up Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot#example-dependabotyml-file-for-github-actions)
so that your pins are updated regularly.

#### Supported tools:
- [![latest pins](https://github.com/install-pinned/autoflake/actions/workflows/update.yml/badge.svg?branch=main) autoflake](https://github.com/install-pinned/autoflake)
- [![latest pins](https://github.com/install-pinned/black/actions/workflows/update.yml/badge.svg?branch=main) black](https://github.com/install-pinned/black)
- [![latest pins](https://github.com/install-pinned/build/actions/workflows/update.yml/badge.svg?branch=main) build](https://github.com/install-pinned/build)
- [![latest pins](https://github.com/install-pinned/isort/actions/workflows/update.yml/badge.svg?branch=main) isort](https://github.com/install-pinned/isort)
- [![latest pins](https://github.com/install-pinned/maturin/actions/workflows/update.yml/badge.svg?branch=main) maturin](https://github.com/install-pinned/maturin)
- [![latest pins](https://github.com/install-pinned/maturin-with-zig/actions/workflows/update.yml/badge.svg?branch=main) maturin[zig]](https://github.com/install-pinned/maturin-with-zig)
- [![latest pins](https://github.com/install-pinned/mitmproxy/actions/workflows/update.yml/badge.svg?branch=main) mitmproxy](https://github.com/install-pinned/mitmproxy)
- [![latest pins](https://github.com/install-pinned/mypy/actions/workflows/update.yml/badge.svg?branch=main) mypy](https://github.com/install-pinned/mypy)
- [![latest pins](https://github.com/install-pinned/pdm/actions/workflows/update.yml/badge.svg?branch=main) pdm](https://github.com/install-pinned/pdm)
- [![latest pins](https://github.com/install-pinned/pdm-backend/actions/workflows/update.yml/badge.svg?branch=main) pdm-backend](https://github.com/install-pinned/pdm-backend)
- [![latest pins](https://github.com/install-pinned/pdoc/actions/workflows/update.yml/badge.svg?branch=main) pdoc](https://github.com/install-pinned/pdoc)
- [![latest pins](https://github.com/install-pinned/pip-tools/actions/workflows/update.yml/badge.svg?branch=main) pip-tools](https://github.com/install-pinned/pip-tools)
- [![latest pins](https://github.com/install-pinned/poetry/actions/workflows/update.yml/badge.svg?branch=main) poetry](https://github.com/install-pinned/poetry)
- [![latest pins](https://github.com/install-pinned/pytest/actions/workflows/update.yml/badge.svg?branch=main) pytest](https://github.com/install-pinned/pytest)
- [![latest pins](https://github.com/install-pinned/pyupgrade/actions/workflows/update.yml/badge.svg?branch=main) pyupgrade](https://github.com/install-pinned/pyupgrade)
- [![latest pins](https://github.com/install-pinned/reorder_python_imports/actions/workflows/update.yml/badge.svg?branch=main) reorder_python_imports](https://github.com/install-pinned/reorder_python_imports)
- [![latest pins](https://github.com/install-pinned/ruff/actions/workflows/update.yml/badge.svg?branch=main) ruff](https://github.com/install-pinned/ruff)
- [![latest pins](https://github.com/install-pinned/setuptools/actions/workflows/update.yml/badge.svg?branch=main) setuptools](https://github.com/install-pinned/setuptools)
- [![latest pins](https://github.com/install-pinned/tox/actions/workflows/update.yml/badge.svg?branch=main) tox](https://github.com/install-pinned/tox)
- [![latest pins](https://github.com/install-pinned/twine/actions/workflows/update.yml/badge.svg?branch=main) twine](https://github.com/install-pinned/twine)
- [![latest pins](https://github.com/install-pinned/wheel/actions/workflows/update.yml/badge.svg?branch=main) wheel](https://github.com/install-pinned/wheel)
- [![latest pins](https://github.com/install-pinned/yesqa/actions/workflows/update.yml/badge.svg?branch=main) yesqa](https://github.com/install-pinned/yesqa)

Your tool is not on the list? Request it [here](https://github.com/install-pinned/.github/issues).

#### Security

If you believe you've identified a security issue with install-pinned, please report it to 
[@mhils](https://github.com/mhils) using the email address listed on his GitHub profile.
