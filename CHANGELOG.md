# Resumo de Mudanças - Sistema de Configuração Centralizado

## 📋 O que mudou?

O projeto foi reestruturado para usar um **arquivo de configuração centralizado** (`config.json`), facilitando a personalização dos horários de entrada e saída sem necessidade de alterar o código Python.

## 🆕 Novos Arquivos

### 1. `config.json`
Arquivo de configuração principal contendo todos os horários e parâmetros do sistema.

**Conteúdo:**
- Horários de entrada (exato, janela início, janela limite)
- Horários de saída (exato, janela início, janela limite)
- Configurações do sistema (timezone, intervalo de verificação, modo headless)
- Configurações SMTP para envio de e-mails

### 2. `config.example.json`
Arquivo de exemplo para facilitar a configuração inicial.

**Como usar:**
```bash
cp config.example.json config.json
# Edite config.json com seus horários
```

### 3. `Scripts/Config.py`
Módulo Python responsável por:
- Carregar o arquivo `config.json`
- Validar a estrutura e formato dos dados
- Fornecer uma API para acesso às configurações
- Converter strings de horário em objetos `time` do Python

### 4. `CONFIG.md`
Documentação completa do arquivo de configuração com:
- Explicação detalhada de cada parâmetro
- Exemplos de uso para diferentes cenários
- Guia de solução de problemas
- Dicas e boas práticas

### 5. `CHANGELOG.md` (este arquivo)
Resumo de todas as alterações realizadas.

## 🔄 Arquivos Modificados

### 1. `Scripts/Main.py`
**Antes:**
- Horários hardcoded como constantes no topo do arquivo
- Timezone hardcoded em múltiplos lugares

**Depois:**
- Carrega configurações do `config.json` via `Config.py`
- Todas as funções recebem o objeto `config` como parâmetro
- Código mais limpo e manutenível

**Principais mudanças:**
```python
# ANTES
TARGET_ENTRADA = "07:22"
ENTRADA_INICIO = time(7, 10)
# ...

# DEPOIS
config = Config()
config.entrada_horario_exato  # "07:22"
config.entrada_janela_inicio  # time(7, 10)
```

### 2. `Scripts/Ponto.py`
**Mudanças:**
- Adicionado parâmetro `timezone` no construtor
- Usa timezone configurável em vez de hardcoded
- Mantém compatibilidade com código existente

### 3. `Scripts/Feriados.py`
**Mudanças:**
- Adicionado parâmetro `timezone` no construtor
- Usa timezone configurável para verificar feriados
- Mantém compatibilidade com código existente

### 4. `Scripts/Send_email.py`
**Mudanças:**
- Parâmetros SMTP agora podem ser passados no construtor
- Mantém valores padrão para compatibilidade

### 5. `Testes/MainV2.py`
**Mudanças:**
- Atualizado para usar o novo sistema de configuração
- Adiciona path do diretório Scripts para importar módulos corretamente

### 6. `README.md`
**Adições:**
- Seção sobre o arquivo de configuração
- Instruções de como copiar e editar `config.json`
- Explicação dos parâmetros principais
- Link para `CONFIG.md` com documentação completa
- Seção "Novidades da Versão Atual"
- Instruções para desenvolvimento local
- Atualização da estrutura de arquivos

### 7. `CRON_ONLINE_SETUP.md`
**Adições:**
- Seção sobre como os horários são configurados no `config.json`
- Instruções de como ajustar horários (via GitHub web ou localmente)
- Nota sobre sincronização entre `config.json` e horários do cron
- Link para `CONFIG.md`
- Solução de problemas relacionada ao timezone no config

### 8. `.gitignore`
**Mudanças:**
- Comentários explicativos sobre o `config.json`
- Opção para não versionar `config.json` (comentada por padrão)
- Nota sobre configuração ao fazer fork do projeto

## ✅ Benefícios

### Para Usuários
1. **Mais fácil de configurar**: Apenas edite um arquivo JSON, sem mexer no código Python
2. **Menos erros**: Validação automática dos horários e configurações
3. **Mais flexível**: Altere timezone, intervalos de verificação, etc. facilmente
4. **Documentação clara**: `CONFIG.md` explica cada parâmetro em detalhes

