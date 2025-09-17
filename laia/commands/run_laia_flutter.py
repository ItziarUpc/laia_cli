import asyncio
import shutil
import os
from laiagenlib.Infrastructure.Openapi.LaiaFlutter import LaiaFlutter

async def run_laia_flutter(openapi_path, backend_folder_name, frontend_folder_name):
    flutter_bin = os.path.expandvars("$HOME/flutter/bin/flutter")
    flutter_path = shutil.which("flutter")

    if flutter_path is None and os.path.exists(flutter_bin):
        flutter_dir = os.path.dirname(flutter_bin)
        os.environ["PATH"] += os.pathsep + flutter_dir
        flutter_path = shutil.which("flutter")

    if flutter_path is None:
        print("❌ Flutter no está instalado ni disponible en $HOME/flutter/bin/flutter")
        return

    await LaiaFlutter(openapi_path, backend_folder_name, frontend_folder_name)
