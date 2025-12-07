import asyncio
import logging
from typing import Optional, Tuple
from arcreactor.core.interfaces.plugin import CorePlugin

logger = logging.getLogger(__name__)

class SubprocessService:
    async def run(self, command: str, cwd: Optional[str] = None) -> Tuple[int, str, str]:
        """
        Runs a shell command asynchronously.
        Returns (returncode, stdout, stderr).
        """
        logger.info(f"Running command: {command} in {cwd}")
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd
        )
        stdout, stderr = await process.communicate()
        return process.returncode, stdout.decode(), stderr.decode()

class SubprocessPlugin(CorePlugin):
    async def initialize(self):
        if hasattr(self.context, "state"):
            self.context.state.subprocess_launcher = SubprocessService()
            logger.info("SubprocessService registered.")
        else:
            logger.warning("Could not register SubprocessService. Context state not found.")

    async def shutdown(self):
        pass
