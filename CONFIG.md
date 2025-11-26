# Guia de Configuração

Este documento explica detalhadamente todas as opções disponíveis no arquivo `config.json`.

## 📄 Localização

O arquivo `config.json` deve estar localizado na **raiz do projeto**, no mesmo nível que as pastas `Scripts/` e `.github/`.

## 🏗️ Estrutura Completa

```json
{
  "horarios": {
    "entrada": {
      "horario_exato": "07:22",
      "janela_inicio": "07:10",
      "janela_limite": "07:23"
    },
    "saida": {
      "horario_exato": "17:10",
      "janela_inicio": "16:55",
      "janela_limite": "17:11"
    }
  },
  "sistema": {
    "timezone": "America/Sao_Paulo",
    "intervalo_verificacao_segundos": 30,
    "modo_headless": true
  }
}
```

> **Nota sobre e-mails:** As credenciais de e-mail (EMAIL_SENDER e EMAIL_PASSWORD) são configuradas via variáveis de ambiente, não no arquivo config.json. Veja o arquivo .env.example para mais detalhes.

## ⛙️ Opções de Configuração

### `horarios.entrada`

Configurações para o ponto de **entrada**.

#### `horario_exato` (string, obrigatório)
- **Formato:** `"HH:MM"` (24 horas)
- **Descrição:** Horário preciso em que o ponto de entrada será batido
- **Exemplo:** `"07:22"` (7h22 da manhã)

#### `janela_inicio` (string, obrigatório)
- **Formato:** `"HH:MM"` (24 horas)
- **Descrição:** Início da janela de verificação. O script só começará a verificar o horário após este momento
- **Exemplo:** `"07:10"` (7h10 da manhã)
- **Recomendação:** Configure 10-15 minutos antes do `horario_exato`

#### `janela_limite` (string, obrigatório)
- **Formato:** `"HH:MM"` (24 horas)
- **Descrição:** Fim da janela de verificação. Se o horário passar deste limite sem bater o ponto, o script irá abortar a tentativa
- **Exemplo:** `"07:23"` (7h23 da manhã)
- **Recomendação:** Configure 1-2 minutos após o `horario_exato`

### `horarios.saida`

Configurações para o ponto de **saída** (mesma estrutura de `horarios.entrada`).

#### `horario_exato` (string, obrigatório)
- **Exemplo:** `"17:10"` (5h10 da tarde)

#### `janela_inicio` (string, obrigatório)
- **Exemplo:** `"16:55"` (4h55 da tarde)

#### `janela_limite` (string, obrigatório)
- **Exemplo:** `"17:11"` (5h11 da tarde)

### `sistema`

Configurações gerais do sistema.

#### `timezone` (string, obrigatório)
- **Formato:** Timezone do banco de dados IANA
- **Descrição:** Fuso horário usado para todas as operações
- **Exemplo:** `"America/Sao_Paulo"` (horário de Brasília)
- **Outros valores comuns:**
  - `"America/Sao_Paulo"` - Brasília, São Paulo, Rio de Janeiro
  - `"America/Manaus"` - Manaus (UTC-4)
  - `"America/Fortaleza"` - Fortaleza (UTC-3, sem horário de verão)

#### `intervalo_verificacao_segundos` (número, obrigatório)
- **Formato:** Número inteiro positivo
- **Descrição:** Tempo em segundos que o script aguarda entre cada verificação de horário
- **Exemplo:** `30` (verifica a cada 30 segundos)
- **Recomendação:** 
  - `30` segundos é ideal para a maioria dos casos
  - Valores menores (10-15s) podem ser usados se precisar de mais precisão
  - Valores maiores (60s) podem ser usados para economizar recursos

#### `modo_headless` (boolean, obrigatório)
- **Formato:** `true` ou `false`
- **Descrição:** Define se o navegador Chrome será executado em modo invisível (sem interface gráfica)
- **Valores:**
  - `true` - Navegador invisível (recomendado para produção e GitHub Actions)
  - `false` - Navegador visível (útil para debug local)
- **Exemplo:** `true`

## 📝 Exemplos de Uso

### Exemplo 1: Horário comercial padrão

