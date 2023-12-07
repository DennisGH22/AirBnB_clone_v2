#!/usr/bin/python3
""" A Fabric script that generates a .tgz archive. """


from fabric.api import local
from os.path import exists, join
from datetime import datetime


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
