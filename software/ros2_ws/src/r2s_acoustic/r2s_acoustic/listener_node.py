#!/usr/bin/env python3
"""Acquisizione I2S e finestratura.

SCHELETRO DI PIATTAFORMA — owner del contenuto: acoustic-perception.
Questo file esiste perche' il workspace compili e perche' l'harness di test
abbia un bersaglio. Non contiene algoritmi: sostituiscilo, non aggirarlo.

Criterio di FATTO associato: Gate fase 5: recall >=0,90, <=1 FP/ora, latenza <=200 ms su RPi5 senza Hailo.
Comando per eseguirlo:  ./scripts/fatto.sh acoustic-perception
"""

import rclpy
from rclpy.node import Node


class ListenerNode(Node):
    """Segnaposto. Dichiara i parametri, non fa lavoro utile."""

    def __init__(self) -> None:
        super().__init__("listener_node")
        self.declare_parameter("enabled", False)
        self.get_logger().info(
            "listener_node: scheletro di piattaforma, nessuna logica implementata. "
            "Owner: acoustic-perception."
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ListenerNode()
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
