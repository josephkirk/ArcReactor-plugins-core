import asyncio
import logging
import shutil
from arcreactor.core.interfaces.plugin import CorePlugin
from arcreactor.core.managers.source_control import SourceControlProvider

logger = logging.getLogger(__name__)

class GitProvider(SourceControlProvider):
    async def download(self, path: str, version: str, dest: str) -> bool:
        if not shutil.which("git"):
            logger.error("Git executable not found.")
            return False
            
        try:
            # Clone
            proc = await asyncio.create_subprocess_exec(
                "git", "clone", path, dest,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            if proc.returncode != 0:
                return False
                
            # Checkout version
            proc = await asyncio.create_subprocess_exec(
                "git", "checkout", version,
                cwd=dest,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            await proc.communicate()
            return proc.returncode == 0
        except Exception as e:
            logger.error(f"Git download failed: {e}")
            return False

    async def get_version(self, path: str) -> str:
        # Implementation for getting remote version (e.g. ls-remote)
        # For MVP, return "unknown" or implement properly
        return "unknown"

class GitCorePlugin(CorePlugin):
    async def initialize(self):
        if hasattr(self.context, "state") and hasattr(self.context.state, "source_control"):
            self.context.state.source_control.register_provider("git", GitProvider())
        else:
            logger.warning("Could not register GitProvider. SourceControlManager not found.")

    async def shutdown(self):
        pass
