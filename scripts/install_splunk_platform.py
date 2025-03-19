import os
import subprocess

def check_and_install_firewalld():
    """Verifica se o firewalld está instalado e o instala se necessário."""
    print("Verificando a presença do firewalld...")
    firewalld_check = subprocess.run(["rpm", "-q", "firewalld"], capture_output=True, text=True)
    
    if "is not installed" in firewalld_check.stdout:
        print("firewalld não encontrado. Instalando...")
        os.system("sudo yum install -y firewalld")
        os.system("sudo systemctl enable firewalld --now")
        print("firewalld instalado e ativado com sucesso!")
    else:
        print("firewalld já está instalado.")

def configure_firewall():
    """Configura o firewalld para abrir a porta 8000."""
    print("Configurando firewall...")
    os.system("sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent")
    os.system("sudo firewall-cmd --reload")
    print("Porta 8000 adicionada com sucesso!")

def create_splunk_user():
    """Cria o usuário Splunk e define senha padrão."""
    print("Criando usuário splunkuser...")
    os.system("sudo useradd -m -r splunkuser")
    os.system("echo 'splunkuser:splunkuser' | sudo chpasswd")
    os.system("sudo usermod -aG wheel splunkuser")
    print("Usuário splunkuser criado e adicionado ao grupo sudo.")

def download_splunk():
    """Baixa o Splunk Enterprise na versão especificada."""
    print("Baixando Splunk Enterprise...")
    os.system("sudo -u splunkuser wget -O /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz 'https://download.splunk.com/products/splunk/releases/9.4.1/linux/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz'")
    print("Download concluído.")

def set_permissions():
    """Define permissões no arquivo baixado."""
    print("Definindo permissões no arquivo de instalação do Splunk...")
    os.system("sudo chmod +x /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz")
    print("Permissões definidas.")

def prepare_installation():
    """Cria o diretório de instalação e ajusta permissões."""
    print("Criando diretório /opt/splunk e configurando permissões...")
    os.system("sudo mkdir -p /opt/splunk")
    os.system("sudo chown -R splunkuser:splunkuser /opt/splunk")
    print("Diretório /opt/splunk pronto.")

def install_splunk():
    """Extrai e instala o Splunk."""
    print("Extraindo e instalando Splunk...")
    os.system("sudo -u splunkuser tar -xzvf /home/splunkuser/splunk-9.4.1-e3bdab203ac8-linux-amd64.tgz -C /opt")
    print("Instalação concluída.")

def start_splunk():
    """Inicia o Splunk e configura inicialização no boot."""
    print("Iniciando Splunk...")
    os.system("sudo -u splunkuser /opt/splunk/bin/splunk start --accept-license --answer-yes --no-prompt")
    os.system("sudo /opt/splunk/bin/splunk enable boot-start -user splunkuser --accept-license --answer-yes --no-prompt")
    print("Splunk iniciado e configurado para iniciar no boot.")

def main():
    check_and_install_firewalld()
    configure_firewall()
    create_splunk_user()
    download_splunk()
    set_permissions()
    prepare_installation()
    install_splunk()
    start_splunk()
    print("Instalação do Splunk Enterprise concluída com sucesso!")

if __name__ == "__main__":
    main()

