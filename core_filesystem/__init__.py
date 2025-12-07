import logging
import shutil
from pathlib import Path
from arcreactor.core.interfaces.plugin import CorePlugin
from arcreactor.core.managers.source_control import SourceControlProvider

logger = logging.getLogger(__name__)

class FileSystemProvider(SourceControlProvider):
    async def download(self, path: str, version: str, dest: str) -> bool:
        try:
            # Construct source path: path_version
            # Example: path="C:/Plugins/MyPlugin", version="v1" -> "C:/Plugins/MyPlugin_v1"
            source_path = Path(f"{path}_{version}")
            
            if not source_path.exists():
                logger.error(f"Source path {source_path} does not exist.")
                return False
                
            if not source_path.is_dir():
                logger.error(f"Source path {source_path} is not a directory.")
                return False
            
            # Copy
            shutil.copytree(source_path, dest, dirs_exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"FileSystem download failed: {e}")
            return False

    async def get_version(self, path: str) -> str:
        return "local"

class FileSystemCorePlugin(CorePlugin):
    async def initialize(self):
        if hasattr(self.context, "state") and hasattr(self.context.state, "source_control"):
            self.context.state.source_control.register_provider("filesystem", FileSystemProvider())
        else:
            logger.warning("Could not register FileSystemProvider. SourceControlManager not found.")

    async def shutdown(self):
        pass
