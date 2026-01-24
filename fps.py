import psutil
import os
import time
from pynvml import *

# Inicializa NVIDIA
try:
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    NVIDIA_AVAILABLE = True
except:
    NVIDIA_AVAILABLE = False

def get_fps_kernel():
    """Lê o contador de interrupções da NVIDIA para calcular FPS real"""
    try:
        # Lemos o contador de interrupções da GPU (ajuste 'nv' se necessário)
        with open("/proc/interrupts", "r") as f:
            for line in f:
                if "nvidia" in line.lower():
                    # Soma as interrupções de todos os cores de CPU
                    return sum(int(x) for x in line.split() if x.isdigit())
    except:
        return 0
    return 0

def main():
    last_count = get_fps_kernel()
    last_time = time.time()
    
    try:
        while True:
            # Cálculo de FPS baseado no delta de interrupções
            current_count = get_fps_kernel()
            current_time = time.time()
            
            # FPS = variação das interrupções / tempo passado
            fps = (current_count - last_count) / (current_time - last_time)
            
            # Reset para a próxima volta
            last_count = current_count
            last_time = current_time

            # Outros dados
            cpu_usage = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            
            # Dados da GPU via NVML (mais precisos)
            if NVIDIA_AVAILABLE:
                temp_gpu = f"{nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)}°C"
                mem = nvmlDeviceGetMemoryInfo(handle)
                vram = f"{mem.used / 1024**2:.0f} / {mem.total / 1024**2:.0f} MB"
                load_gpu = f"{nvmlDeviceGetUtilizationRates(handle).gpu}%"
            else:
                temp_gpu = vram = load_gpu = "N/A"

            os.system('clear')
            print(f"===========================================")
            print(f"   AGENTE PERFORMANCE (KERNEL MONITOR)    ")
            print(f"===========================================")
            # Se o FPS for muito baixo, mostramos 0 (evita ruído de desktop)
            print(f" FPS REAL (GPU):   {int(fps) if fps > 1 else 0} FPS")
            print(f"-------------------------------------------")
            print(f" GPU: {load_gpu} | TEMP: {temp_gpu}")
            print(f" VRAM: {vram}")
            print(f"-------------------------------------------")
            print(f" CPU: {cpu_usage}%")
            print(f" RAM: {ram.percent}% ({ram.used // 1024**2}MB)")
            print(f"===========================================")
            print(" Monitorando interrupções da GTX 1060...")
            
            time.sleep(1) # Atualiza a cada 1 segundo para o cálculo de FPS bater
            
    except KeyboardInterrupt:
        print("\nEncerrado.")

if __name__ == "__main__":
    main()
