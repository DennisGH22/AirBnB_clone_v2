#!/usr/bin/python3
""" A Fabric script that generates a .tgz archive. """


from fabric.api import local, put, run, env, path
from os.path import exists, join, isfile
from datetime import datetime


env.hosts = ['54.237.94.18', '100.26.154.55']
env.user = 'ubuntu'


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Check if the 'versions' folder exists; create it if not
    if not exists("versions"):
        local("mkdir versions")

    # Generate the timestamp for the archive name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the archive path using os.path.join
    # for better cross-platform compatibility
    archive_path = join("versions", "web_static_{}.tgz".format(timestamp))

    # Create the tar archive
    local('tar cvfz "{}" .'.format(archive_path))

    # Check if the archive has been correctly generated
    if exists(archive_path):
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers and deploys it."""

    if not path.isfile(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp')

        # Extract name without extension from the archive path
        archive_name = archive_path.split('/')[-1][:-4]

        # Create necessary folders and extract the archive
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(archive_name))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'.format(
            archive_name, archive_name))

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
