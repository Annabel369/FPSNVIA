📋 Guia de Instalação: Agente de Performance NVIDIA (Debian)

Se você formatar o PC ou quiser disponibilizar para o público, estes são os passos exatos:
1. Dependências do Sistema (S.O.)

Primeiro, instale as ferramentas base para leitura de hardware e sensores no Debian:
Bash

sudo apt update
sudo apt install python3-venv python3-dev lm-sensors nvidia-smi -y
sudo sensors-detect --auto

2. Configuração do Ambiente Python

Crie e ative o ambiente virtual para manter o sistema limpo:
Bash

# Criando o ambiente
python3 -m venv meu_agente_env

# Ativando
source meu_agente_env/bin/activate

# Instalando as bibliotecas necessárias
pip install psutil nvidia-ml-py

3. Lista de Bibliotecas (requirements.txt)

Para o seu GitHub, crie um arquivo chamado requirements.txt. Assim, qualquer um pode instalar tudo com um único comando (pip install -r requirements.txt):
Plaintext

psutil
nvidia-ml-py

4. O Script Principal (agente_performance.py)

Recomendo colocar o código final que funcionou (o que lê o /proc/interrupts) em um arquivo com esse nome.
5. Como usar (Passo a Passo para o README.md)

No seu GitHub, adicione estas instruções no README.md:

    🚀 Como executar

        Certifique-se de estar usando o driver proprietário da NVIDIA.

        Ative o ambiente virtual: source meu_agente_env/bin/activate.

        Importante: Como o script lê dados brutos do Kernel (/proc/interrupts) para calcular o FPS sem depender de X11/Wayland, ele deve ser executado como root ou com sudo:
        Bash

        sudo ./meu_agente_env/bin/python agente_performance.py

🛠 Por que este projeto é útil para o público?

Se você for escrever a descrição no GitHub, aqui está uma sugestão de "Diferencial":

    Compatível com Wayland: Diferente do MangoHud ou nvidia-settings que falham no GNOME/Wayland, este agente usa contadores de interrupção do Kernel.

    Baixo Consumo: Feito em Python, utiliza NVML oficial para dados da GPU.

    Sem Injeção de Código: Não precisa de comandos extras na Steam, evitando que jogos fechem por conflito de bibliotecas.
