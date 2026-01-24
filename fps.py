import psutil
import os
import time
import socket
from pynvml import *

# ==========================================================
# CONFIGURAÇÕES DE PRECISÃO - AMAURI BUENO
# ==========================================================
ESP32_IP = "192.168.100.49"
ESP32_PORT = 5005

# NOVO FATOR: Ajustado para subir de 58 para a faixa de 70-80 FPS
FATOR_CORRECAO = 0.233  

# TEMPO DE ATUALIZAÇÃO: 10 segundos para máxima estabilidade
TEMPO_AMOSTRA = 4.0     

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Inicializa NVIDIA
try:
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    NVIDIA_AVAILABLE = True
except:
    NVIDIA_AVAILABLE = False

def get_fps_kernel():
    try:
        with open("/proc/interrupts", "r") as f:
            for line in f:
                if "nvidia" in line.lower():
                    return sum(int(x) for x in line.split() if x.isdigit())
    except:
        return 0
    return 0

def main():
    last_count = get_fps_kernel()
    last_time = time.time()
    
    print(f"Modo Precisão: 10s de leitura. Fator: {FATOR_CORRECAO}")
    
    try:
        while True:
            # Coleta dados por 10 segundos para eliminar oscilações
            time.sleep(TEMPO_AMOSTRA)
            
            current_count = get_fps_kernel()
            current_time = time.time()
            diff_time = current_time - last_time
            
            if diff_time <= 0: diff_time = 0.001
            
            # Cálculo do FPS real baseado no acumulado de 10 segundos
            raw_fps = (current_count - last_count) / diff_time
            corrected_fps = raw_fps * FATOR_CORRECAO
            
            # Arredondamento para o inteiro mais próximo
            final_fps = int(round(corrected_fps)) if corrected_fps > 2 else 0
            if final_fps > 999: final_fps = 999 

            # Coleta de GPU
            if NVIDIA_AVAILABLE:
                temp_gpu = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)
                load_gpu = nvmlDeviceGetUtilizationRates(handle).gpu
            else:
                temp_gpu = load_gpu = 0

            # Envio para o ESP32 (Creeper Auth)
            mensagem = f"{final_fps},{load_gpu},{temp_gpu}"
            try:
                sock.sendto(mensagem.encode(), (ESP32_IP, ESP32_PORT))
            except:
                pass

            # Feedback no Terminal
            os.system('clear')
            print(f"CALIBRAÇÃO DE PERFORMANCE - DEBIAN")
            print(f"-------------------------------------------")
            print(f" FPS CALCULADO (10s): {final_fps}")
            print(f" GPU: {load_gpu}% | TEMP: {temp_gpu}°C")
            print(f"-------------------------------------------")
            print(f" Fator atual: {FATOR_CORRECAO}")

            # Reset do ciclo
            last_count = current_count
            last_time = current_time
            
    except KeyboardInterrupt:
        if NVIDIA_AVAILABLE: nvmlShutdown()

if __name__ == "__main__":
    main()
