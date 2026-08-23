from fastapi import FastAPI

from backend.app.plugins.agi_plugin import plugin as agi_plugin
from backend.app.plugins.precision_plugin import plugin as precision_plugin
from backend.app.plugins.research_plugin import plugin as research_plugin
from backend.app.plugins.global_intelligence_plugin import plugin as global_intelligence_plugin


PLUGINS = [
    agi_plugin,
    precision_plugin,
    research_plugin,
    global_intelligence_plugin,
]


def load_plugins(app: FastAPI):
    loaded = []

    for plugin in PLUGINS:
        plugin.register(app)
        loaded.append({
            "name": plugin.name,
            "version": plugin.version,
            "category": plugin.category,
            "description": plugin.description,
        })

    return loaded
