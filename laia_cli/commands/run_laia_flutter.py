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


async def run_laia_flutter(frontend_folder_name):
    flutter_path = shutil.which("flutter")

    print("Ejecutando flutter run...")
    await run_command([flutter_path, "run", "-d", "web-server", "--web-port", "8080", "--web-hostname", "0.0.0.0"], cwd=frontend_folder_name)
