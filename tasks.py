from pathlib import Path

from invoke import Collection
from invoke import task

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git


@task
def init_repo(ctx):
    """Initialize freshly cloned repo"""
    git.init(ctx)


ns = Collection(bumpversion, init_repo)
ns.add_collection(git.collection, name="scm")
