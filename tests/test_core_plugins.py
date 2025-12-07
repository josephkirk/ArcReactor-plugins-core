import pytest
from fastapi import FastAPI
from arcreactor.core.managers.plugin_manager import PluginManager
from arcreactor.core.managers.source_control import SourceControlManager
from arcreactor.core.managers.project_manager import ProjectManager, YamlProvider
from arcreactor.core.interfaces.plugin import PluginTiming


@pytest.mark.asyncio
async def test_core_plugins_load():
    # Setup App Context
    app = FastAPI()
    app.state.source_control = SourceControlManager()
    app.state.project_manager = ProjectManager(provider=YamlProvider())
    
    # Initialize PluginManager pointing to real plugins dir
    # Assuming tests are run from root
    plugin_manager = PluginManager(plugin_dir="src/arcreactor/plugins", config_path="test-config.toml", context=app)
    app.state.plugin_manager = plugin_manager
    
    # Load Pre-Init Plugins
    await plugin_manager.load_plugins(PluginTiming.PRE_INIT)
    
    # Verify TomlProvider
    # It should have replaced the provider in project_manager
    # Note: Using class name check to avoid issues with double-importing module if plugin manager loads it differently
    assert type(app.state.project_manager.provider).__name__ == "TomlProvider"
    
    # Verify Source Control Providers
    assert app.state.source_control.get_provider("git") is not None
    assert app.state.source_control.get_provider("filesystem") is not None
    assert app.state.source_control.get_provider("zip") is not None
    
    # Verify SubprocessService
    assert hasattr(app.state, "subprocess_launcher")
    assert app.state.subprocess_launcher is not None