```json
{
  "horarios": {
    "entrada": {
      "horario_exato": "08:00",
      "janela_inicio": "07:50",
      "janela_limite": "08:02"
    },
    "saida": {
      "horario_exato": "17:00",
      "janela_inicio": "16:50",
      "janela_limite": "17:02"
    }
  },
  "sistema": {
    "timezone": "America/Sao_Paulo",
    "intervalo_verificacao_segundos": 30,
    "modo_headless": true
  }
}
```

### Exemplo 2: Turno alternativo

```json
{
  "horarios": {
    "entrada": {
      "horario_exato": "14:00",
      "janela_inicio": "13:50",
      "janela_limite": "14:02"
    },
    "saida": {
      "horario_exato": "22:00",
      "janela_inicio": "21:50",
      "janela_limite": "22:02"
    }
  },
  "sistema": {
    "timezone": "America/Sao_Paulo",
    "intervalo_verificacao_segundos": 30,
    "modo_headless": true
  }
}
```

### Exemplo 3: Debug local (navegador visível)

```json
{
  "horarios": {
    "entrada": {
      "horario_exato": "07:22",
      "janela_inicio": "07:10",
      "janela_limite": "07:23"
    },
    "saida": {
      "horario_exato": "17:10",
      "janela_inicio": "16:55",
      "janela_limite": "17:11"
    }
  },
  "sistema": {
    "timezone": "America/Sao_Paulo",
    "intervalo_verificacao_segundos": 10,
    "modo_headless": false
  }
}
```

## 🔄 Como Recarregar as Configurações

### GitHub Actions
As configurações são carregadas automaticamente a cada execução do workflow. Para atualizar:

1. Edite o arquivo `config.json` no repositório
2. Faça commit das alterações
3. Na próxima execução agendada, as novas configurações serão usadas

### Localmente
Para aplicar novas configurações:

1. Edite o arquivo `config.json`
2. Salve o arquivo
3. Execute o script novamente: `python Scripts/Main.py`

## ⚠️ Validações

O sistema valida automaticamente o arquivo `config.json` ao iniciar:

- ✅ Verifica se o arquivo existe
- ✅ Valida sintaxe JSON
- ✅ Confirma que todas as seções obrigatórias estão presentes
- ✅ Verifica formato dos horários (HH:MM)

Se houver erro de validação, o script será interrompido com uma mensagem clara do problema.

## 🚨 Erros Comuns

### Erro: "Arquivo de configuração não encontrado"
**Causa:** O arquivo `config.json` não existe na raiz do projeto.

**Solução:**
```bash
cp config.example.json config.json
```

### Erro: "Formato de horário inválido"
**Causa:** Horário não está no formato `HH:MM`.

**Exemplo errado:** `"7:22"`, `"07:22:00"`, `"07h22"`

**Exemplo correto:** `"07:22"`

### Erro: "Configuração obrigatória 'X' não encontrada"
**Causa:** Falta uma seção ou campo obrigatório no JSON.

**Solução:** Compare seu `config.json` com o `config.example.json` e adicione os campos faltantes.

## 💡 Dicas

1. **Mantenha uma cópia de backup**: Antes de fazer grandes alterações, faça uma cópia do `config.json`

2. **Teste localmente primeiro**: Antes de fazer commit de novas configurações, teste localmente para garantir que funciona

3. **Janelas realistas**: Configure janelas que dão tempo suficiente para o GitHub Actions iniciar (2-3 minutos antes do horário exato)

4. **Use comentários (com cuidado)**: JSON padrão não suporta comentários, mas você pode adicionar um campo `"_comentario"` que será ignorado:
   ```json
   {
     "_comentario": "Esta configuração é para o turno da manhã",
     "horarios": {
       ...
     }
   }
   ```

5. **Versionamento**: Faça commits descritivos ao alterar configurações:
   ```bash
   git commit -m "Ajusta horário de entrada para 08:00"
   ```

## 🔗 Relacionado

- [README.md](README.md) - Documentação principal
- [CRON_ONLINE_SETUP.md](CRON_ONLINE_SETUP.md) - Configuração do cron externo
- [config.example.json](config.example.json) - Arquivo de exemplo
