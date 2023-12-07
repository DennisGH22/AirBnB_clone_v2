#!/usr/bin/python3
""" A Fabric script that generates a .tgz archive. """

from fabric import task
from datetime import datetime
import os

@task
def do_pack(c):
    """Generates a .tgz archive from the contents of the web_static folder."""

    # Create the versions folder if it doesn't exist
    c.local('mkdir -p versions')

    # Generate the timestamp for the archive name
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')

    # Create the archive path
    archive_path = 'versions/web_static_{}.tgz'.format(timestamp)

    # Compress the web_static folder into the archive
    result = c.local('tar -cvzf {} web_static'.format(archive_path))

    # Check if the archive has been correctly generated
    if result.failed:
        return None
    else:
        return archive_path
