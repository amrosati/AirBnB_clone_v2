#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the `web_static` folder
"""

import os
from datetime import datetime
from fabric.api import local, env, run, put

# List of web servers
env.user = 'ubuntu'
env.hosts = ["34.224.4.6", "18.208.120.244"]


def do_pack():
    """Packs static files.

    Returns:
        str: Path to the packed static files, None otherwise.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    dt = datetime.now().strftime('%Y%m%d%H%M%S')
    path = f"versions/web_static_{dt}.tgz"

    try:
        print(f"Packing web_static to {path}")
        local(f"tar -cvzf {path} web_static")

        size = os.stat(archive_path).st_size
        print(f"web_static packed: {path} -> {size}Bytes")
    except:
        return None

    return path


def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the web static archive file.

    Returns:
        bool: True if deployed successfully, False otherwise.
    """
    try:
        if not archive_path:
            raise

        archive = archive_path.split('/')[-1]
        path = "/data/web_static/releases/" + archive.strip('.tgz')

        put(archive_path, "/tmp")

        run(f"mkdir -p {path}/")
        run(f"tar -xzf /tmp/{archive} -C {path}")
        run(f"rm /tmp/{archive}")
        run(f"mv {path}/web_static/* {path}")
        run(f"rm -rf {path}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {path} /data/web_static/current")

        print("New version deployed!")
    except:
        return False

    return True


def deploy():
    """Packs and deploys static files.

    Returns:
        bool: True if everything finished successfully, False otherwise.
    """
    archive = do_pack()
    deployed = do_deploy(archive)

    return deployed
