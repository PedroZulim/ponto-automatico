# Configuração: GitHub Actions + Cron Online

## 🎯 Visão Geral

Este guia mostra como configurar um **serviço de cron online gratuito** (cron-job.org) para disparar o GitHub Actions e bater ponto automaticamente.

### Arquitetura

```
┌───────────────────────────────┐    ┌───────────────────────────────┐
│        Cron-Job.org           │──▶│        GitHub Actions         │
│        (07:20 e 17:00)        │    │      (workflow ponto.yml)     │
└───────────────────────────────┘    └───────────────────────────────┘
                                                    │
                                                    ▼
┌───────────────────────────────┐    ┌───────────────────────────────┐
│       Main.py aguarda         │◀──│        Ponto batido +         │
│         horário exato         │    │         E-mail enviado        │
└───────────────────────────────┘    └───────────────────────────────┘
```

### Por que usar cron externo?

- ✅ **Mais confiável** que o cron do GitHub Actions
- ✅ **100% gratuito**
- ✅ **Notificações** em caso de falha
- ✅ **Histórico** de execuções
- ✅ **Não precisa** de máquina ligada

---

## 📋 Passo a Passo

### 1️⃣ Criar Token do GitHub

1. Acesse: https://github.com/settings/tokens
2. Clique em **"Generate new token"** → **"Generate new token (classic)"**
3. Configure:
   - **Nome:** `Ponto Automatico Trigger`
   - **Expiration:** No expiration (ou 1 ano)
   - **Permissões:**
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
4. Clique em **"Generate token"**
5. **⚠️ COPIE O TOKEN** (formato: `ghp_xxxxxxxxxxxx`)

### 2️⃣ Criar Conta no Cron-Job.org

1. Acesse: https://cron-job.org
2. Clique em **"Sign up"** (gratuito)
3. Preencha seus dados
4. Confirme o e-mail

### 3️⃣ Configurar Cron de Entrada

Os horários do cron devem ser configurados para disparar **alguns minutos antes** do horário real de batida do ponto (configurado no `config.json`).

**Valores padrão no config.json:**
- Entrada: 07:22
- Saída: 17:10

**Recomendação:** Configure o cron para disparar 2 minutos antes.

1. No dashboard, clique em **"Create cronjob"**

2. **Aba: General**
   - **Title:** `Ponto - Entrada 07:20`
   - **Address (URL):**
     ```
     https://api.github.com/repos/SEU_USUARIO/ponto-automatico/actions/workflows/ponto.yml/dispatches
     ```
     ⚠️ Substitua `SEU_USUARIO` pelo seu usuário do GitHub

3. **Aba: Schedule**
   - **Hours:** `07`
   - **Minutes:** `20` (2 min antes de 07:22)
   - **Days:**
     - ✅ Monday (Segunda)
     - ✅ Tuesday (Terça)
     - ✅ Wednesday (Quarta)
     - ✅ Thursday (Quinta)
     - ✅ Friday (Sexta)
     - ❌ Saturday (Sábado)
     - ❌ Sunday (Domingo)
   - **Timezone:** `America/Sao_Paulo` (ou busque por "Brazil")

4. **Aba: Advanced** (clique em "Show advanced")
   - **Request method:** `POST`
   - **Request body:**
     ```json
     {"ref":"main"}
     ```
   - **Request headers:** (clique em "+ Add header" três vezes)
     
     **Header 1:**
     ```
     Header name: Authorization
     Header value: Bearer ghp_SEU_TOKEN_AQUI
     ```
     
     **Header 2:**
     ```
     Header name: Accept
     Header value: application/vnd.github+json
     ```

5. Clique em **"Create cronjob"**

### 4️⃣ Configurar Cron de Saída

Repita o **Passo 3**, alterando apenas:

- **Title:** `Ponto - Saída 17:08`
- **Schedule:**
  - **Hours:** `17`
  - **Minutes:** `08` (2 min antes de 17:10)

(Mantenha todos os outros campos iguais)

**💡 Dica:** Se você alterou os horários no `config.json`, ajuste os horários aqui para 2-3 minutos antes do `horario_exato` configurado.

### 5️⃣ Testar a Configuração

1. No dashboard do cron-job.org, localize um dos jobs
2. Clique nos **três pontinhos (⋮)** ao lado do job
3. Clique em **"Execute now"**
4. Observe a coluna **"Last execution"**:
   - ✅ **Success (204)** = Configurado corretamente!
   - ❌ **401** = Token inválido ou sem permissões
   - ❌ **404** = URL incorreta

5. Verifique no GitHub:
   - Acesse: https://github.com/SEU_USUARIO/ponto-automatico/actions
   - Deve aparecer uma nova execução do workflow

---

## 🔍 Verificação e Monitoramento

### Verificar Execuções no Cron-Job.org

1. Dashboard → Lista de jobs
2. Coluna **"Last execution"** mostra:
   - Status (Success/Failure)
   - Data/hora
   - Response code
3. Clique no status para ver detalhes completos

### Verificar Execuções no GitHub Actions

1. Repositório → **Actions**
2. Workflow **"Bater ponto automático"**
3. Lista de execuções com status
4. Clique em uma execução para ver logs detalhados

### E-mails de Notificação

Você receberá e-mails em duas situações:

1. **Cron-Job.org:** Se o disparo falhar
2. **GitHub Actions:** Após o ponto ser batido (resultado)

---

## ⏰ Horários e Funcionamento

### Cronograma Completo

Os horários são configurados no arquivo `config.json`

**Exemplo de fluxo:**

| Cron Dispara | GitHub Actions Inicia | Main.py Aguarda | Ponto Batido |
|--------------|----------------------|-----------------|--------------|
| 07:20 | ~07:20-07:22 | Até 07:22 | 07:22 exato |
| 17:08 | ~17:08-17:10 | Até 17:10 | 17:10 exato |

