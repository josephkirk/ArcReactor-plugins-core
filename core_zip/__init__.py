import logging
import shutil
from pathlib import Path
from arcreactor.core.interfaces.plugin import CorePlugin
from arcreactor.core.managers.source_control import SourceControlProvider

logger = logging.getLogger(__name__)

class ZipFileProvider(SourceControlProvider):
    async def download(self, path: str, version: str, dest: str) -> bool:
        try:
            # Construct source path: path_version.zip
            # Example: path="C:/Plugins/MyPlugin", version="v1" -> "C:/Plugins/MyPlugin_v1.zip"
            source_path = Path(f"{path}_{version}.zip")
            
            if not source_path.exists():
                logger.error(f"Source zip {source_path} does not exist.")
                return False
                
            if not source_path.is_file():
                logger.error(f"Source path {source_path} is not a file.")
                return False
            
            # Unpack
            shutil.unpack_archive(source_path, dest)
            return True
        except Exception as e:
            logger.error(f"ZipFile download failed: {e}")
            return False

    async def get_version(self, path: str) -> str:
        return "local"

class ZipFileCorePlugin(CorePlugin):
    async def initialize(self):
        if hasattr(self.context, "state") and hasattr(self.context.state, "source_control"):
            self.context.state.source_control.register_provider("zip", ZipFileProvider())
        else:
            logger.warning("Could not register ZipFileProvider. SourceControlManager not found.")

    async def shutdown(self):
        pass
