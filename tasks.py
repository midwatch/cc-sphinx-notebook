from pathlib import Path

from invoke import Collection
from invoke import task

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git

GITHUB_USERNAME = "midwatch"
GITHUB_SLUG = "cc-sphinx-notebook"
CC_VERSION = "0.4.0"


@task
def init_repo(ctx):
    """Initialize freshly cloned repo"""
    git.init(ctx, GITHUB_USERNAME, GITHUB_SLUG, CC_VERSION)


ns = Collection(bumpversion, init_repo)
ns.add_collection(git.collection, name="scm")
