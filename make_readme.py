#!/usr/bin/env python3
import json
from pathlib import Path

tools = json.loads(Path("tools.json").read_text())

tool_list = "\n".join(
    f"- [{tool}](https://github.com/install-pinned/{tool})"
    for tool in tools
)

readme = f"""\
## Keep your CI pipeline secure with pinned installs.
<!-- auto-generated from make_readme.py, do not edit manually -->

When you `pip install foo` in your CI pipeline, you trust 

 - PyPI,
 - the authors of `foo`, and 
 - all authors of all (sub)dependencies of `foo`
 
to keep their systems secure at all times.[^1] If only one of them is compromised,
they may push a malicious package to PyPI which steals your code and your repository secrets.[^2]
To mitigate this problem, you should _pin_ your dependencies, i.e. use a `requirements.txt`/`poetry.lock`/... lock file
that ensures only specific versions (with specific file hashes) are allowed. This changes the threat model from "trust 
continuously" to "trust on first use".

#### What is @install-pinned for?

The actions available in this GitHub organization allow you to securely (i.e. with pinning + hashes) install popular 
tools to use in your CI pipeline without any additional lockfiles. 

For example, you maybe want to run [black](https://github.com/psf/black) in your CI pipeline, but black is not a 
dependency for your application. Instead of adding a separate lock file to your repository, you just use the [install-pinned/black](https://github.com/install-pinned/black) action.

[^1]: More specifically, you hope that the respective PyPI packages are not compomised at the same time when your CI 
      runs.
[^2]: By default, `GITHUB_TOKEN` can push new commits, which can be used to obtain all secrets defined for a repository.

#### Supported tools:
{tool_list}
 
Your tool is not on the list? Request it [here](https://github.com/install-pinned/.github/issues).

#### Security

If you believe you've identified a security issue with install-pinned, please report it to 
[@mhils](https://github.com/mhils) using the email address listed on his GitHub profile.
"""

Path("profile/README.md").write_text(readme, encoding="utf-8", newline="\n")
