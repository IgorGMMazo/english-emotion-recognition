# 🇧🇷 PT-BR Emotion Recognition

Projeto desenvolvido para a disciplina de Processamento de Linguagem Natural (NLP), com o objetivo de investigar técnicas de reconhecimento e classificação de emoções em textos escritos em Português Brasileiro.

O projeto busca comparar diferentes estratégias de classificação de emoções, com foco no fine-tuning de modelos de linguagem pré-treinados.

## 🎯 Objetivo

Desenvolver e avaliar modelos capazes de identificar emoções presentes em textos em Português Brasileiro.

Diferentemente de uma análise de sentimentos tradicional, que normalmente classifica um texto como positivo, negativo ou neutro, este projeto trabalha com emoções mais específicas.

No dataset BRIGHTER, são consideradas seis categorias:

- Anger (raiva)
- Disgust (nojo)
- Fear (medo)
- Joy (alegria)
- Sadness (tristeza)
- Surprise (surpresa)

O problema é tratado como classificação multilabel, ou seja, um mesmo texto pode apresentar mais de uma emoção simultaneamente.

---

## 📊 Datasets

### 1. BRIGHTER

Dataset multilíngue para reconhecimento de emoções que possui uma configuração específica para Português Brasileiro (PT-BR).

**PT-BR:**

| Split | Instâncias |
|------|-----------:|
| Train | 2.226 |
| Dev | 400 |
| Test | 4.452 |
| **Total** | **7.078** |

O BRIGHTER será considerado o principal benchmark do projeto.

Dataset:

https://huggingface.co/datasets/brighter-dataset/BRIGHTER-emotion-categories

---

### 2. GoEmotions PT-BR

Versão em Português Brasileiro do dataset GoEmotions.

O GoEmotions original foi desenvolvido para classificação granular de emoções e possui 27 categorias emocionais, além da categoria neutra.

**PT-BR:**

| Split | Instâncias |
|------|-----------:|
| Train | 43.410 |
| Validation | 5.426 |
| Test | 5.427 |
| **Total** | **54.263** |

Uma diferença importante é que o GoEmotions original foi produzido em inglês e esta versão foi obtida através da tradução dos textos para Português Brasileiro.

Dataset:

https://huggingface.co/datasets/antoniomenezes/go_emotions_ptbr

---

# 🧪 Cenários Experimentais

Inicialmente, o projeto considera dois possíveis cenários de experimentação.

## Cenário 1 — Fine-tuning utilizando somente o BRIGHTER

No primeiro cenário, o modelo será treinado utilizando apenas os dados em Português Brasileiro do BRIGHTER.

Fluxo:

BRIGHTER PT-BR
      ↓
Train (2.226)
      ↓
Fine-tuning
      ↓
Modelo especializado
      ↓
Test BRIGHTER (4.452)
      ↓
Avaliação

Esse cenário permite investigar o desempenho de modelos pré-treinados em uma situação com quantidade relativamente limitada de dados anotados.

Uma possível questão de pesquisa é:

> Qual é o desempenho de modelos de linguagem pré-treinados após fine-tuning para reconhecimento multilabel de emoções em Português Brasileiro em um cenário de poucos dados?

Também poderão ser construídas curvas de aprendizado utilizando diferentes porcentagens do conjunto de treinamento:

10% → 25% → 50% → 75% → 100%

Isso permitirá analisar o impacto da quantidade de dados sobre o desempenho do modelo.

---

## Cenário 2 — BRIGHTER + GoEmotions PT-BR

O segundo cenário investiga se uma quantidade maior de dados, provenientes de um dataset traduzido, pode melhorar o reconhecimento de emoções em Português Brasileiro.

Uma possível estratégia é utilizar dados do GoEmotions PT-BR como dados adicionais durante o treinamento e manter o BRIGHTER como benchmark de avaliação.

GoEmotions PT-BR
       +
BRIGHTER Train
       ↓
Treinamento / Fine-tuning
       ↓
Modelo especializado
       ↓
BRIGHTER Test
       ↓
Avaliação

A ideia é manter o conjunto de teste do BRIGHTER como referência para permitir uma comparação justa entre os experimentos.

A principal questão de pesquisa desse cenário é:

> Dados traduzidos automaticamente podem melhorar o desempenho de modelos de reconhecimento de emoções treinados em um cenário com poucos dados nativos em Português Brasileiro?

Esse experimento também permite investigar possíveis problemas de domain shift e artefatos introduzidos pelo processo de tradução.

> Observação: BRIGHTER e GoEmotions utilizam esquemas de emoções diferentes. Portanto, antes desse experimento será necessário definir um mapeamento entre as categorias compatíveis dos dois datasets.

---

## 📏 Avaliação

Como o problema é multilabel e pode apresentar desbalanceamento entre as emoções, serão consideradas métricas como:

- Macro-F1
- Micro-F1
- Precision
- Recall
- F1 por emoção

O Macro-F1 será especialmente importante porque atribui o mesmo peso a cada categoria, evitando que emoções mais frequentes dominem a avaliação.

Também será realizada uma análise qualitativa dos erros do modelo, buscando identificar dificuldades relacionadas a fenômenos como:

- emoções implícitas;
- múltiplas emoções;
- negação;
- sarcasmo;
- linguagem informal;
- ambiguidades.

---

## 🔬 Possíveis Experimentos

O projeto poderá comparar diferentes abordagens de NLP, como:

1. Métodos clássicos de Machine Learning;
2. Transformers pré-treinados com fine-tuning;
3. Modelos de linguagem utilizando zero-shot ou few-shot prompting.

Um possível baseline clássico seria:

TF-IDF → Logistic Regression

que posteriormente poderá ser comparado com modelos baseados em Transformers.

---

## 📌 Status

🚧 Projeto em desenvolvimento.

As arquiteturas, modelos e estratégias definitivas de treinamento serão determinadas após a análise exploratória dos datasets e o desenvolvimento dos primeiros baselines.