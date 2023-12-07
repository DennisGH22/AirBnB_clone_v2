#!/usr/bin/python3
""" A Fabric script that generates a .tgz archive. """


from fabriapi import local, put, run, path
from os.path import exists, join
from datetime import datetime


env.hosts = ['54.237.94.18', '100.26.154.55']


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

    # Check if the archive file exists
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory on the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/ folder
        archive_filename = archive_path.split('/')[-1]
        archive_folder = '/data/web_static/releases/{}'.format(
            archive_filename.split('.')[0]
        )
        run('mkdir -p {}'.format(archive_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, archive_folder))

        # Remove the uploaded archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the extracted archive to the web_static folder
        run('mv {}/web_static/* {}'.format(archive_folder, archive_folder))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(archive_folder))

        print('New version deployed!')
        return True

    except Exception as e:
        print('Deployment failed:', str(e))
        return False
