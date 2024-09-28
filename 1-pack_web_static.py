#!/usr/bin/python3
"""Generates a .tgz archive from the contents of the `web_static` folder
"""

import os
from datetime import datetime
from fabric.api import local, runs_once


@runs_once
def do_pack():
    """Packs static files
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
