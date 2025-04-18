# example run
# uv run python -m ops_tools.dns_git_check \
#   --domains mydomain1.com mydomain2.com --git-dir /top/my-dns-repo
import argparse
import json
import os
import subprocess

from ops_tools import dns_fetch


def check_git_clean(args):
    git_status = subprocess.run(
        [
            "git",
            "diff-index",
            "--quiet",
            "HEAD",
        ]
    )
    if git_status.returncode:
        raise Exception(f"git repo {args.git_dir} is not clean")


def main(args):
    os.chdir(args.git_dir)
    check_git_clean(args)

    for domain in args.domains:
        repr = dns_fetch.process_domain(
            domain=domain,
            format=dns_fetch.JSON,
        )
        data = json.dumps(repr, sort_keys=True, indent=2)
        with open(file=f"./{domain}", mode="w") as ff:
            ff.write(data)

    check_git_clean(args)  # did anything change


_arg_parser = argparse.ArgumentParser()
_arg_parser.add_argument(
    "--domains",
    metavar="S",
    type=str,
    nargs="+",
    required=True,
    help="a list of strings",
)
_arg_parser.add_argument(
    "--git-dir",
    type=str,
    required=True,
    help="the dns data git repo dir",
)

if __name__ == "__main__":
    main(_arg_parser.parse_args())