### Por que disparar antes?

- **Cron-Job.org:** dispara no horário exato (ex: 07:20)
- **GitHub Actions:** pode levar 1-3 minutos para iniciar
- **Main.py:** aguarda o `horario_exato` configurado dentro da janela (ex: 07:22)
- **Resultado:** ponto batido no horário desejado ✅

### Como ajustar os horários?

**Opção 1: Via GitHub Web Interface**
1. Acesse seu repositório no GitHub
2. Navegue até o arquivo `config.json`
3. Clique no ícone de lápis (editar)
4. Altere os valores de `horario_exato`, `janela_inicio` e `janela_limite`
5. Faça o commit das alterações

**Opção 2: Localmente**
1. Clone o repositório
2. Edite o arquivo `config.json`
3. Commit e push:
   ```bash
   git add config.json
   git commit -m "Ajusta horários de ponto"
   git push
   ```

**⚠️ Lembre-se:** Após alterar o `config.json`, ajuste também os horários de disparo no cron-job.org para alguns minutos antes do `horario_exato`.

---

## 🛠️ Solução de Problemas

### ❌ Erro 401 (Unauthorized)

**Causa:** Token inválido ou sem permissões

**Solução:**
1. Verifique se copiou o token completo (`ghp_...`)
2. Confirme que marcou as permissões `repo` e `workflow`
3. Gere um novo token se necessário
4. Atualize o header `Authorization` no cron-job.org

### ❌ Erro 404 (Not Found)

**Causa:** URL incorreta ou repositório/workflow não existe

**Solução:**
1. Verifique a URL:
   ```
   https://api.github.com/repos/SEU_USUARIO/ponto-automatico/actions/workflows/ponto.yml/dispatches
   ```
2. Confirme que:
   - Owner: Seu nome de usuário do GitHub
   - Repo: `ponto-automatico` (ou o nome do seu repositório)
   - Workflow: `ponto.yml`
3. Verifique se o arquivo `.github/workflows/ponto.yml` existe no repositório

### ❌ Cron dispara mas workflow não executa

**Causa:** Workflow sem `workflow_dispatch` ou desabilitado

**Solução:**
1. Verifique se o arquivo `ponto.yml` tem:
   ```yaml
   on:
     workflow_dispatch:
   ```
2. Vá em **Actions** → habilite workflows se necessário

### ❌ Workflow executa mas não bate ponto

**Causa:** Secrets não configuradas ou erro no script

**Solução:**
1. Verifique secrets: **Settings** → **Secrets and variables** → **Actions**
2. Confirme que existem:
   - `APDATA_USERNAME`
   - `APDATA_PASSWORD`
   - `EMAIL_SENDER` (opcional)
   - `EMAIL_PASSWORD` (opcional)
3. Veja os logs no GitHub Actions para detalhes do erro

### ⏰ Horário incorreto

**Causa:** Timezone errado no cron-job.org ou `config.json`

**Solução:**

**No cron-job.org:**
1. Edite o cronjob
2. Aba **Schedule**
3. **Timezone:** selecione `America/Sao_Paulo`
4. Salve

**No config.json:**
1. Verifique se a timezone está correta:
   ```json
   {
     "sistema": {
       "timezone": "America/Sao_Paulo"
     }
   }
   ```
2. Commit e push se fizer alterações

---

## 🔒 Segurança

### ⚠️ Importante: Proteção do Token

1. **NUNCA** compartilhe seu token
2. **NUNCA** commite o token no Git
3. **Use** apenas nos headers do cron-job.org
4. **Revogue** imediatamente se suspeitar de comprometimento
5. **Considere** expiração de 1 ano e renove periodicamente

### Token Comprometido?

1. Acesse: https://github.com/settings/tokens
2. Localize o token
3. Clique em **"Delete"**
4. Gere um novo token
5. Atualize no cron-job.org

### Permissões Mínimas

O token deve ter apenas:
- ✅ `repo` (para acessar repositório privado)
- ✅ `workflow` (para disparar workflows)

Não marque outras permissões desnecessárias.

---

## 📊 Custos

### Tudo 100% Gratuito

| Serviço | Plano | Custo |
|---------|-------|-------|
| **Cron-Job.org** | Free (ilimitado) | R$ 0 |
| **GitHub Actions** | 2000 min/mês | R$ 0 |
| **Gmail** | Notificações | R$ 0 |

**Total: R$ 0/mês** ✅

### Uso Estimado de GitHub Actions

- **Execuções:** 2x/dia × 22 dias úteis = 44 execuções/mês
- **Duração:** ~2-3 minutos por execução
- **Total:** ~88-132 minutos/mês
- **Limite Free:** 2000 minutos/mês
- **Sobra:** ~1800+ minutos

## 📚 Recursos Adicionais

### Documentação do Projeto

- **[CONFIG.md](CONFIG.md):** Documentação completa do arquivo `config.json`
- **[README.md](README.md):** Documentação principal do projeto

### Documentação Oficial

- **Cron-Job.org:** https://cron-job.org/en/documentation/
- **GitHub API:** https://docs.github.com/en/rest/actions/workflows
- **GitHub Actions:** https://docs.github.com/en/actions

### Ferramentas Úteis

- **Cron Expression Generator:** https://crontab.guru
- **GitHub Token Tester:**
  ```bash
  curl -H "Authorization: Bearer ghp_seu_token" https://api.github.com/user
  ```

---

**Pronto! Seu sistema de ponto automático está configurado.** 🎉

O cron-job.org irá disparar o GitHub Actions nos horários configurados, e você receberá e-mails com o resultado de cada batida de ponto.
