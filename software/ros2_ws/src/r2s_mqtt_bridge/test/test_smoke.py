"""Smoke test di piattaforma: gira in CI, non richiede hardware.

Verifica solo che il pacchetto sia importabile e che il nodo si costruisca.
Se questo fallisce il problema e' del workspace, non dell'algoritmo.
"""
import pytest


@pytest.mark.ci
def test_import_package():
    import r2s_mqtt_bridge  # noqa: F401


@pytest.mark.ci
def test_nodes_importable():
    from r2s_mqtt_bridge import bridge_node  # noqa: F401
    from r2s_mqtt_bridge import topic_lint  # noqa: F401
