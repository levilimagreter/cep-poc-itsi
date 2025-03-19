# cep-poc-itsi

# Guia para POC de ITSI - Splunk

## Visão Geral
Este repositório tem como objetivo fornecer um guia passo a passo para que parceiros Splunk possam aprender a configurar e demonstrar uma POC do IT Service Intelligence (ITSI). O foco é criar um ambiente funcional para monitoramento, correlação de eventos e detecção de anomalias.

## Estrutura do Projeto
O projeto está dividido nas seguintes fases:

### 1. Instalação do Splunk (Arquitetura S1)
- Requisitos de hardware e software.
- Passo a passo para instalação do Splunk Enterprise em ambiente Linux.
- Configuração inicial e boas práticas.

### 2. Instalação do ITSI e Licenciamento
- Download e instalação do ITSI.
- Aplicação da licença.
- Configuração inicial do ITSI.

### 3. Ingestão de Dados
- Definição de um dataset de logs de firewall para ingestão.
- Configuração de inputs no Splunk para receber esses logs.
- Normalização dos dados conforme o CIM (Common Information Model).

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
2. Definir os logs de firewall a serem utilizados.
3. Desenvolver um template de árvore de serviço.
4. Implementar a regra de detecção de anomalias.

---
Esse guia será atualizado conforme o desenvolvimento do projeto. Contribuições são bem-vindas!
