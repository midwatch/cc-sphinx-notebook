from pathlib import Path

from dotenv import dotenv_values

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git

config = dotenv_values(".env")

@task
def clean_build(ctx):
    """
    Clean up files from package building
    """
    ctx.run("rm -fr build/")


@task(pre=[clean_build])
def clean(ctx):
    """
    Runs all clean sub-tasks
    """
    pass


@task(clean)
def build(ctx):
    """
    Build html pages.
    """
    ctx.run('mkdir build')
    ctx.run('cp -r notebook build/rst')
    ctx.run(f'sphinx_notebook build notebook/ build/rst/index.rst')
    ctx.run('sphinx-build -b html build/rst build/www')


@task
def init_repo(ctx):
    """Initialize freshly cloned repo"""
    with Path("project.d/version_cc").open() as fd_in:
        version = fd_in.read().strip()
        commit_msg = f'new package from midwatch/cc-sphinx-notebook ({version})'

        git.init(ctx, config['GITHUB_USERNAME'], config['GITHUB_SLUG'],
                 commit_msg)


@task(help={'target': 'develop (default) or main'}, pre=[clean, build])
def release(ctx, target='develop'):
    """
    Build notebook and release to target
    """
    PATH_LOCAL = config['RELEASE_PATH_LOCAL']

    if target == 'main':
        DOMAIN = config['RELEASE_MAIN_DOMAIN']
        HOST = config['RELEASE_MAIN_HOST']
        PATH_REMOTE = config['RELEASE_MAIN_PATH']
        USER = config['RELEASE_MAIN_USER']

    else:
        DOMAIN = config['RELEASE_DEVELOP_DOMAIN']
        HOST = config['RELEASE_DEVELOP_HOST']
        PATH_REMOTE = config['RELEASE_DEVELOP_PATH']
        USER = config['RELEASE_DEVELOP_USER']

    ctx.run(f'rsync -r --delete {PATH_LOCAL} {USER}@{HOST}.{DOMAIN}:{PATH_REMOTE}')

ns = Collection(bumpversion, build, clean, release)
ns.add_task(init_repo, name='init')

ns.add_collection(git.collection, name="scm")
