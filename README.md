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

### 3. Estrutura da Árvore de Serviços
# **POC ITSI - Simulação de Serviços e KPIs**

## **Objetivo**
Este documento define a estrutura de uma **POC** para o **Splunk ITSI**, baseada em uma arquitetura de um **site monolítico** com serviços fictícios e KPIs simulados. O objetivo é fornecer um ambiente de testes prático para **parceiros SEs** aprenderem a configurar **serviços, KPIs e árvores de dependências** no ITSI sem necessidade de dados reais.

---

## **Estrutura da Árvore de Serviços**
A POC será baseada em uma aplicação monolítica, onde cada serviço representa um componente essencial do sistema:

### **Serviços e KPIs**
1. **Frontend Web**
   - **KPIs:**
     - CPU Usage
     - Memory Usage
     - HTTP Response Time
     - HTTP Errors (4xx, 5xx)
   - **Dependência:** Backend API

2. **Backend API**
   - **KPIs:**
     - CPU Usage
     - Memory Usage
     - Request Count
     - Error Rate
   - **Dependência:** Database & Authentication Service

3. **Database**
   - **KPIs:**
     - CPU Usage
     - Disk I/O
     - Query Response Time
     - Active Connections
   - **Dependência:** Storage

4. **Authentication Service**
   - **KPIs:**
     - CPU Usage
     - Failed Logins
     - Authentication Latency
   - **Dependência:** Database

5. **Storage**
   - **KPIs:**
     - Disk Usage
     - Read/Write Latency
     - Available Space
   - **Dependência:** Nenhuma (base da infraestrutura)

### **Hierarquia da Árvore de Serviços**
```
          Frontend Web
               |
         Backend API
          /       \
  Authentication   Database
         |           |
       Database    Storage
```
- O **Frontend Web** depende do **Backend API**.
- O **Backend API** depende do **Authentication Service** e do **Database**.
- O **Database** depende do **Storage**.
- O **Storage** é a base da infraestrutura.

---

# **POC ITSI - Simulação de Serviços e KPIs**

## **Objetivo**
Este documento define a estrutura de uma **POC** para o **Splunk ITSI**, baseada em uma arquitetura de um **site monolítico** com serviços fictícios e KPIs simulados. O objetivo é fornecer um ambiente de testes prático para **parceiros SEs** aprenderem a configurar **serviços, KPIs e árvores de dependências** no ITSI sem necessidade de dados reais.

---

## **Estrutura da Árvore de Serviços**
A POC será baseada em uma aplicação monolítica, onde cada serviço representa um componente essencial do sistema:

### **Serviços e KPIs**
1. **Frontend Web**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Backend API

2. **Backend API**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Database & Authentication Service

3. **Database**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Storage

4. **Authentication Service**
   - **KPIs:**
     - CPU Usage
     - Latência de Rede
   - **Dependência:** Database

5. **Storage**
   - **KPIs:**
     - Disk Usage
     - Read/Write Latency
     - Available Space
   - **Dependência:** Nenhuma (base da infraestrutura)
   - 
---

### **1. Criar os Serviços no ITSI (Sem Dependências)**
Os serviços devem ser criados **sem dependências inicialmente**. A vinculação será feita depois, dentro do **Service Analyzer**.

1. Acesse **ITSI > Configuration Assistant**.
2. Vá para **Service Configuration > Configure Services**.
3. Create Service > Create Service. Crie os serviços:

* Title: Storage | * Title: Authentication Service | * Title: Database | * Title: Backend API | * Title: Serviços e KPIs
* Manually add service content
  
KPIs

Para cada serviço acima. Vá na guia KPIs > New > Generic KPI
* Title: Storage CPU_Usage

Ad hoc Search
```
| makeresults count=100 
| streamstats count as time 
| eval CPU_Usage=round(random()%100,2)
```
Threshold Field: CPU_Usage

KPI Search Schedule: Every minute

Unit: %

Configure os **thresholds** para:
   Critical: 80
   Hight: 70
   Medium: 50
   Low: 40

Para cada serviço acima. Vá na guia KPIs > New > Generic KPI
* Title: Network Latency
  
Ad hoc Search
```
| makeresults count=100 
| streamstats count as time 
| eval Latency=round(random()%500,2)
```
Threshold Field: Latency

KPI Search Schedule: Every minute

Unit: ms

Configure os **thresholds** para:
   Critical: 50
   Hight: 40
   Medium: 30
   Low: 20

### ** Configurar a Árvore de Dependências no Service Analyzer**
A configuração das dependências pode ser feita na criação do serviço ou posteriormente. Neste caso vamos fazer posteriormente. Vamos visitar cada serviço criado e ir até a guia Service Dependencies e depois Add dependecies:

1. Acesse **ITSI > Configuration Assistant**.
2. Vá para **Service Configuration > Storage, Authentication Service, etc**.
3. Tab Service Dependecies > Para cada serviço faça esta lógica:

Selecionar "CPU Usage", Simulação de Latência de Rede e ServiceHealthScore:

   •	O Frontend Web depende do Backend API.
	•	O Backend API depende do Authentication Service e do Database.
	•	O Database depende do Storage.
	•	O Storage é a base da infraestrutura.

 Vamos até o Service Analyzer olhar como ficou as metricas.

 Agora clique no Tree View. 

 Tome alguns minutos para explorar as metricas e arvore de serviços.

