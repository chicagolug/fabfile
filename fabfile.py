import fabric.api as fab

import fabric.contrib.project as project
import os
import shutil

# Remote server configuration
# user@host:port
host = [ "user@url-or-ip-address:port_number" ]

# Local path configuration (can be absolute or relative to fabfile)
#local build path
fab.env.deploy_path    = "output"
#my pelican theme static folder
fab.env.static_path    = "korgi/static"
#beta deploy path on the webserver
fab.env.beta_dest_path = "/srv/public/test/chicagolug.org/"
#the live deploy path on the webserver
fab.env.live_dest_path = "/srv/public/chicagolug.org/"


def startdev():
    """
        serve files locally via the development server
    """
    fab.local("./develop_server.sh start")


def stopdev():
    """
        stop the local development server
    """
    fab.local("./develop_server.sh stop")


def clean():
    """
        do a local cleanup
    """
    if os.path.isdir(fab.env.deploy_path):
        fab.local("rm -rf {deploy_path}".format(**fab.env))
        fab.local("mkdir {deploy_path}".format(**fab.env))

def build():
    """
        build the site locally
    """
    clean()
    fab.local("make html".format(**fab.env))


@fab.hosts(host)
def test():
    """
        build and deploy the site to the test url
        http://test.chicagolug.org
    """
    build()
    project.rsync_project(
        remote_dir=fab.env.beta_dest_path,
        #excluded files
        exclude="",
        local_dir=fab.env.deploy_path.rstrip("/") + "/",
        delete=True
    )


@fab.hosts(host)
def live():
    """
        build and deploy the live site
        http://chicagolug.org
    """
    build()
    project.rsync_project(
        remote_dir=fab.env.live_dest_path,
        #excluded files
        exclude="",
        local_dir=fab.env.deploy_path.rstrip("/") + "/",
        delete=True
    )
