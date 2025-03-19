# Guia para POC de ITSI - Splunk

## Visão Geral
Este repositório tem como objetivo fornecer um guia passo a passo para que parceiros Splunk possam aprender a configurar e demonstrar uma POC do IT Service Intelligence (ITSI). O foco é criar um ambiente funcional para monitoramento, correlação de eventos e detecção de anomalias.

## Estrutura do Projeto
O projeto está dividido nas seguintes fases:

### 1. Instalação do Splunk (Arquitetura S1)
#### Requisitos de Hardware e Software

Antes de iniciar a instalação do Splunk, é essencial garantir que o ambiente atenda aos requisitos mínimos de hardware e software conforme a documentação oficial do Splunk ITSI ([Referência](https://docs.splunk.com/Documentation/ITSI/4.20.0/Install/Plan)).

##### Hardware Recomendado:
| Componente      | Requisitos Mínimos |
|----------------|------------------|
| CPU           | 16 vCPUs          |
| Memória RAM   | 12 GB             |
| Armazenamento | 100 GB SSD        |
| Rede         | 1 Gbps Ethernet    |

##### Software Recomendado:
| Componente    | Versão Requerida |
|--------------|----------------|
| SO          | Linux (Ubuntu 20.04+, CentOS 7+, RHEL 8+) |
| Pacotes adicionais | `wget`, `curl`, `tar`, `unzip`, `firewalld` (se aplicável) |

##### Dependências de Rede:
Certifique-se de que as seguintes portas estão abertas:
| Serviço       | Porta |
|--------------|------|
| Web UI (HTTPS) | 8000 |
| Indexação | 9997 |
| Forwarding | 8089 |
| Deployment Server | 8089 |
| HEC | 8088 |
| KV Store | 8191 |

---

### 2. Instalação do ITSI e Licenciamento
#### Requisitos para POC do ITSI
Para realizar uma POC de ITSI, é necessário atender aos seguintes critérios:
- Uma **oportunidade aberta** na Splunk.
- A POC precisa ser aprovada como exequível pela equipe de vendas da Splunk.
- O licenciamento será disponibilizado **apenas após a aprovação** da POC.

#### Download e Instalação do ITSI
O ITSI pode ser baixado das seguintes formas:
- Diretamente pelo [Splunkbase](https://splunkbase.splunk.com/app/1841) (se houver uma licença válida para a conta Splunk associada).
- Mediante solicitação à equipe **Splunk Solutions Engineer (SE)** ou **Splunk Partner Solutions Engineer (PSE)**, caso a POC tenha sido aprovada.

#### Aplicação da Licença
Após receber a licença de ITSI:
1. Acesse o Splunk Web via navegador.
2. Faça login com as credenciais:
   - **Usuário**: `admin`
   - **Senha**: `splunkuser`
3. Navegue até **Settings > Licensing**.
4. Clique em **Add license** e faça o upload do arquivo `license.lic`.
5. Confirme a ativação da licença.

#### Configuração Inicial do ITSI
O ITSI **não pode ser instalado via Splunk Web**, ele deve ser extraído manualmente na pasta correta.

### **Passos para instalar o ITSI via CLI**

1️⃣ **Certifique-se de que o arquivo ITSI (`.spl`) está no diretório correto e sua permissão de execução**:
   ```bash
   ls -lha /home/splunkuser/splunk-it-service-intelligence_4200.spl
   ```
   Se o arquivo não estiver lá, faça o download conforme orientações anteriores. Para colocar permissão de execução:

   ```bash
   sudo chmod +x /home/splunkuser/splunk-it-service-intelligence_4200.spl
   ```

2️⃣ **Extraia o ITSI na pasta de aplicativos do Splunk**:
   ```bash
   sudo -u splunkuser tar -xvf /home/splunkuser/splunk-it-service-intelligence_4200.spl -C /opt/splunk/etc/apps/
   ```

3️⃣ **Corrija as permissões para o Splunk acessar corretamente**:
   ```bash
   sudo chown -R splunkuser:splunkuser /opt/splunk/etc/apps/itsi
   ```

4️⃣ **Reinicie o Splunk para aplicar a instalação**:
   ```bash
   sudo -u splunkuser /opt/splunk/bin/splunk restart
   ```

5️⃣ **Após a reinicialização, acesse o ITSI no Splunk Web**:
   - Navegue até **Apps > IT Service Intelligence** para concluir a configuração inicial.

##### Configuração Detalhada
1. **Configuração de Índices:**
   - Vá para **Settings > Indexes** e crie os seguintes índices se ainda não existirem:
     - `itsi_summary`
     - `itsi_tracked_alerts`
     - `itsi_notable_grouped_events`
   - Verifique se há espaço suficiente em disco para a retenção dos eventos.

2. **Definição de Permissões de Usuários:**
   - Acesse **Settings > Access Controls > Roles**.
   - Crie ou modifique os papéis para garantir que usuários relevantes tenham permissões para visualizar e gerenciar o ITSI.
   - Adicione os usuários corretos ao grupo, um novo usuario chamado `analyst` ao `itoa_admin` e outro chamado `user` associado ao `itoa_user`.
   - `Não` precisa marcar a opção "Require password change on next login".
   - Use a mesma senha para facilitar o laboratório.

3. **Inicialização do KV Store:**
   - Execute o seguinte comando para verificar o status do KV Store:
     ```bash
     sudo -u splunkuser /opt/splunk/bin/splunk show kvstore-status
     ```
   - Usuário admin e a mesma senha compatilhada anteriormente.
     
   - Se necessário, reinicie o KV Store:
     ```bash
     sudo -u splunkuser /opt/splunk/bin/splunk restart splunkd
     ```
---

### 3. Ingestão de Dados
Para esta POC, usaremos os seguintes data sources:
- **Cisco ASA**: Será disponibilizado um script em Python no GitHub para facilitar a instalação e configuração no ambiente.
- **Linux Host (próprio servidor do Splunk)**: Captura de métricas nativas do sistema operacional.

#### Configuração do Data Source Cisco ASA
O script Python será responsável por:
- Configurar o envio de logs do Cisco ASA para o Splunk via syslog.
- Criar os inputs necessários no Splunk automaticamente.
- Configurar parsing adequado dos eventos.

Os detalhes da execução estarão disponíveis no diretório `/scripts` deste repositório.

#### Configuração do Data Source Linux
1. No Splunk, vá até **Settings > Data Inputs**.
2. Selecione **Local Performance Monitoring** e adicione os seguintes inputs:
   - CPU
   - Memória
   - Disco
   - Processos ativos
3. Verifique os eventos no índice `_internal` para confirmar que os dados estão sendo coletados corretamente.

---

### 4. Criação de Árvores de Serviço
- Conceitos e estrutura das árvores de serviço no ITSI.
- Criação de um exemplo básico.
- Configuração de KPIs e thresholds.

### 5. Criação de Regra de Detecção de Anomalia
- Definição de um caso de uso baseado em logs de firewall.
- Implementação de uma regra de anomalia utilizando Machine Learning Toolkit (MLTK) ou ITSI Anomaly Detection.
- Testes e validação da regra.

## Requisitos
- Acesso a um ambiente Linux (Ubuntu/CentOS recomendado).
- Conta Splunk para download dos pacotes.
- Licença válida para o ITSI.

## Estrutura do Repositório
- `/scripts` - Scripts para instalação e configuração automatizada.
- `/datasets` - Arquivos de logs de firewall para testes.
- `/docs` - Documentação detalhada de cada etapa.
- `/configs` - Arquivos de configuração do Splunk e ITSI.

## Próximos Passos
1. Criar scripts de instalação do Splunk e ITSI.
2. Desenvolver o script Python para ingestão de logs do Cisco ASA.
3. Criar templates de árvores de serviço.
4. Implementar a regra de detecção de anomalias.

---
Esse guia será atualizado conforme o desenvolvimento do projeto. Contribuições são bem-vindas!

