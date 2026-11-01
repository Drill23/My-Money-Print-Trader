# Robô "Tendência BTC 3 de 6": manual de configuração e operação na Binance (Spot)

**Para:** assistente responsável por operar a conta na Binance
**Capital inicial:** R$ 50,00
**Tipo de operação:** somente Spot (compra e venda à vista). **Sem alavancagem, sem margem, sem futuros.**

---

## 1. O que este robô faz (em uma frase)

Uma vez por dia, logo depois do fechamento do candle diário do Bitcoin, o robô confere **6 indicadores de tendência**.
Se **3 ou mais** apontarem alta, o dinheiro fica **100% em Bitcoin**. Se **2 ou menos** apontarem alta, o dinheiro fica **100% em reais (caixa)**.
Entre uma checagem e outra fica valendo uma ordem de proteção (stop) contra quedas extremas.

Não há palpites, notícias nem "sensação de mercado". A decisão é sempre a da tabela da Seção 6.

---

## 2. Regras de ouro (não negociáveis)

1. **Nunca** usar Futuros, Margem, alavancagem, "Convert com alavancagem", empréstimos ou produtos "Earn" com o dinheiro desta estratégia.
2. **Nunca** comprar "um pouco mais" quando o preço cai, nem vender "para garantir" fora da regra.
3. Fazer a checagem **todos os dias**, inclusive fins de semana e feriados (cripto negocia 24/7).
4. Usar sempre o **candle diário já FECHADO**, nunca o candle que está se formando.
5. Registrar toda checagem na planilha de controle (Seção 9), mesmo quando a decisão for "não fazer nada".
6. Em caso de dúvida, **não operar** e avisar o titular da conta.

---

## 3. Preparação da conta (fazer uma única vez)

### 3.1 Segurança
1. Entrar na Binance pelo endereço oficial **www.binance.com** (ou pelo app oficial).
2. Em **Perfil → Segurança**:
   - Ativar a **Autenticação de 2 fatores (2FA)** com app autenticador (Google Authenticator ou Binance Authenticator).
   - Ativar o **Código Antiphishing** (todo e-mail legítimo da Binance passa a exibir esse código).
   - Ativar a **Lista de permissões de endereços de saque (Whitelist)**. Esta estratégia nunca precisa sacar cripto.
3. **Não** criar chaves de API. Esta estratégia é operada manualmente pela interface.

### 3.2 Verificar se não há nada ativo além do Spot
1. Em **Carteira → Visão geral**, confirmar que os R$ 50 estão na **Carteira Spot**.
2. Não ativar a conta de Futuros nem a de Margem. Se aparecer convite ou termo para ativá-las, recusar.

### 3.3 Depósito
1. **Carteira → Depositar → BRL → Pix**.
2. Depositar **R$ 50,00**.
3. Confirmar que o saldo de **BRL** apareceu na **Carteira Spot**.

### 3.4 Escolher o par de execução
- **Par principal de execução: `BTC/BRL`** (compra e venda de Bitcoin diretamente em reais, sem conversões extras).
- **Antes da primeira operação**, abrir **Mercados → Spot → BTC/BRL** e conferir:
  - se o par está disponível para negociação;
  - o **valor mínimo de ordem** (no formulário de compra aparece um aviso quando o valor é baixo demais; também consta em **Mais → Regras de negociação**).
- **Se `BTC/BRL` não estiver disponível ou o mínimo for maior que o saldo:** usar o plano B:
  1. **Comprar cripto → Converter** (ou **Trade → Converter**): converter os **BRL para USDT**.
  2. Operar no par **`BTC/USDT`**. Todo o resto do manual continua igual, trocando "BRL" por "USDT".

---

## 4. Preparação do gráfico de leitura dos sinais (fazer uma única vez)

Os sinais são sempre lidos no gráfico **`BTC/USDT`**, que é o mercado de referência mais líquido do mundo. Mesmo que a execução seja em `BTC/BRL`, a **leitura** é no `BTC/USDT`.

Usar a **versão web (computador)**, porque ela tem o gráfico TradingView completo.

1. Abrir **Trade → Spot → par `BTC/USDT`**.
2. Acima do gráfico, clicar em **"TradingView"** (não usar a visão "Original"/"Básica").
3. Selecionar o tempo gráfico **"1D"** (um candle por dia).
4. Fuso horário: no canto inferior direito do gráfico, escolher **UTC**.
   - O candle diário da Binance **fecha às 00:00 UTC = 21:00 no horário de Brasília**.
5. Adicionar os indicadores (botão **"Indicadores" / ƒx**):

