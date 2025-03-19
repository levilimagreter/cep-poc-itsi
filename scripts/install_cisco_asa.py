#!/usr/bin/env python3

import os
import subprocess

# Definição dos add-ons e seus respectivos caminhos
addons = {
    "Cisco ASA": "/home/splunkuser/splunk-add-on-for-cisco-asa_520.tgz",
    "Unix & Linux": "/home/splunkuser/splunk-add-on-for-unix-and-linux_1000.tgz"
}

def install_addon(name, path):
    """Instala um add-on do Splunk a partir de um arquivo local."""
    print(f"=== Instalando o Splunk Add-on para {name} ===")

    # Verifica se o arquivo do add-on existe
    if os.path.exists(path):
        print(f"✅ {name} encontrado! Ajustando permissões...")
        os.system(f"sudo chmod +r {path}")  # Garante permissão de leitura
        os.system(f"sudo -u splunkuser tar -xvf {path} -C /opt/splunk/etc/apps/")
        os.system("sudo chown -R splunkuser:splunkuser /opt/splunk/etc/apps/")
        print(f"✅ Add-on {name} instalado com sucesso!")
    else:
        print(f"❌ ERRO: Arquivo {path} não encontrado.")
        print("➡ Certifique-se de que o Add-on foi baixado e está na pasta /home/splunkuser/")
        return False
    return True

def restart_splunk():
    """Reinicia o Splunk para aplicar as mudanças."""
    print("\n🔄 Reiniciando o Splunk para aplicar as mudanças...")
    os.system("sudo -u splunkuser /opt/splunk/bin/splunk restart")

def main():
    success = True
    for name, path in addons.items():
        success &= install_addon(name, path)

    if success:
        restart_splunk()
        print("\n✅ Configuração finalizada! Os logs do Cisco ASA e do Linux devem começar a ser ingeridos no Splunk.")
    else:
        print("\n⚠ Alguns Add-ons não foram instalados corretamente. Verifique os erros acima.")

if __name__ == "__main__":
    main()
