# Ponto Automático 🕐

Sistema automatizado para registro de ponto de entrada e saída usando GitHub Actions.

> **✅ Sim, funciona em repositórios privados!** Para mais informações sobre como usar GitHub Actions em repositórios privados, veja [este guia detalhado](GITHUB_ACTIONS_PRIVATE_REPO.md).

## 📋 Descrição

Este projeto automatiza o registro de ponto (entrada e saída) utilizando GitHub Actions, executando em horários específicos durante dias úteis. O sistema:

- ✅ Executa automaticamente em dias úteis (segunda a sexta)
- ✅ Verifica feriados nacionais brasileiros
- ✅ Registra ponto em horários configurados
- ✅ Envia notificações por e-mail sobre o status
- ✅ **Funciona em repositórios privados**

## 🚀 Como usar em seu repositório privado

### Pré-requisitos

1. Um repositório privado no GitHub (sim, GitHub Actions funciona em repositórios privados!)
2. Credenciais do sistema APDATA
3. (Opcional) Conta de e-mail Gmail para notificações

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

#### 3. Ajuste os horários (opcional)

Os horários estão configurados em dois arquivos:

**`.github/workflows/ponto.yml`** - Horários de execução do workflow:
```yaml
schedule:
  - cron: "0 10 * * 1-5"  # 10:00 UTC = 07:00 BRT (inicia antes da entrada)
  - cron: "55 19 * * 1-5" # 19:55 UTC = 16:55 BRT (inicia antes da saída)
```
> O workflow inicia alguns minutos antes do horário de batida para dar tempo ao script aguardar o momento exato.

**`Scripts/Main.py`** - Horários exatos de entrada e saída:
```python
TARGET_ENTRADA = "07:22"  # Horário desejado de entrada
TARGET_SAIDA = "17:10"    # Horário desejado de saída
```
> O script aguarda até atingir estes horários exatos para bater o ponto, mesmo que o workflow tenha iniciado antes.

#### 4. Habilite o GitHub Actions

1. Vá em **Actions** no seu repositório
2. Se necessário, clique em **I understand my workflows, go ahead and enable them**
3. O workflow está configurado para executar automaticamente

#### 5. Teste manualmente (opcional)

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
│   └── Send_email.py          # Envio de notificações
├── .env.example               # Exemplo de variáveis de ambiente
├── requirements.txt           # Dependências Python
└── README.md                  # Este arquivo
```

## 🛠️ Desenvolvimento Local

Se quiser testar localmente antes de usar no GitHub Actions:

1. Clone o repositório
2. Copie `.env.example` para `.env`
3. Preencha suas credenciais no arquivo `.env`
4. Instale as dependências:
```bash
pip install -r requirements.txt
```
5. Execute o script:
```bash
python Scripts/Main.py
```

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
Sim! Edite os arquivos mencionados na seção "Ajuste os horários".

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Nota**: Este projeto é para uso pessoal. Certifique-se de estar em conformidade com as políticas da sua empresa ao usar automação para registro de ponto.
