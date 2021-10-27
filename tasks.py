from pathlib import Path

from invoke import Collection
from invoke import task


@task
def scm_push(ctx):
    """Push all branches and tags to origin."""

    for branch in ('develop', 'main'):
        ctx.run('git push origin {}'.format(branch))

    ctx.run('git push --tags')


@task
def scm_status(ctx):
    """Show status of remote branches."""
    ctx.run('git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads')


@task
def init(ctx):
    """Initialize freshly cloned repo."""
    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix v_')


scm = Collection()
scm.add_task(scm_push, name="push")
scm.add_task(scm_status, name="status")

ns = Collection(init)
ns.add_collection(scm, name="scm")
