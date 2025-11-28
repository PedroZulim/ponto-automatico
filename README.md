# Sistema Automatizado de Ponto Eletrônico

## Visão Geral
Este é um sistema Python desenvolvido para automatizar o processo de batida de ponto eletrônico no sistema APDATA (cliente.apdata.com.br/dicon/). O sistema monitora continuamente o horário e bate ponto automaticamente nos horários configurados, respeitando dias úteis e feriados.

## Arquitetura do Sistema

### 📁 Estrutura de Arquivos
```
ponto-automatico/
├── config.json              # Configurações personalizadas do usuário
├── config.example.json      # Template de configuração
├── requirements.txt         # Dependências Python
├── LICENSE                  # Licença MIT
└── Scripts/
    ├── Main.py              # Orchestrador principal
    ├── Config.py            # Gerenciador de configurações
    ├── Feriados.py          # Controle de feriados nacionais/municipais
    ├── Ponto.py             # Bot de automação web
    └── Send_email.py        # Sistema de notificações por e-mail
```

## 🔧 Componentes do Sistema

### 1. Main.py - Orchestrador Principal
**Responsabilidade**: Coordena todo o fluxo de execução do sistema.

**Funcionalidades**:
- Loop principal de monitoramento contínuo
- Validação de dias úteis e feriados
- Controle de janelas de tempo para entrada e saída
- Detecção de horários exatos configurados
- Coordenação entre todos os módulos

**Lógica de Funcionamento**:
1. Carrega configurações e inicializa componentes
2. Valida se é um dia útil (não feriado/fim de semana)
3. Loop contínuo verificando horário atual a cada 30 segundos
4. Identifica se está dentro das janelas de entrada ou saída
5. Dispara automação quando atinge horário exato configurado
6. Envia notificação do resultado por e-mail

### 2. Config.py - Gerenciador de Configurações
**Responsabilidade**: Centraliza o carregamento e validação de todas as configurações.

**Funcionalidades**:
- Carrega arquivo `config.json` com validação completa
- Converte strings de horário para objetos `time`
- Propriedades type-safe para todos os parâmetros
- Validação automática de estrutura e formatos
- Suporte a recarga dinâmica de configurações

**Configurações Gerenciadas**:
- Horários exatos de entrada/saída
- Janelas de tempo permitidas
- Timezone do sistema
- Intervalo de verificação
- Modo headless do navegador

### 3. Feriados.py - Controle de Feriados
**Responsabilidade**: Determina se o dia atual é válido para batida de ponto.

**Funcionalidades**:
- **Feriados Nacionais**: Integração com API BrasilAPI para feriados oficiais
- **Feriados Municipais**: Leitura de planilha Google Sheets configurável
- Cache inteligente para evitar múltiplas consultas
- Suporte a múltiplos formatos de data
- Validação combinada de fins de semana + feriados

**Integrações**:
- API: `https://brasilapi.com.br/api/feriados/v1/{ano}`
- Google Sheets: CSV público exportado
- Timezone: Cálculo correto do "hoje" por região

### 4. Ponto.py - Bot de Automação Web
**Responsabilidade**: Executa a automação do processo de batida de ponto.

**Tecnologia**: Playwright (mais robusto que Selenium)

**Funcionalidades**:
- Navegação automatizada para sistema APDATA
- Tratamento de cookies e timeouts
- Preenchimento automático de credenciais
- Captura de confirmação do sistema
- Modo headless configurável para servidores

**Fluxo de Automação**:
1. Abre navegador Chromium com configurações otimizadas
2. Acessa página de ponto do cliente APDATA
3. Aceita cookies automaticamente
4. Aguarda carregamento completo dos campos
5. Preenche usuário e senha das variáveis de ambiente
6. Clica no botão de bater ponto
7. Captura mensagem de confirmação do sistema
8. Fecha navegador e retorna resultado

### 5. Send_email.py - Sistema de Notificações
**Responsabilidade**: Envia relatórios por e-mail sobre execuções do sistema.

**Funcionalidades**:
- SMTP configurável (padrão: Gmail)
- Autenticação segura via variáveis de ambiente
- Templates de e-mail por tipo de status
- Tratamento de erros sem quebrar execução principal
- Modo degradado quando credenciais não disponíveis

**Tipos de Notificação**:
- **Sucesso**: Ponto batido com confirmação do sistema
- **Erro**: Falhas técnicas ou timeout
- **Ignorado**: Feriados, fins de semana, fora de horário

## ⚙️ Configuração do Sistema

### config.json
```json
{
  "horarios": {
    "entrada": {
      "horario_exato": "07:22",      // Horário preciso para entrada
      "janela_inicio": "07:10",      // Início da janela permitida
      "janela_limite": "07:23"       // Fim da janela permitida
    },
    "saida": {
      "horario_exato": "17:10",      // Horário preciso para saída
      "janela_inicio": "16:55",      // Início da janela permitida
      "janela_limite": "17:11"       // Fim da janela permitida
    }
  },
  "sistema": {
    "timezone": "America/Sao_Paulo",           // Timezone brasileiro
    "intervalo_verificacao_segundos": 30,     // Frequência de verificação
    "modo_headless": true                     // Navegador invisível
  }
}
```

### Variáveis de Ambiente (.env)
```bash
# Credenciais do sistema APDATA
APDATA_USERNAME=seu_usuario
APDATA_PASSWORD=sua_senha

# Credenciais de e-mail (opcional)
EMAIL_SENDER=seu_email@gmail.com
EMAIL_PASSWORD=sua_senha_app
```

