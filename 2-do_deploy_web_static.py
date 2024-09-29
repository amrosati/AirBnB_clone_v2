#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the `web_static` folder
"""

import os
from datetime import datetime
from fabric.api import local, runs_once, env, run, put

# List of web servers
env.hosts = ["34.224.4.6", "18.208.120.244"]


@runs_once
def do_pack():
    """Packs static files

    Returns:
        str: Path to the packed static files, None otherwise
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")

    dt = datetime.now()
    op = "versions/web_static_{}{}{}{}{}{}.tgz".format(
                dt.year, dt.month, dt.day,
                dt.hour, dt.minute, dt.second
            )

    try:
        print(f"Packing web_static to {op}")
        local(f"tar -cvzf {op} web_static")

        op_size = os.stat(op).st_size
        print(f"web_static packed: {op} -> {op_size} Bytes")
    except Exception:
        return None

    return op


def do_deploy(archive_path):
    """Distributes an archive to the web servers

    Args:
        archive_path (str): Path to the web static archive file

    Returns:
        bool: True if deployed successfully, False otherwise
    """
    if not os.path.exists(archive_path):
        return False

    filename = os.path.basename(archive_path)
    dirname = filename.replace('.tgz', '')
    dirpath = f"/data/web_static/releases/{dirname}/"

    try:
        put(archive_path, f"/tmp/{filename}")
        run(f"mkdir -p {dirpath}")
        run(f"tar -xzf /tmp/{filename} -C {dirpath}")
        run(f"rm /tmp/{filename}")
        run(f"mv {dirpath}web_static/* {dirpath}")
        run(f"rm -rf {dirpath}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {dirpath} /data/web_static/current")
        print("New version deployed!")
    except Exception:
        return False

    return True
