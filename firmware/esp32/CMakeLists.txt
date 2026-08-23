# Progetto ESP-IDF — ESP32-S3, livello motori via micro-ROS (PROJECT.md §6).
# SCHELETRO DI PIATTAFORMA. Owner del contenuto: mechatronics.
# Serve a verificare che la toolchain si ricostruisca e che il firmware compili
# da zero: e' un criterio di riproducibilita', non un firmware funzionante.
cmake_minimum_required(VERSION 3.16)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(r2s_esp32)
