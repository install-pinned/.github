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

access_token = Path("github_token.txt").read_text().strip()

client = httpx.Client(
    headers={
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }
)

repos_dir = (Path(__file__).parent / "repos").absolute()

tools = json.loads(Path("tools.json").read_text())
python_versions = ["3.7", "3.8", "3.9", "3.10"]

if False:
    for tool in tools:
        resp = client.post(
            "https://api.github.com/orgs/install-pinned/repos",
            json={
                "name": tool,
                "license_template": "mit",
            },
        )
        print(resp)
        print(resp.read())

if False:
    for tool in tools:
        resp = client.patch(
            f"https://api.github.com/repos/install-pinned/{tool}",
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
    if (repos_dir / tool).exists():
        def make_writable(function, path, _exception):
            os.chmod(path, stat.S_IWRITE)
            function(path)


        shutil.rmtree(repos_dir / tool, onerror=make_writable)

    run(f"git clone git@github.com:install-pinned/{tool}.git", cwd=repos_dir)

for tool in tools:
    os.chdir(repos_dir / tool)

    def write(filename: str, contents: str) -> None:
        f = Path(filename)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(dedent(contents), encoding="utf-8", newline="\n")

    # modify one of this pins to make sure that the CI runs.
    write("pins/requirements-3.10.txt", "")

    try:
        last_release = re.search(r"(?<=@)[0-9a-f]{40}.+", Path("README.md").read_text())[0]
    except Exception:
        last_release = "ffffffffffffffffffffffffffffffffffffffff"
    write(
        "README.md",
        f"""
        
        # install-pinned/{tool}
        
        ![](https://shields.io/badge/python-{'%20%7C%20'.join(python_versions)}-blue)
        
        Securely install the latest [{tool}](https://pypi.org/project/{tool}/) release from PyPI.
        
        This action installs a pinned version of **{tool}** and all its dependencies, \
        making sure that file hashes match. Pinning your dependencies stops supply chain attacks where an adversary \
        replaces {tool} or one of its dependencies with malicious code.
        
        ## Usage
        
        In your GitHub Actions workflow, use this action like so:
        
        ```yaml
        - name: Install {tool} from PyPI
          uses: install-pinned/{tool}@{last_release}
        ```
        
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
        name: 'install-pinned/{tool}'
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
            - uses: install-pinned/pip-tools@41f7e8a0605d3487afde2503a5b352b2126b0873  # 6.9.0
            - run: pip-compile --allow-unsafe --generate-hashes pins/requirements.in -o pins/requirements-{py}.txt 
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
                    ver=$(curl -Ls https://pypi.org/pypi/{tool}/json | jq -r .info.version)
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
    run("git push")

for tool in tools:
    resp = client.post(
        f"https://api.github.com/repos/install-pinned/{tool}/actions/workflows/update.yml/dispatches",
        json={"ref": "main"},
    )
    print(resp)
    print(resp.read())