### Para Desenvolvedores
1. **Código mais limpo**: Sem constantes hardcoded espalhadas pelo código
2. **Mais testável**: Fácil criar diferentes configurações para testes
3. **Mais manutenível**: Mudanças de configuração não exigem alteração de código
4. **Melhor separação de responsabilidades**: Configuração separada da lógica

## 🔧 Como Atualizar de Versões Antigas

Se você já estava usando este projeto:

### Passo 1: Backup
```bash
# Faça backup dos arquivos que você modificou
cp Scripts/Main.py Scripts/Main.py.backup
```

### Passo 2: Atualize o código
```bash
git pull origin main
```

### Passo 3: Crie o arquivo de configuração
```bash
cp config.example.json config.json
```

### Passo 4: Configure seus horários
Edite `config.json` e coloque os horários que você usava anteriormente no `Main.py`:

**Se no Main.py você tinha:**
```python
TARGET_ENTRADA = "07:22"
TARGET_SAIDA = "17:10"
ENTRADA_INICIO = time(7, 10)
ENTRADA_LIMITE = time(7, 23)
SAIDA_INICIO = time(16, 55)
SAIDA_LIMITE = time(17, 11)
```

**No config.json, coloque:**
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
  }
}
```

### Passo 5: Teste localmente
```bash
python Scripts/Main.py
```

### Passo 6: Commit e push
```bash
git add config.json
git commit -m "Configura horários personalizados"
git push
```

## 🧪 Testando

Para testar o novo sistema:

```bash
# 1. Configure um horário de teste (ex: 2 minutos no futuro)
# Edite config.json e coloque o horário desejado

# 2. Execute o script
python Scripts/Main.py

# 3. Observe os logs
# O script deve aguardar até o horário exato e tentar bater ponto
```

## 📝 Notas Importantes

### Sobre o config.json no Git

Por padrão, o `config.json` **É versionado** no Git. Isso é necessário para que o GitHub Actions funcione corretamente.

**Opções:**

1. **Versionar o config.json (recomendado para uso pessoal)**
   - Seus horários ficam salvos no repositório
   - Funciona automaticamente no GitHub Actions
   - ⚠️ Não use em repositórios públicos com dados sensíveis

2. **Não versionar o config.json**
   - Adicione `config.json` no `.gitignore`
   - Configure o arquivo via GitHub web interface após cada clone/fork
   - Mais seguro para repositórios públicos

### Compatibilidade

- ✅ **Python 3.10+**: Totalmente compatível
- ✅ **Python 3.9**: Compatível (mas pode ter avisos sobre type hints)
- ❌ **Python 3.8 ou inferior**: Não compatível (usa syntax `str | None`)

### Dependências

Nenhuma nova dependência foi adicionada. O projeto continua usando:
- `selenium`
- `python-dotenv`
- `pandas`
- `requests`

## 🐛 Problemas Conhecidos

### Import warning no Testes/MainV2.py

O Pylance pode mostrar um aviso sobre `from Config import Config` não poder ser resolvido. Isso é apenas um warning do linter - o código funciona corretamente em runtime pois o `sys.path` é ajustado antes do import.

**Não afeta a execução.**

## 🚀 Próximos Passos Sugeridos

Para futuras melhorias, considere:

1. **Suporte a múltiplos perfis**: Permitir diferentes configurações para diferentes dias (ex: sexta-feira com horário diferente)

2. **Configuração via variáveis de ambiente**: Sobrescrever valores do config.json com env vars para maior flexibilidade no GitHub Actions

3. **Interface web de configuração**: Criar uma página simples para editar configurações sem precisar editar JSON manualmente

4. **Validação de timezone**: Verificar se o timezone é válido ao carregar o config

5. **Configuração de retry**: Permitir configurar quantas tentativas fazer em caso de erro

## 📞 Suporte

Se você encontrar problemas após a atualização:

1. Verifique se o `config.json` existe e está bem formatado
2. Consulte a documentação em `CONFIG.md`
3. Veja a seção de "Solução de Problemas" no `README.md`
4. Abra uma issue no GitHub com detalhes do erro

## 📄 Licença

Mantém a mesma licença do projeto original (MIT).

---

**Data da atualização:** 26/11/2025  
**Versão:** 2.0.0 - Sistema de Configuração Centralizado
