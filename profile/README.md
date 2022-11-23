## Keep your CI pipeline secure with pinned installs.
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
<!-- auto-generated from make_readme.py, do not edit manually -->
<!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

When you `pip install foo` in your CI pipeline, you trust 

 - PyPI,
 - the authors of `foo`, and 
 - all authors of all (sub)dependencies of `foo`
 
to not be compromised.[^1] If one of them is, an attacker may push a malicious package to PyPI which steals your code 
and your repository secrets (e.g. deployment tokens).[^2]
To mitigate this problem, you should _pin_ your dependencies, i.e. use a `requirements.txt`/`poetry.lock`/... lock file
that ensures only specific versions (with specific file hashes) are allowed. This changes the threat model from "trust 
continuously" to "trust on first use".

[^1]: More specifically, you hope that the respective PyPI packages are not compomised at the same time when your CI 
      runs.
[^2]: This often includes GitHub secrets that are not available to the current workflow.
      By default, `GITHUB_TOKEN` can push new commits, which can be used to rewrite workflows and obtain other secrets.

#### What are the actions here for?

The actions provided here allow you to securely (i.e. with pinning + hashes) install popular 
tools to use in your CI pipeline without any additional lock files. 

For example, you maybe want to run [black](https://github.com/psf/black) in your CI pipeline, but black is not a 
dependency for your application. Instead of adding a separate lock file to your repository, you just use the [install-pinned/black](https://github.com/install-pinned/black) action.

#### Why should I not use this?

By pinning your tools, the dependency graph becomes static. 
This means that you will not automatically get new (security) updates.

#### Supported tools:
- [autoflake](https://github.com/install-pinned/autoflake)
- [autopep8](https://github.com/install-pinned/autopep8)
- [black](https://github.com/install-pinned/black)
- [blacken-docs](https://github.com/install-pinned/blacken-docs)
- [docformatter](https://github.com/install-pinned/docformatter)
- [isort](https://github.com/install-pinned/isort)
- [maturin](https://github.com/install-pinned/maturin)
- [maturin[zig]](https://github.com/install-pinned/maturin[zig])
- [pdoc](https://github.com/install-pinned/pdoc)
- [pip-tools](https://github.com/install-pinned/pip-tools)
- [pyupgrade](https://github.com/install-pinned/pyupgrade)
- [reorder_python_imports](https://github.com/install-pinned/reorder_python_imports)
- [ruff](https://github.com/install-pinned/ruff)
- [usort](https://github.com/install-pinned/usort)
- [yapf](https://github.com/install-pinned/yapf)
- [yesqa](https://github.com/install-pinned/yesqa)
 
Your tool is not on the list? Request it [here](https://github.com/install-pinned/.github/issues).

#### Security

If you believe you've identified a security issue with install-pinned, please report it to 
[@mhils](https://github.com/mhils) using the email address listed on his GitHub profile.