| # | Indicador (nome no TradingView) | Configuração | Nome curto neste manual |
|---|---|---|---|
| 1 | **Moving Average** (Média Móvel Simples) | Length (Comprimento) = **30**, Source = **close**, Offset = 0 | MM30 |
| 2 | **Moving Average** | Length = **50**, Source = **close**, Offset = 0 | MM50 |
| 3 | **Moving Average** | Length = **100**, Source = **close**, Offset = 0 | MM100 |
| 4 | **Rate Of Change (ROC)** | Length = **14**, Source = **close** | ROC14 |
| 5 | **Rate Of Change (ROC)** | Length = **28**, Source = **close** | ROC28 |
| 6 | **Rate Of Change (ROC)** | Length = **56**, Source = **close** | ROC56 |

- Atenção: precisa ser a **média SIMPLES** ("Moving Average" / "MA" / "SMA"). **Não** usar "EMA" (exponencial).
- Dica: dar uma cor diferente a cada média e salvar o layout do gráfico (ícone de nuvem / "Salvar layout") para não precisar refazer.
- **Alternativa sem o ROC:** o ROC só responde à pergunta "o fechamento de hoje é maior que o fechamento de N dias atrás?". Se o indicador ROC não estiver disponível, basta passar o cursor sobre o candle de N dias antes e comparar o **fechamento (C)** dele com o fechamento do último candle fechado.

---

## 5. Rotina diária: a checagem (todos os dias)

**Horário:** entre **21:05 e 22:00 (Brasília)**, ou seja, logo após o fechamento do candle diário às 21:00.
Se não for possível nesse horário, fazer **assim que possível**, sempre usando o **último candle diário fechado**.

### Passo 1: identificar o candle certo
- No gráfico 1D do `BTC/USDT`, o candle mais à direita acabou de começar e **NÃO deve ser usado**.
- Usar o **penúltimo candle**, o que fechou às 21:00. Passar o cursor sobre ele e anotar:
  - **Fechamento (C)** desse candle;
  - valor da **MM30**, **MM50** e **MM100** nesse candle;
  - valor do **ROC14**, **ROC28** e **ROC56** nesse candle.

### Passo 2: preencher o placar (1 ponto por "SIM")

| Teste | Pergunta | SIM = 1 ponto |
|---|---|---|
| T1 | Fechamento > MM30? | ☐ |
| T2 | Fechamento > MM50? | ☐ |
| T3 | Fechamento > MM100? | ☐ |
| T4 | ROC14 > 0? (fechamento maior que o de 14 dias atrás) | ☐ |
| T5 | ROC28 > 0? (fechamento maior que o de 28 dias atrás) | ☐ |
| T6 | ROC56 > 0? (fechamento maior que o de 56 dias atrás) | ☐ |
| | **PONTOS (0 a 6)** | **___** |

- Valor exatamente igual (empate) conta como **NÃO** (0 ponto).

### Passo 3: decidir pela tabela da Seção 6 e executar (Seção 7).

### Passo 4: registrar tudo na planilha (Seção 9).

---

## 6. Tabela de decisão

| Pontos | Situação atual da carteira | AÇÃO |
|---|---|---|
| **3, 4, 5 ou 6** | Está em **reais (BRL)** | **COMPRAR BTC** com 100% do saldo (Seção 7.1) e criar o stop de proteção (Seção 7.3) |
| **3, 4, 5 ou 6** | Já está em **BTC** | **MANTER**. Apenas **atualizar o stop** de proteção (Seção 7.3) |
| **0, 1 ou 2** | Está em **BTC** | **VENDER TODO o BTC** (Seção 7.2) e ficar em reais |
| **0, 1 ou 2** | Já está em **reais (BRL)** | **NÃO FAZER NADA** |

Resumo: **3 ou mais pontos = Bitcoin. 2 ou menos = reais.**

---

## 7. Como executar cada ação na Binance

### 7.1 COMPRAR (entrar no BTC)
1. Abrir **Trade → Spot → `BTC/BRL`**.
2. No painel de ordens, aba **Comprar**, tipo **"Mercado" (Market)**.
3. Em "Total" (valor em BRL), arrastar a barra para **100%** do saldo disponível.
4. Clicar em **Comprar BTC** e confirmar.
5. Conferir em **Ordens → Histórico de negociações** se a ordem foi executada.
6. Seguir imediatamente para a **Seção 7.3** (stop de proteção).

### 7.2 VENDER (sair do BTC)
1. **Primeiro cancelar o stop de proteção que estiver aberto:** **Ordens → Ordens abertas → Cancelar** a ordem Stop-Limit. Enquanto ela existir, o BTC fica bloqueado e a venda não passa.
2. Em **Trade → Spot → `BTC/BRL`**, aba **Vender**, tipo **"Mercado" (Market)**.
3. Em "Quantidade" (BTC), arrastar a barra para **100%**.
4. Clicar em **Vender BTC** e confirmar.
5. Conferir no **Histórico de negociações**.
6. Se sobrar uma quantidade minúscula de BTC que a Binance não deixa vender (abaixo do mínimo), ignorar. Ela será vendida junto na próxima venda.

