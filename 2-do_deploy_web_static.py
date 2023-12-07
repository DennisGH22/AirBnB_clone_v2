#!/usr/bin/python3
""" A Fabric script that generates a .tgz archive. """


from fabric.api import local, put, run, env
from os.path import exists, join, isfile
from datetime import datetime


env.hosts = ['54.237.94.18', '100.26.154.55']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers and deploys it."""

    if not isfile(archive_path):
        return False

    try:
        # Extract name without extension from the archive path
        archive_name = archive_path.split('/')[-1][:-4]

        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp')

        # Create necessary folders and extract the archive
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(archive_name, archive_name))

        # Remove the uploaded archive from the web server
        run('rm /tmp/{}.tgz'.format(archive_name))

        # Move contents and update symbolic link
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(archive_name, archive_name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(archive_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name))

        print("New version deployed!")
        return True

    except:
        return False
