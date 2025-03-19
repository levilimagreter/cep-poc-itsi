import os
import subprocess

def install_splunk_addon():
    """Faz o download e instala o Splunk Add-on para Cisco ASA."""
    print("Baixando o Splunk Add-on para Cisco ASA...")
    addon_url = "https://splunkbase.splunk.com/app/1620/download"  # URL do Splunkbase
    download_cmd = f"wget --content-disposition --no-check-certificate {addon_url} -O Splunk_TA_cisco-asa.tgz"
    
    os.system(download_cmd)
    
    print("Extraindo o Add-on...")
    os.system("tar -xvzf Splunk_TA_cisco-asa.tgz -C /opt/splunk/etc/apps/")
    
    print("Reiniciando o Splunk para aplicar as mudanças...")
    os.system("/opt/splunk/bin/splunk restart")
    print("Instalação concluída!")

def configure_inputs():
    """Cria os inputs para ingestão dos logs Cisco ASA."""
    inputs_conf = "/opt/splunk/etc/apps/Splunk_TA_cisco-asa/local/inputs.conf"
    
    print("Configurando inputs para ingestão dos logs do Cisco ASA...")
    config_content = """[udp://514]
    connection_host = ip
    sourcetype = cisco:asa
    index = cisco_asa
    """
    
    os.makedirs(os.path.dirname(inputs_conf), exist_ok=True)
    with open(inputs_conf, "w") as f:
        f.write(config_content)
    
    print("Reiniciando o Splunk para aplicar a configuração...")
    os.system("/opt/splunk/bin/splunk restart")
    print("Configuração de inputs concluída!")

def main():
    install_splunk_addon()
    configure_inputs()
    print("Configuração finalizada! Os logs do Cisco ASA devem começar a ser ingeridos no Splunk.")

if __name__ == "__main__":
    main()
