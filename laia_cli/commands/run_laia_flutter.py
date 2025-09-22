import asyncio
import json
import shutil
import os
from laiagenlib.Infrastructure.Openapi.LaiaFlutter import LaiaFlutter

async def run_command(command, cwd=None):
    process = await asyncio.create_subprocess_exec(
        *command,
        cwd=cwd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    async def read_stream(stream, prefix=""):
        while True:
            line = await stream.readline()
            if not line:
                break
            print(prefix + line.decode().rstrip())

    await asyncio.gather(
        read_stream(process.stdout, ""),
        read_stream(process.stderr, "ERR: ")
    )

    return await process.wait()


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

    laia_config_path = os.path.join(os.getcwd(), "laia.json")
    with open(laia_config_path, "r", encoding="utf-8") as f:
        laia_config = json.load(f)

    await LaiaFlutter(openapi_path, backend_folder_name, frontend_folder_name, laia_config.get("use_access_rights", True))

    print("Ejecutando build_runner...")
    code = await run_command(
        [flutter_path, "pub", "run", "build_runner", "build", "--delete-conflicting-outputs"],
        cwd=frontend_folder_name
    )
    if code != 0:
        print("❌ Error en build_runner")
        return

    print("Ejecutando flutter run...")
    await run_command([flutter_path, "run", "-d", "chrome"], cwd=frontend_folder_name)
