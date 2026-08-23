#!/usr/bin/env python3
"""Pubblica UnitStatus/eventi su MQTT, riconnessione con backoff.

SCHELETRO DI PIATTAFORMA — owner del contenuto: software-platform.
Questo file esiste perche' il workspace compili e perche' l'harness di test
abbia un bersaglio. Non contiene algoritmi: sostituiscilo, non aggirarlo.

Criterio di FATTO associato: Criterio: latenza <=2 s, riconnessione automatica <=30 s, 10/10.
Comando per eseguirlo:  ./scripts/fatto.sh software-platform
"""

import rclpy
from rclpy.node import Node


class BridgeNode(Node):
    """Segnaposto. Dichiara i parametri, non fa lavoro utile."""

    def __init__(self) -> None:
        super().__init__("bridge_node")
        self.declare_parameter("enabled", False)
        self.get_logger().info(
            "bridge_node: scheletro di piattaforma, nessuna logica implementata. "
            "Owner: software-platform."
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = BridgeNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
