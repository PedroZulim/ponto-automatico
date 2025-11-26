# Ponto Automático 🕐

Sistema automatizado para registro de ponto de entrada e saída usando GitHub Actions.

> **✅ Sim, funciona em repositórios privados!** Para mais informações sobre como usar GitHub Actions em repositórios privados, veja este guia detalhado.

## 📋 Descrição

Este projeto automatiza o registro de ponto (entrada e saída) utilizando GitHub Actions, executando em horários específicos durante dias úteis. O sistema:

- ✅ Executa automaticamente em dias úteis (segunda a sexta)
- ✅ Verifica feriados nacionais brasileiros
- ✅ Registra ponto em horários configurados
- ✅ Envia notificações por e-mail sobre o status
- ✅ **Funciona em repositórios privados**

## 🚀 Modos de Operação

Este projeto pode ser configurado utilizando:

### Cron Externo + GitHub Actions (Recomendado)
Usa um serviço de cron online gratuito (cron-job.org) para disparar o GitHub Actions.

**Prós:** Mais confiável, notificações, histórico  
**Contras:** Requer configuração externa

📖 **[Guia completo de configuração com cron externo →](CRON_ONLINE_SETUP.md)**  
📖 **[Documentação completa do arquivo de configuração →](CONFIG.md)**

---

## 🚀 Como usar em seu repositório privado

### Pré-requisitos

1. Um repositório privado no GitHub (sim, GitHub Actions funciona em repositórios privados!)
2. Credenciais do sistema APDATA
3. (Opcional) Conta de e-mail Gmail para notificações
4. Conta no cron-job.org para scheduler externo utilziando API do GitHub Actions

### Configuração Passo a Passo

#### 1. Configure os Secrets no GitHub

Para que a action funcione no seu repositório privado, você precisa configurar as seguintes secrets:

1. Acesse seu repositório no GitHub
2. Vá em **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. Adicione os seguintes secrets:

**Obrigatórios:**
- `APDATA_USERNAME`: Seu usuário do sistema APDATA
- `APDATA_PASSWORD`: Sua senha do sistema APDATA

**Opcionais (para notificações por e-mail):**
- `EMAIL_SENDER`: Seu e-mail Gmail
- `EMAIL_PASSWORD`: Senha de aplicativo do Gmail (veja instruções abaixo)

#### 2. Como obter a senha de aplicativo do Gmail

1. Acesse sua conta Google
2. Vá em **Segurança**
3. Ative a **verificação em duas etapas** (se ainda não estiver ativa)
4. Procure por **Senhas de app**
5. Crie uma nova senha de app para "Mail"
6. Use essa senha no secret `EMAIL_PASSWORD`

#### 3. Siga o guia de operação do scheduler externo

- Siga o guia completo: **[CRON_ONLINE_SETUP.md](CRON_ONLINE_SETUP.md)**
- Configure cron-job.org para disparar às 07:20 e 17:08
- Workflow `ponto.yml` já está configurado com `workflow_dispatch`

#### 4. Configure os horários de batida

Este projeto utiliza um arquivo de configuração centralizado para facilitar ajustes.

**Passo 1: Copie o arquivo de exemplo**
```bash
cp config.example.json config.json
```

**Passo 2: Edite o arquivo `config.json`** para ajustar os horários:

```json
{
  "horarios": {
    "entrada": {
      "horario_exato": "08:00",
      "janela_inicio": "07:58",
      "janela_limite": "08:01"
    },
    "saida": {
      "horario_exato": "17:48",
      "janela_inicio": "17:46",
      "janela_limite": "17:49"
    }
  },
  "sistema": {
    "timezone": "America/Sao_Paulo",
    "intervalo_verificacao_segundos": 30,
    "modo_headless": true
  }
}
```

**Parâmetros principais:**

- `horario_exato`: Horário preciso em que o ponto será batido (formato HH:MM)
- `janela_inicio`: Início da janela de verificação (o script só tentará bater ponto após este horário)
- `janela_limite`: Fim da janela de verificação (se passar deste horário, o ponto não será batido)
- `intervalo_verificacao_segundos`: Tempo de espera entre verificações de horário
- `modo_headless`: Se `true`, o navegador roda invisível (sem abrir janela)

> ⚠️ **Importante 1**: O GitHub Actions deve ser agendado para disparar alguns minutos ANTES do `horario_exato` para dar tempo do workflow iniciar e aguardar o horário correto.

> ⚠️ **Importante 2**: O GitHub Actions não consegue rodar o navegador se não estiver no `modo_headless`, matenha sempre `true`.

#### 5. Habilite o GitHub Actions

1. Vá em **Actions** no seu repositório
2. Se necessário, clique em **I understand my workflows, go ahead and enable them**
3. O workflow está configurado

