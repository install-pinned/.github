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

#### How do I get (security) updates?

By pinning your tools, the dependency graph becomes static and you will not get (security) updates by default.
To mitigate this, you can [set up Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot#example-dependabotyml-file-for-github-actions)
so that your pins are updated regularly. A simple `.github/dependabot.yml` that works with **@install-pinned** looks like this:

```yaml
version: 2
updates:
  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: "monthly"
 ```

#### Supported tools:
- [autoflake](https://github.com/install-pinned/autoflake)
- [autopep8](https://github.com/install-pinned/autopep8)
- [black](https://github.com/install-pinned/black)
- [blacken-docs](https://github.com/install-pinned/blacken-docs)
- [build](https://github.com/install-pinned/build)
- [docformatter](https://github.com/install-pinned/docformatter)
- [isort](https://github.com/install-pinned/isort)
- [maturin](https://github.com/install-pinned/maturin)
- [maturin[zig]](https://github.com/install-pinned/maturin-with-zig)
- [pdoc](https://github.com/install-pinned/pdoc)
- [pip-tools](https://github.com/install-pinned/pip-tools)
- [poetry](https://github.com/install-pinned/poetry)
- [pyupgrade](https://github.com/install-pinned/pyupgrade)
- [reorder_python_imports](https://github.com/install-pinned/reorder_python_imports)
- [ruff](https://github.com/install-pinned/ruff)
- [setuptools](https://github.com/install-pinned/setuptools)
- [tox](https://github.com/install-pinned/tox)
- [twine](https://github.com/install-pinned/twine)
- [usort](https://github.com/install-pinned/usort)
- [yapf](https://github.com/install-pinned/yapf)
- [yesqa](https://github.com/install-pinned/yesqa)

Your tool is not on the list? Request it [here](https://github.com/install-pinned/.github/issues).

#### Security

If you believe you've identified a security issue with install-pinned, please report it to 
[@mhils](https://github.com/mhils) using the email address listed on his GitHub profile.
