from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git

GITHUB_USERNAME = "{{ cookiecutter.github_username }}"
GITHUB_SLUG = "{{ cookiecutter.repo_slug }}"
CC_VERSION = "0.5.1"

RSYNC_HOST = "host"
RSYNC_USER = "user"
RSYNC_PATH_LOCAL = "build/www/"
RSYNC_PATH_REMOTE = "remote path"

TEMPLATE_NAME = "{{ cookiecutter.index_template }}.rst.jinja"

ROOT_DIR = Path(__file__).parent


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
    options = ' '.join((
        f'--template-name {TEMPLATE_NAME}',
        'notebook/',
        'build/rst/index.rst'
        ))

    ctx.run('mkdir build')
    ctx.run('cp -r notebook build/rst')
    ctx.run(f'sphinx_notebook build {options}')
    ctx.run('sphinx-build -b html build/rst build/www')


@task
def init_repo(ctx):
    """Initialize freshly cloned repo"""
    git.init(ctx, GITHUB_USERNAME, GITHUB_SLUG, CC_VERSION)


@task(pre=[clean, build])
def release(ctx):
    """
    Make a release of the python package to pypi
    """
    # ctx.run(f'rsync -r --delete {RSYNC_PATH_LOCAL} {RSYNC_USER}@{RSYNC_HOST}:{RSYNC_PATH_REMOTE}')


ns = Collection(build, clean, init_repo, release)
ns.add_collection(git.collection, name="scm")
