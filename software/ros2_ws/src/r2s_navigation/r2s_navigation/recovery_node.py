#!/usr/bin/env python3
"""Recupero da blocco entro 60 s, altrimenti STATE_SAFE.

SCHELETRO DI PIATTAFORMA — owner del contenuto: autonomy.
Questo file esiste perche' il workspace compili e perche' l'harness di test
abbia un bersaglio. Non contiene algoritmi: sostituiscilo, non aggirarlo.

Criterio di FATTO associato: Gate fase 7: chiusura d'anello <=10 cm su >=60 m2, 20/20 agganci, 0 collisioni in 2 h.
Comando per eseguirlo:  ./scripts/fatto.sh autonomy
"""

import rclpy
from rclpy.node import Node


class RecoveryNode(Node):
    """Segnaposto. Dichiara i parametri, non fa lavoro utile."""

    def __init__(self) -> None:
        super().__init__("recovery_node")
        self.declare_parameter("enabled", False)
        self.get_logger().info(
            "recovery_node: scheletro di piattaforma, nessuna logica implementata. "
            "Owner: autonomy."
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = RecoveryNode()
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
