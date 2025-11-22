# GitHub Actions em Repositórios Privados

## ✅ Sim, funciona perfeitamente!

Este guia responde à pergunta: **"Você pode rodar uma action dentro de um repositório privado meu?"**

**Resposta: SIM!** GitHub Actions funciona perfeitamente em repositórios privados.

## 🔑 Diferenças entre repositórios públicos e privados

### Repositórios Públicos
- ✅ Minutos de execução **ilimitados** e gratuitos
- ✅ Sem limite de armazenamento de artifacts
- ✅ Ideal para projetos open source

### Repositórios Privados
- ✅ Funciona da **mesma forma** que em repos públicos
- ⚠️ Possui limite de minutos gratuitos por mês
- ⚠️ Minutos variam conforme o plano do GitHub

## 💰 Limites gratuitos para repositórios privados

| Plano | Minutos/mês | Armazenamento |
|-------|-------------|---------------|
| **Free** | 2.000 min | 500 MB |
| **Pro** | 3.000 min | 1 GB |
| **Team** | 10.000 min | 2 GB |
| **Enterprise** | 50.000 min | 50 GB |

### Quanto este projeto consome?

- **Por execução**: ~2-3 minutos
- **Execuções/dia**: 2 (entrada e saída)
- **Dias úteis/mês**: ~22
- **Total/mês**: ~88-132 minutos

**Conclusão**: Bem dentro do limite gratuito! 🎉

## 🚀 Como habilitar GitHub Actions no seu repositório privado

### 1. Verifique se Actions está habilitado

1. Acesse seu repositório no GitHub
2. Clique na aba **Actions**
3. Se você ver uma mensagem pedindo para habilitar, clique em **"I understand my workflows, go ahead and enable them"**

### 2. Configure os Secrets (Obrigatório)

GitHub Actions precisa de credenciais para funcionar. Configure os secrets:

1. Vá em **Settings** → **Secrets and variables** → **Actions**
2. Clique em **New repository secret**
3. Adicione cada secret necessário (veja o README.md para lista completa)

### 3. Ajuste permissões (se necessário)

Para repositórios de organizações:

1. Vá em **Settings** → **Actions** → **General**
2. Em "Actions permissions", selecione:
   - ✅ **"Allow all actions and reusable workflows"**
   ou
   - ✅ **"Allow [owner], and select non-[owner], actions and reusable workflows"**

### 4. Execute o workflow

**Automaticamente:**
- O workflow está configurado para rodar em horários específicos
- Aguarde o horário programado no `schedule`

**Manualmente:**
1. Vá em **Actions**
2. Selecione o workflow **"Bater ponto automático"**
3. Clique em **"Run workflow"**
4. Escolha a branch
5. Clique em **"Run workflow"**

## 📊 Monitore o uso de minutos

### Como verificar quanto você está usando:

1. Acesse **Settings** → **Billing and plans**
2. Veja a seção **"Actions & Packages"**
3. Você verá:
   - Minutos usados no mês atual
   - Minutos incluídos no seu plano
   - Histórico de uso

### Dica para economizar minutos:

Se você quiser economizar ainda mais:
- Ajuste os horários de `schedule` para executar apenas quando necessário
- Use `workflow_dispatch` para executar manualmente quando precisar
- Considere reduzir o tempo de espera no código Python

## 🔒 Segurança em repositórios privados

### Por que é seguro usar Actions em repos privados:

1. **Secrets são criptografados**
   - Armazenados de forma segura pelo GitHub
   - Nunca aparecem em logs
   - Não são acessíveis via API

2. **Ambiente isolado**
   - Cada execução roda em uma máquina virtual isolada
   - Ambiente é destruído após a execução
   - Sem risco de dados remanescentes

3. **Código privado permanece privado**
   - Apenas pessoas com acesso ao repo veem o código
   - Logs são visíveis apenas para pessoas com acesso
   - Artifacts são privados

4. **Controle de permissões**
   - Você controla quem pode executar workflows
   - Pode restringir aprovações para execuções

## 🆚 GitHub Actions vs outras alternativas

| Recurso | GitHub Actions | Jenkins | GitLab CI | Circle CI |
|---------|----------------|---------|-----------|-----------|
| Hospedado no GitHub | ✅ Sim | ❌ Não | ❌ Não | ✅ Sim |
| Setup zero | ✅ Sim | ❌ Não | ⚠️ Depende | ✅ Sim |
| Funciona em repo privado | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |
| Minutos gratuitos | ✅ 2.000+ | ❌ N/A | ✅ 400 | ✅ 6.000 |
| Integração nativa GitHub | ✅ Perfeita | ⚠️ Via plugin | ⚠️ Via integration | ⚠️ Via integration |

## ❓ Perguntas Frequentes

### 1. Preciso pagar para usar Actions em repo privado?
**Não**, se você ficar dentro do limite gratuito (2.000 minutos/mês no plano Free).

### 2. O que acontece se eu ultrapassar os minutos?
- O GitHub para de executar workflows automaticamente
- Você pode comprar minutos adicionais (se no plano pago)
- Ou esperar o próximo mês para o limite resetar

### 3. Posso ver os logs das execuções?
**Sim!** Vá em Actions → selecione uma execução → veja os logs detalhados.

### 4. Outras pessoas podem ver meus workflows privados?
**Não**, apenas pessoas com acesso ao repositório podem ver workflows, logs e resultados.

### 5. Preciso de um servidor próprio?
**Não**, GitHub Actions usa runners hospedados pelo GitHub. Tudo roda na nuvem.

### 6. Posso usar em todos os meus repos privados?
**Sim**, cada repositório tem seu próprio limite de minutos.

### 7. E se eu tiver uma organização?
- Organizações têm limites próprios
- Minutos são compartilhados entre repos da organização
- Administradores podem ver uso consolidado

## 📚 Recursos adicionais

- [Documentação oficial GitHub Actions](https://docs.github.com/actions)
- [Billing for GitHub Actions](https://docs.github.com/billing/managing-billing-for-github-actions)
- [Usage limits](https://docs.github.com/actions/learn-github-actions/usage-limits-billing-and-administration)

## ✅ Conclusão

**Sim, você pode rodar GitHub Actions em repositórios privados!**

Este projeto está configurado e pronto para usar. Basta:
1. ✅ Configurar os secrets
2. ✅ Habilitar Actions (se necessário)
3. ✅ Deixar rodar automaticamente ou executar manualmente

Para mais detalhes de configuração específica deste projeto, consulte o [README.md](README.md).
