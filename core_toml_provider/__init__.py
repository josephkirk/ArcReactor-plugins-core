from pathlib import Path
from typing import List, Optional, Dict, Any
import toml
from arcreactor.core.interfaces.plugin import CorePlugin
from arcreactor.core.managers.project_manager import ProjectProvider, Project

class TomlProvider(ProjectProvider):
    def __init__(self, config_path: str = "projects.toml"):
        self.config_path = Path(config_path)
        self._ensure_config()

    def _ensure_config(self):
        if not self.config_path.exists():
            self._write_config({"projects": []})

    def _write_config(self, data: dict):
        with open(self.config_path, "w") as f:
            toml.dump(data, f)

    def _load_config(self) -> Dict[str, Any]:
        with open(self.config_path, "r") as f:
            return toml.load(f) or {"projects": []}

    def get_project(self, name: str) -> Optional[Project]:
        data = self._load_config()
        for p_data in data.get("projects", []):
            if p_data["name"] == name:
                return Project(**p_data)
        return None

    def list_projects(self) -> List[Project]:
        data = self._load_config()
        return [Project(**p) for p in data.get("projects", [])]

    def create_project(self, project: Project):
        data = self._load_config()
        projects = data.get("projects", [])
        
        for p in projects:
            if p["name"] == project.name:
                raise ValueError(f"Project {project.name} already exists")
        
        p_dict = project.dict()
        # Convert datetime to string for TOML
        if "created_at" in p_dict:
            p_dict["created_at"] = p_dict["created_at"].isoformat()
            
        projects.append(p_dict)
        data["projects"] = projects
        self._write_config(data)

    def delete_project(self, name: str):
        data = self._load_config()
        projects = [p for p in data.get("projects", []) if p["name"] != name]
        data["projects"] = projects
        self._write_config(data)

class TomlCorePlugin(CorePlugin):
    async def initialize(self):
        # Register TomlProvider
        # Assuming context is FastAPI app and state has project_manager
        if hasattr(self.context, "state") and hasattr(self.context.state, "project_manager"):
             # Replace the provider
             # Note: This is a simple replacement. In a real system we might want to support multiple or configuration.
             self.context.state.project_manager.provider = TomlProvider()
             print("TomlProvider registered and active.")
        else:
            print("Warning: Could not register TomlProvider. ProjectManager not found in context.")

    async def shutdown(self):
        pass