## 🚀 Dependências e Tecnologias

### Bibliotecas Python
- **pandas**: Processamento de dados de feriados
- **requests**: Consulta à API de feriados nacionais
- **python-dotenv**: Carregamento seguro de credenciais
- **playwright**: Automação web moderna e robusta
- **webdriver-manager**: Gerenciamento automático de drivers

### APIs e Integrações
- **BrasilAPI**: Feriados nacionais/estaduais oficiais
- **Google Sheets**: Feriados municipais personalizáveis
- **APDATA**: Sistema de ponto eletrônico target
- **Cron-job.org**: Agendamento automático via API HTTP

## 📅 Sistema de Agendamento

### Integração com cron-job.org
O sistema utiliza a plataforma [cron-job.org](https://cron-job.org/) para agendamento automatizado, eliminando a necessidade de manter um servidor rodando continuamente.

**Funcionalidades do Agendamento**:
- **Triggers HTTP**: Dispara execução via chamada de API
- **Horários Precisos**: Configuração exata para horários de entrada e saída
- **Monitoramento Web**: Interface visual para acompanhar execuções
- **Logs Centralizados**: Histórico completo de execuções na plataforma
- **Alertas**: Notificações quando jobs falham ou não executam

**Configuração Típica**:
```
# Entrada: 07:20 (2 minutos antes do horário exato)
20 7 * * 1-5

# Saída: 17:08 (2 minutos antes do horário exato)  
8 17 * * 1-5
```

**Vantagens desta Abordagem**:
- ✅ Sem necessidade de servidor 24/7
- ✅ Alta confiabilidade da plataforma
- ✅ Monitoramento visual simples
- ✅ Logs e alertas automáticos
- ✅ Configuração via interface web
- ✅ Backup automático de configurações

## 🔄 Fluxo de Execução

### Inicialização
1. Carrega configurações do `config.json`
2. Inicializa gerenciadores de feriados e e-mail
3. Configura bot de automação web

### Loop Principal
1. **Verificação de Data**: Valida se é dia útil e não é feriado
2. **Monitoramento de Horário**: Verifica horário atual contra configurações
3. **Controle de Janelas**: 
   - Se antes da janela de entrada → aguarda
   - Se perdeu janela de entrada → notifica erro e encerra
   - Se passou de todas as janelas → encerra
4. **Detecção de Horário Exato**: Compara com horários configurados
5. **Execução**: Dispara automação quando horário exato é atingido
6. **Notificação**: Envia resultado por e-mail

### Estados Possíveis
- **Aguardando**: Dentro do horário válido, mas não é o momento exato
- **Executando**: Automação em andamento
- **Sucesso**: Ponto batido com confirmação
- **Ignorado**: Feriado, fim de semana ou fora de horário válido
- **Erro**: Falha técnica ou timeout

## 🎯 Características Técnicas

### Robustez
- Tratamento abrangente de exceções
- Timeouts configuráveis para evitar travamentos
- Validação completa de dados de entrada
- Logs detalhados para depuração

### Segurança
- Credenciais em variáveis de ambiente (nunca no código)
- Validação de certificados SSL
- Headers de segurança no navegador
- Dados sensíveis nunca logados

### Confiabilidade
- Cache de feriados para evitar falhas de rede
- Múltiplas tentativas com timeouts graduais
- Modo degradado quando serviços externos falham
- Notificações sempre enviadas (sucesso ou falha)

### Flexibilidade
- Configurações completamente externalizadas
- Suporte a feriados municipais personalizáveis
- Timezone configurável para diferentes regiões
- Modo headless para execução em servidores
- Agendamento externo via cron-job.org (sem necessidade de servidor próprio)

## 💡 Casos de Uso

### Execução Local
- Desenvolvimento e testes em máquina pessoal
- Debug com navegador visível
- Configuração rápida via arquivo local

### Execução em Servidor
- Deploy automatizado via GitHub Actions
- Modo headless para economia de recursos
- Notificações por e-mail para monitoramento

### Agendamento Automático
- **Scheduler Online**: Utiliza [cron-job.org](https://cron-job.org/) para agendamento
- **Trigger por API**: Dispara workflow via chamada HTTP automatizada
- **Execução Pontual**: Sistema roda exatamente nos horários necessários
- **Monitoramento Remoto**: Controle e logs através da plataforma online

### Ambientes Corporativos
- Feriados municipais específicos via planilha
- Múltiplos usuários com configurações individuais
- Logs centralizados para auditoria

## 🏆 Pontos Fortes da Implementação

1. **Modularidade**: Cada classe tem responsabilidade única e bem definida
2. **Type Hints**: Código totalmente tipado para melhor manutenibilidade
3. **Configurabilidade**: Todas as configurações são externas e validadas
4. **Tolerância a Falhas**: Sistema continua funcionando mesmo com falhas parciais
5. **Observabilidade**: Logs detalhados e notificações automáticas
6. **Padrões Modernos**: Uso de tecnologias atuais (Playwright, zoneinfo, etc.)
7. **Arquitetura Serverless**: Agendamento via cron-job.org elimina necessidade de infraestrutura própria

Este sistema representa uma solução completa e profissional para automação de ponto eletrônico, combinando robustez técnica com facilidade de uso, manutenção e deploy totalmente automatizado via agendamento externo.