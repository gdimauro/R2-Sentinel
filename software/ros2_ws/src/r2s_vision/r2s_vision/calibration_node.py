#!/usr/bin/env python3
"""Calibrazione geometrica camera/testa pan-tilt.

SCHELETRO DI PIATTAFORMA — owner del contenuto: vision-perception.
Questo file esiste perche' il workspace compili e perche' l'harness di test
abbia un bersaglio. Non contiene algoritmi: sostituiscilo, non aggirarlo.

Criterio di FATTO associato: Gate fase 3: >=25 fps end-to-end, mAP@50 >=0,85, <=1 FP/ora, latenza <=150 ms.
Comando per eseguirlo:  ./scripts/fatto.sh vision-perception
"""

import rclpy
from rclpy.node import Node


class CalibrationNode(Node):
    """Segnaposto. Dichiara i parametri, non fa lavoro utile."""

    def __init__(self) -> None:
        super().__init__("calibration_node")
        self.declare_parameter("enabled", False)
        self.get_logger().info(
            "calibration_node: scheletro di piattaforma, nessuna logica implementata. "
            "Owner: vision-perception."
        )


def main(args=None) -> None:
    rclpy.init(args=args)
    node = CalibrationNode()
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
