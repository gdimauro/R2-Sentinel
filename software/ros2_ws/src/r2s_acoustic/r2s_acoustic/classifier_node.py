#!/usr/bin/env python3
"""Classificazione firma alare -> AcousticEvent.

SCHELETRO DI PIATTAFORMA — owner del contenuto: acoustic-perception.
Questo file esiste perche' il workspace compili e perche' l'harness di test
abbia un bersaglio. Non contiene algoritmi: sostituiscilo, non aggirarlo.

Criterio di FATTO associato: Gate fase 5: recall >=0,90, <=1 FP/ora, latenza <=200 ms su RPi5 senza Hailo.
Comando per eseguirlo:  ./scripts/fatto.sh acoustic-perception
"""

import rclpy
from rclpy.node import Node


class ClassifierNode(Node):
    """Segnaposto. Dichiara i parametri, non fa lavoro utile."""

    def __init__(self) -> None:
        super().__init__("classifier_node")
        self.declare_parameter("enabled", False)
        self.get_logger().info(
            "classifier_node: scheletro di piattaforma, nessuna logica implementata. "
            "Owner: acoustic-perception."
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = ClassifierNode()
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