#### 6. Teste manualmente (opcional)

1. Vá em **Actions** no seu repositório
2. Selecione o workflow **"Bater ponto automático"**
3. Clique em **Run workflow**
4. Selecione a branch `main` (ou sua branch principal)
5. Clique em **Run workflow**

## 📊 Uso no GitHub Actions (Repositórios Privados)

### Limites de uso

- **Repositórios públicos**: Minutos ilimitados e gratuitos
- **Repositórios privados**: 
  - Plano Free: 2.000 minutos/mês
  - Plano Pro: 3.000 minutos/mês
  - Plano Team: 10.000 minutos/mês

Este workflow consome aproximadamente **2-3 minutos por execução**. Com 2 execuções por dia útil (~22 dias/mês), você usará aproximadamente **88-132 minutos/mês**, bem dentro do limite gratuito.

### Verificar uso

1. Acesse **Settings** → **Billing and plans**
2. Veja o uso de **Actions & Packages**

## 🔒 Segurança

- ✅ Todas as credenciais são armazenadas como **GitHub Secrets** (criptografadas)
- ✅ As secrets nunca aparecem nos logs
- ✅ O código roda em ambiente isolado do GitHub
- ✅ O navegador Chrome roda em modo headless (sem interface gráfica)

## 📁 Estrutura do Projeto

```
.
├── .github/
│   └── workflows/
│       └── ponto.yml          # Configuração do GitHub Actions
├── Scripts/
│   ├── Main.py                # Script principal
│   ├── Ponto.py               # Lógica de registro de ponto
│   ├── Feriados.py            # Verificação de feriados
│   ├── Send_email.py          # Envio de notificações
│   └── Config.py              # Gerenciador de configurações
├── config.json                # Arquivo de configuração (horários, etc)
├── config.example.json        # Exemplo de arquivo de configuração
├── .env.example               # Exemplo de variáveis de ambiente
├── requirements.txt           # Dependências Python
├── README.md                  # Este arquivo
├── CONFIG.md                  # Documentação detalhada de configuração
└── CRON_ONLINE_SETUP.md       # Guia de configuração com cron externo
```

## 🛠️ Desenvolvimento Local

Se quiser testar localmente antes de usar no GitHub Actions:

1. Clone o repositório
2. Copie `config.example.json` para `config.json` e ajuste os horários:
   ```bash
   cp config.example.json config.json
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o script:
   ```bash
   python Scripts/Main.py
   ```

### Testando com horários diferentes

Para testar o sistema, você pode:

1. Editar `config.json` com um horário próximo (ex: 2 minutos no futuro)
2. Ajustar as janelas para cobrir esse horário
3. Executar `python Scripts/Main.py`
4. O script aguardará até o horário exato e tentará bater o ponto

## ❓ FAQ

### O GitHub Actions funciona em repositórios privados?
**Sim!** GitHub Actions funciona perfeitamente em repositórios privados, com algumas limitações de minutos dependendo do seu plano.

### Preciso pagar para usar GitHub Actions?
Para uso básico como este (2-3 minutos por execução, 2x ao dia), o plano **gratuito** é suficiente.

### Como vejo os logs de execução?
1. Vá em **Actions** no seu repositório
2. Clique em uma execução específica
3. Clique no job "run-ponto"
4. Veja os logs detalhados de cada step

### E se der erro?
Se você configurou o e-mail, receberá uma notificação. Você também pode verificar os logs na aba Actions do GitHub.

### Posso ajustar os horários?
Sim! Basta editar o arquivo `config.json` na raiz do projeto. Você pode alterar os horários de entrada e saída sem precisar modificar o código Python.

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📚 Documentação Adicional

- **[CONFIG.md](CONFIG.md)** - Documentação completa do arquivo `config.json` com exemplos e explicações detalhadas de cada parâmetro
- **[CRON_ONLINE_SETUP.md](CRON_ONLINE_SETUP.md)** - Guia passo a passo para configurar o disparo automático usando cron-job.org

## 🆕 Novidades da Versão Atual

### Sistema de Configuração Centralizado

A partir desta versão, todos os horários e configurações foram movidos para o arquivo `config.json`:

- ✅ **Horários configuráveis**: Altere entrada/saída sem mexer no código Python
- ✅ **Janelas de verificação**: Configure quando o sistema deve tentar bater ponto
- ✅ **Validação automática**: O sistema valida o JSON e os horários ao iniciar
- ✅ **Fácil manutenção**: Um único arquivo para todas as configurações

**Para usuários de versões antigas:**
1. Copie `config.example.json` para `config.json`
2. Ajuste os horários conforme necessário
3. Commit e push das alterações

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Nota**: Este projeto é para uso pessoal. Certifique-se de estar em conformidade com as políticas da sua empresa ao usar automação para registro de ponto.
