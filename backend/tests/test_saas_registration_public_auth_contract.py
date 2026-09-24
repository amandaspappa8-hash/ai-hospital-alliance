from backend.app.route_security_policy_approved import (
    classify_approved,
)
from backend.app.route_security_policy_generated import (
    classify_generated,
)
from backend.app.route_security_registry import classify


REGISTER_PATH = "/saas/register"


def test_saas_registration_is_public_in_runtime_registry():
    assert classify(REGISTER_PATH) == "PUBLIC"


def test_saas_registration_is_public_in_generated_policy():
    assert classify_generated(REGISTER_PATH) == "PUBLIC"


def test_saas_registration_is_public_in_approved_policy():
    assert classify_approved(REGISTER_PATH) == "PUBLIC"


def test_neighboring_saas_control_plane_routes_remain_protected():
    assert classify("/saas/plans") == "PROTECTED"
    assert classify("/saas/tenants") == "PROTECTED"


def test_unknown_route_remains_fail_closed():
    assert classify("/definitely-not-a-public-route") == "PROTECTED"
