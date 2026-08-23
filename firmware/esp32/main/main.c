/*
 * R2-Sentinel — firmware ESP32-S3, scheletro di piattaforma.
 *
 * Owner del contenuto: mechatronics.
 * Questo file esiste per una ragione sola: dimostrare che la toolchain ESP-IDF
 * si ricostruisce con un comando e che il firmware compila da zero. Non pilota
 * nulla e non deve essere esteso qui dentro senza aggiornare package/Decision Log.
 *
 * Requisiti che vivranno qui (D-06):
 *   - loop di controllo a 1 kHz con jitter <= 100 us
 *   - arresto sui finecorsa entro 1 step
 *   - comando pan/tilt ricevuto via micro-ROS (r2s_interfaces/PanTiltCommand)
 */
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"

static const char *TAG = "r2s";

void app_main(void)
{
    ESP_LOGI(TAG, "R2-Sentinel ESP32-S3: scheletro di piattaforma, nessuna logica.");
    ESP_LOGI(TAG, "Owner del contenuto: mechatronics. Toolchain: vedi firmware/toolchain.yaml");
    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
