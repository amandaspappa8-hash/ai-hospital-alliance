from .ahos_future import register_ahos_future
from .ahos_enterprise import register_enterprise
from .clinical import register_clinical
from .radiology import register_radiology
from .pharmacy import register_pharmacy
from .laboratory import register_laboratory
from .research import register_research


def register_all_routers(app):
    register_clinical(app)
    register_radiology(app)
    register_pharmacy(app)
    register_laboratory(app)
    register_research(app)
    # AHOS R13C.16A: enterprise routers are already registered
    # directly by backend.app.main; avoid duplicate registration.
    # register_enterprise(app)
    # register_ahos_future(app)  # disabled: now loaded by Plugin Architecture
