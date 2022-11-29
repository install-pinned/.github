#!/usr/bin/env python3
import json
import os
import re
import shutil
import stat
from pathlib import Path
from subprocess import run
from textwrap import dedent, indent

import httpx

here = Path(__file__).parent
access_token = (here / "github_token.txt").read_text().strip()

client = httpx.Client(
    headers={
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }
)

repos_dir = (here / "repos").absolute()

tools = json.loads((here / "tools.json").read_text())
python_versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]


def repo_name(tool: str) -> str:
    return tool.replace("[", "-with-").replace(",","-").replace("]", "")


def tool_name_without_extras(tool: str) -> str:
    return tool.partition("[")[0]


readme_tool_list = "\n".join(
    f"- [{tool}](https://github.com/install-pinned/{repo_name(tool)})"
    for tool in tools
)
readme = f"""\
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
{readme_tool_list}

Your tool is not on the list? Request it [here](https://github.com/install-pinned/.github/issues).

#### Security

If you believe you've identified a security issue with install-pinned, please report it to 
[@mhils](https://github.com/mhils) using the email address listed on his GitHub profile.
"""
(here / "profile/README.md").write_text(readme, encoding="utf-8", newline="\n")


for tool in tools:
    continue
    repo = repo_name(tool)
    resp = client.post(
        "https://api.github.com/orgs/install-pinned/repos",
        json={
            "name": repo,
            "license_template": "mit",
        },
    )
    print(resp)
    print(resp.read())

for tool in tools:
    # continue
    repo = repo_name(tool)
    resp = client.patch(
        f"https://api.github.com/repos/install-pinned/{repo}",
        json={
            "description": f"Securely install the latest {tool} release from PyPI.",
            "homepage": "https://github.com/install-pinned",
            "private": False,
            "has_issues": False,
            "has_projects": False,
            "has_wiki": False,
        },
    )
    print(resp)
    print(resp.read())

for tool in tools:
    # continue
    repo = repo_name(tool)
    if (repos_dir / repo).exists():
        def make_writable(function, path, _exception):
            os.chmod(path, stat.S_IWRITE)
            function(path)


        shutil.rmtree(repos_dir / repo, onerror=make_writable)

    run(f"git clone git@github.com:install-pinned/{repo}.git", cwd=repos_dir)

for tool in tools:
    # continue
    repo = repo_name(tool)
    tool_name = tool_name_without_extras(tool)
    os.chdir(repos_dir / repo)

    def write(filename: str, contents: str) -> None:
        f = Path(filename)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(dedent(contents), encoding="utf-8", newline="\n")

    # modify one of this pins to make sure that the CI runs.
    # write("pins/requirements-3.10.txt", "")

    try:
        last_release = re.search(r"(?<=@)[0-9a-f]{40}.+", Path("README.md").read_text())[0]
    except Exception:
        last_release = "ffffffffffffffffffffffffffffffffffffffff"
    write(
        "README.md",
        f"""
        # install-pinned/{repo}
        <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
        <!-- ⚠️auto-generated from init.py, do not edit manually ⚠️-->
        <!-- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
        
        ![](https://shields.io/badge/python-{'%20%7C%20'.join(python_versions)}-blue)
        
        Securely install the latest [{tool}](https://pypi.org/project/{tool_name}/) release from PyPI.
        
        This action installs a pinned version of **{tool}** and all its dependencies, \
        making sure that file hashes match. Pinning your dependencies:

         1. Stops software supply chain attacks.
         2. Makes sure your CI does not break unexpectedly.
        
        ## Usage
        
        In your GitHub Actions workflow, use this action like so:
        
        ```yaml
              - name: Install {tool} from PyPI
                uses: install-pinned/{repo}@{last_release}
        ```
        
        You can [set up Dependabot](https://docs.github.com/en/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot#example-dependabotyml-file-for-github-actions)
        so that your pins are updated regularly.
        
        ## Alternatives
        
        This action is a relatively simple wrapper around the fantastic [pip-tools](https://pip-tools.rtfd.io) \
        and is most useful if there is no existing `requirements.txt`/`poetry.lock`/... infrastructure in place. \
        If you already pin all your dependencies in a single place, you don't need it!
        
        ## More Details
        
        See the [@install-pinned README](https://github.com/install-pinned) for details.
        """,
    )
    write(
        "action.yml",
        # language=yaml
        f"""\
        name: 'install-pinned/{repo}'
        description: 'Securely install the latest {tool} release from PyPI'
        branding:
          icon: 'lock'
          color: 'green'
        runs:
          using: "composite"
          steps:
            - shell: bash
              run: |
                pyver=$(python -c 'import sys; print(f"{{sys.version_info.major}}.{{sys.version_info.minor}}")')
                pip install -r $GITHUB_ACTION_PATH/pins/requirements-$pyver.txt
        """,
    )

    write("pins/requirements.in", f"{tool}\n")

    versions = "\n".join(
        dedent(
            # language=yaml
            f"""
            - uses: actions/setup-python@v4
              with:
                python-version: '{py}'
            - run: pip install pip-tools==6.9.0
            - run: pip-compile --upgrade --allow-unsafe --generate-hashes pins/requirements.in -o pins/requirements-{py}.txt 
            """.rstrip()
        )
        for py in python_versions
    )
    write(
        ".github/workflows/update.yml",
        # language=yaml
        f"""
        name: "update pins"

        on:
          workflow_dispatch:
          schedule:
            - cron: '25 4,16 * * *'

        jobs:
          update_pins:
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v3
                with:
                  ref: main
              {indent(versions, " " * 14)}

              - id: commit
                run: |
                  if [ -n "$(git status --porcelain)" ]; then
                    git config --global user.name "install-pinned bot"
                    git config --global user.email "install-pinned@users.noreply.github.com"
                    git add --all
                    ver=$(curl -Ls https://pypi.org/pypi/{tool_name}/json | jq -r .info.version)
                    git commit -m "update pins ({tool} $ver)"
                    commit=$(git rev-parse HEAD)
                    sed -i -E "s/@[0-9a-f]{{40}}.*/@$commit  # $ver/g" README.md
                    git commit -am "update README.md ({tool} $ver)"
                    git push
                  fi
        """,
    )

    run("git add --all")
    run('git commit -m "update repository from template"')
    top_commit = run("git rev-list --max-parents=0 HEAD", capture_output=True, text=True).stdout.strip()
    run(f"git tag -f add-commit-hash-here {top_commit}")
    run(f"git tag -f v1 {top_commit}")  # dependabot somehow needs this.
    run("git push -f origin main add-commit-hash-here v1")

for tool in tools:
    # continue
    repo = repo_name(tool)
    resp = client.post(
        f"https://api.github.com/repos/install-pinned/{repo}/actions/workflows/update.yml/dispatches",
        json={"ref": "main"},
    )
    print(resp)
    print(resp.read())

for tool in tools:
    # continue
    repo = repo_name(tool)
    resp = client.get(f"https://github.com/marketplace/actions/install-pinned-{repo}")
    print(f"{tool} marketplace release: {'✅' if resp.status_code == 200 else '❌'}")
    if resp.status_code != 200:
        print(f"https://github.com/install-pinned/{repo}/releases/new?tag=add-commit-hash-here")

"""
(() => {
    document.getElementById("release_repository_action_release_attributes_published_on_marketplace").click();
    document.getElementById("action-primary-category").value = "2";
    document.getElementById("action-secondary-category").value = "6";
    document.querySelector(".js-publish-release").click()
})()
"""
