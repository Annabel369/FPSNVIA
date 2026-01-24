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

O Arquivo de Serviço Final (/etc/systemd/system/creeper-stats.service)

Abra o arquivo para edição:
Bash

sudo nano /etc/systemd/system/creeper-stats.service

Apague o que estiver lá e cole este bloco ajustado:
Ini, TOML

[Unit]
Description=Agente de Performance Creeper - Amauri
After=network.target

[Service]
# Caminho exato para o Python do Venv e para o seu script fps.py
ExecStart=/root/meu_agente_env/bin/python3 /root/fps.py
Restart=always
RestartSec=5
User=root
WorkingDirectory=/root

[Install]
WantedBy=multi-user.target

Comandos para ativar agora:

    Recarregue o sistema: sudo systemctl daemon-reload

    Habilite para iniciar no boot: sudo systemctl enable creeper-stats.service

    Inicie o serviço: sudo systemctl restart creeper-stats.service

    Confira se está rodando: sudo systemctl status creeper-stats.service

Dica para o Futuro:

Se você precisar alterar o Fator de Correção no seu fps.py, lembre-se que após salvar o arquivo você precisa reiniciar o serviço para as mudanças valerem no visor: sudo systemctl restart creeper-stats.service

Agora seu agente fps.py está oficializado como um processo do sistema Debian!
