from pathlib import Path

from dotenv import dotenv_values

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure

from mw_dry_invoke import bumpversion
from mw_dry_invoke import git

config = dotenv_values(".env")

with Path("project.d/version_cc").open() as fd_in:
    config['VERSION_CC'] = fd_in.read().strip()


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
    git.init(ctx, config['GITHUB_USERNAME'], config['GITHUB_SLUG'],
             config['VERSION_CC'])


@task(help={'target': 'develop or main'}, pre=[clean, build])
def release(ctx, target):
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

ns = Collection(bumpversion, build, clean, init_repo, release)
ns.add_collection(git.collection, name="scm")