### 7.3 STOP DE PROTEÇÃO (seguro contra quedas extremas)
Serve só para catástrofes entre uma checagem e outra. Em condições normais ele **nunca** é acionado.

**Ao comprar, e em TODA checagem diária em que a carteira estiver em BTC:**
1. **Ordens → Ordens abertas**: se existir um Stop-Limit antigo, **cancelar**.
2. Ver o **último preço** do par `BTC/BRL` (topo da tela). Chamar esse valor de **P**.
3. No painel de ordens, aba **Vender**, tipo **"Stop Limit"**:
   - **Stop (gatilho)** = **P × 0,75** (25% abaixo do preço atual);
   - **Limite** = **P × 0,74** (um pouco abaixo do gatilho, para garantir a execução);
   - **Quantidade** = **100%** do BTC.
4. Clicar em **Vender BTC** e confirmar.
5. Conferir em **Ordens abertas** se o Stop-Limit aparece.

> Exemplo de cálculo (números ilustrativos): se P = R$ 400.000, o gatilho fica em R$ 300.000 e o limite em R$ 296.000.

**Se o stop for executado** (a carteira amanhece em reais sem que ninguém tenha vendido):
- Não recomprar no mesmo dia.
- Na checagem diária seguinte, seguir normalmente a tabela da Seção 6.

---

## 8. Situações especiais

| Situação | O que fazer |
|---|---|
| Esqueceu ou não conseguiu fazer a checagem no horário | Fazer assim que possível, usando o **último candle diário fechado**. Nunca "compensar" operando duas vezes. |
| Binance em manutenção ou instável | Esperar normalizar e então fazer a checagem. O stop de proteção continua valendo. |
| Ordem rejeitada por "valor mínimo" | Não insistir. Registrar na planilha e avisar o titular da conta. |
| Ordem a mercado executada em partes | Normal. Conferir se o total foi executado no histórico. |
| Dúvida sobre se um teste deu SIM ou NÃO (valores muito próximos) | Usar os números exatos do cursor. Se forem iguais, conta **NÃO**. |
| Notícia forte, "todo mundo comprando/vendendo", pânico | **Ignorar.** Só vale a tabela da Seção 6. |
| Titular quer adicionar mais dinheiro | Depositar em BRL. Na próxima checagem: se a carteira estiver em BTC, comprar BTC com o novo saldo (e refazer o stop com 100% da quantidade); se estiver em reais, deixar em reais. |
| Titular quer sacar | Se estiver em BTC, vender primeiro (Seção 7.2) e então sacar em BRL via Pix. |

---

## 9. Planilha de controle (preencher em toda checagem)

Criar uma planilha com estas colunas:

| Data | Hora | Fech. BTC/USDT | MM30 | MM50 | MM100 | ROC14 | ROC28 | ROC56 | Pontos | Carteira antes | Ação | Preço execução (BRL) | Stop: gatilho / limite | Saldo total (R$) | Observações |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | BRL / BTC | Comprar / Vender / Manter / Nada | | | | |

Enviar ao titular um resumo **semanal** (cópia das linhas da semana).

---

## 10. Primeiro dia (início da operação)

1. Fazer a preparação das Seções 3 e 4.
2. Fazer a checagem da Seção 5 com o **último candle diário fechado**, mesmo que não seja 21:00.
3. Aplicar a tabela da Seção 6:
   - se der **3 ou mais pontos**: comprar BTC e criar o stop;
   - se der **2 ou menos**: **não comprar nada**. O dinheiro fica em reais, aguardando o sinal. **Isso é normal e faz parte da estratégia.** Haverá dias e até semanas seguidas em caixa.
4. A partir daí, seguir a rotina diária.

---

## 11. Glossário rápido

- **Candle diário (1D):** barra que resume um dia de preço (abertura, máxima, mínima, fechamento). Na Binance cada candle diário vai de 00:00 a 00:00 UTC (21:00 a 21:00 em Brasília).
- **Fechamento (C / Close):** último preço do candle.
- **MM30 / MM50 / MM100:** média simples dos fechamentos dos últimos 30, 50 e 100 dias.
- **ROC (Rate of Change):** variação percentual entre o fechamento de hoje e o de N dias atrás. ROC > 0 significa "hoje está mais alto que N dias atrás".
- **Ordem a Mercado:** executa na hora, pelo melhor preço disponível.
- **Stop-Limit:** ordem que fica "dormindo" e só é enviada quando o preço atinge o gatilho (Stop), sendo executada até o preço Limite.
- **Spot:** compra e venda real do ativo, sem alavancagem.
