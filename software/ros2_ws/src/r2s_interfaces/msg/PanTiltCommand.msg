# Comando alla testa pan-tilt, consumato dal firmware ESP32-S3 via micro-ROS.
# Owner dell'implementazione: mechatronics. Requisito di riferimento: D-06,
# errore di puntamento <=1,0 gradi a 5 m.

builtin_interfaces/Time stamp
float32 pan_deg           # assoluto, riferito allo zero dei finecorsa
float32 tilt_deg
float32 max_speed_deg_s   # 0 = usa il default del firmware
bool    enable            # false = disabilita i driver (stato sicuro)
