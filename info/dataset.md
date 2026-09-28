# GoEmotions — dataset e decisões do projeto

Atualizado em **28/09/2026**. Projeto: **English Emotion Recognition**.

## 1. Decisão de escopo

O projeto passa a estudar reconhecimento multilabel de emoções **em inglês**, utilizando somente o **GoEmotions original**, na configuração `simplified` disponibilizada no Hugging Face. A documentação continua em português para facilitar o registro das decisões da equipe.

Esta decisão substitui a proposta anterior de trabalhar com BRIGHTER PT-BR e GoEmotions traduzido. Os motivos são:

- trabalhar diretamente com os textos no idioma de origem, sem depender da fidelidade de uma tradução;
- utilizar uma única taxonomia, evitando conversão entre conjuntos de emoções;
- aproveitar exemplos consolidados e divisões de treino, validação e teste já estabelecidas;
- concentrar o trabalho na comparação de métodos de classificação e na análise dos erros.

**Não foi incluído um segundo dataset.** O GoEmotions já oferece dados suficientes para iniciar baselines e fine-tuning. Outro corpus faria sentido futuramente para testar generalização fora do Reddit, mas introduziria diferenças de domínio e, possivelmente, de rótulos. Essa extensão não faz parte do escopo atual.

A tarefa mantém **27 emoções + a categoria neutra**, totalizando 28 saídas. Não será aplicado o agrupamento para seis emoções discutido na proposta anterior. Isso preserva a tarefa original e dispensa uma justificativa adicional para o mapeamento.

## 2. Origem, versão e unidade de observação

O GoEmotions foi apresentado por Demszky et al. (2020) e é formado por comentários do Reddit em inglês, anotados por humanos. A documentação original distingue os dados brutos, com avaliações individuais, de uma versão filtrada por concordância entre avaliadores. O projeto usa essa versão filtrada, em que os rótulos retidos contam com concordância de pelo menos dois avaliadores. [Fonte: documentação original](https://github.com/google-research/google-research/tree/master/goemotions).

| Propriedade | Valor adotado |
|---|---|
| Nome | GoEmotions |
| Idioma dos textos | Inglês |
| Modalidade | Texto tabular |
| Imagens | Nenhuma; resolução e canais não se aplicam |
| Origem | Comentários do Reddit |
| Repositório de distribuição | `google-research-datasets/go_emotions` |
| Configuração | `simplified` |
| Revisão fixada | `add492243ff905527e67aeb8b80c082af02207c3` |
| Unidade de cada linha | Um comentário com seus rótulos consolidados |
| Total utilizado | 54.263 comentários |
| Categorias | 27 emoções e `neutral` |
| Tipo de classificação | Multilabel |
| Destino local | `datasets/go_emotions/` |

Os CSVs brutos de avaliações não são usados. Assim, não é necessário reconstruir consenso por `rater_id` nem selecionar traduções. A expressão “simplified” identifica a configuração preparada para classificação; ela **não reduz o número de categorias**.

## 3. Separação dos exemplos

| Split no código | Comentários | Proporção aproximada | Uso |
|---|---:|---:|---|
| `train` | 43.410 | 80% | Treinamento dos modelos |
| `validation` | 5.426 | 10% | Seleção de hiperparâmetros, checkpoints e limiares |
| `test` | 5.427 | 10% | Avaliação final |
| **Total** | **54.263** | **100%** | |

As divisões foram confirmadas no download local. Não foram criados novos splits ou redistribuídos exemplos. Na distribuição original em TSV, o desenvolvimento aparece como `dev.tsv`; nesta configuração do Hugging Face, ele é chamado `validation`.

O teste não deve ser usado para ajustar modelos ou decidir limiares de classificação. Resultados obtidos em splits diferentes não devem ser apresentados como comparações diretamente equivalentes.

## 4. Estrutura de cada registro

| Campo | Tipo | Descrição |
|---|---|---|
| `text` | string | Comentário em inglês; entrada textual do modelo |
| `labels` | Lista de `ClassLabel`, armazenada como IDs inteiros | Uma ou mais categorias associadas ao comentário |
| `id` | string | Identificador do comentário |

Não há uma coluna binária para cada emoção nessa configuração. Os nomes das categorias ficam no esquema de `labels`, e cada registro contém a lista dos IDs positivos.

Exemplo **didático**, não extraído do corpus: `labels = [0, 15]` significa admiração e gratidão. Para treinar um classificador com 28 saídas, essa lista pode ser convertida em um vetor de 28 posições, com `1` nos índices 0 e 15 e `0` nos demais. Esse vetor é chamado multi-hot.

Como um comentário pode ter vários rótulos, não se deve reduzir `labels` ao primeiro elemento. Um Transformer para essa tarefa normalmente utiliza 28 logits, sigmoid por categoria e uma perda binária multilabel. Arquitetura e limiares exatos ainda serão definidos no protocolo de treinamento.

`neutral` é uma categoria explícita, com ID 27. Um exemplo exclusivamente neutro é representado por `[27]`, não por uma lista vazia. O tratamento de eventuais previsões simultâneas de neutro e emoções deverá ser definido e avaliado na validação.

## 5. Categorias e distribuição

IDs e contagens medidos na revisão local. As traduções são apenas explicativas; os nomes originais e os IDs serão preservados no código.

| ID | Rótulo | Significado | Treino | Validação | Teste |
|---:|---|---|---:|---:|---:|
| 0 | admiration | admiração | 4.130 | 488 | 504 |
| 1 | amusement | divertimento | 2.328 | 303 | 264 |
| 2 | anger | raiva | 1.567 | 195 | 198 |
| 3 | annoyance | irritação | 2.470 | 303 | 320 |
| 4 | approval | aprovação | 2.939 | 397 | 351 |
| 5 | caring | cuidado | 1.087 | 153 | 135 |
| 6 | confusion | confusão | 1.368 | 152 | 153 |
| 7 | curiosity | curiosidade | 2.191 | 248 | 284 |
| 8 | desire | desejo | 641 | 77 | 83 |
| 9 | disappointment | decepção | 1.269 | 163 | 151 |
| 10 | disapproval | desaprovação | 2.022 | 292 | 267 |
| 11 | disgust | nojo | 793 | 97 | 123 |
| 12 | embarrassment | constrangimento | 303 | 35 | 37 |
| 13 | excitement | entusiasmo | 853 | 96 | 103 |
| 14 | fear | medo | 596 | 90 | 78 |
| 15 | gratitude | gratidão | 2.662 | 358 | 352 |
| 16 | grief | pesar/luto | 77 | 13 | 6 |
| 17 | joy | alegria | 1.452 | 172 | 161 |
| 18 | love | amor | 2.086 | 252 | 238 |
| 19 | nervousness | nervosismo | 164 | 21 | 23 |
| 20 | optimism | otimismo | 1.581 | 209 | 186 |
| 21 | pride | orgulho | 111 | 15 | 16 |
| 22 | realization | percepção/compreensão | 1.110 | 127 | 145 |
| 23 | relief | alívio | 153 | 18 | 11 |
| 24 | remorse | remorso | 545 | 68 | 56 |
| 25 | sadness | tristeza | 1.326 | 143 | 156 |
| 26 | surprise | surpresa | 1.060 | 129 | 141 |
| 27 | neutral | neutro | 14.219 | 1.766 | 1.787 |

As contagens não somam o total de comentários, pois as categorias não são mutuamente exclusivas. Há **7.102** exemplos com mais de um rótulo no treino, **878** na validação e **837** no teste.

O desbalanceamento é relevante: no treino, `neutral` aparece em 14.219 exemplos, enquanto `grief` aparece em 77. A avaliação proposta é Macro-F1, Micro-F1 e F1 por categoria, acompanhadas de precisão, recall e análise qualitativa. O protocolo deverá explicitar se a métrica inclui `neutral` — a proposta inicial é incluir os 28 rótulos e reportar todos individualmente.

## 6. Formato e tamanho

O corpus original filtrado é distribuído em TSV. A revisão utilizada pelo código é distribuída em **Parquet** no Hugging Face e salva com `DatasetDict.save_to_disk` em **Apache Arrow**, acompanhado de metadados JSON. O manifesto `source.json` é criado pelo projeto para registrar repositório, configuração e revisão.

```text
datasets/go_emotions/
├── dataset_dict.json
├── source.json
├── train/
│   ├── data-00000-of-00001.arrow
│   ├── dataset_info.json
│   └── state.json
├── validation/
│   ├── data-00000-of-00001.arrow
│   ├── dataset_info.json
│   └── state.json
└── test/
    ├── data-00000-of-00001.arrow
    ├── dataset_info.json
    └── state.json
```

| Arquivo ou medida | Bytes | MB decimais aproximados |
|---|---:|---:|
| Arrow de treino | 4.240.272 | 4,240 |
| Arrow de validação | 530.056 | 0,530 |
| Arrow de teste | 527.376 | 0,527 |
| **Total Arrow** | **5.297.704** | **5,298** |
| Pasta salva, incluindo JSON e manifesto | 5.303.986 | 5,304 |
| Download informado pela biblioteca | 3.464.371 | 3,464 |
| Tamanho lógico informado pela biblioteca | 5.283.701 | 5,284 |

MB significa 1.000.000 bytes. O tamanho da pasta não inclui o cache externo do Hugging Face. Download comprimido, tamanho lógico e arquivos salvos são medidas distintas. Esses números não estimam RAM ou VRAM para treinamento e podem variar se a serialização ou a versão das bibliotecas mudar.

## 7. Comprimentos e verificações iniciais

Comprimentos medidos em caracteres de `text`, sem normalização:

| Split | Mínimo | Mediana | Máximo |
|---|---:|---:|---:|
| Treino | 2 | 65 | 703 |
| Validação | 5 | 64 | 187 |
| Teste | 5 | 65 | 184 |

Caracteres não são tokens. O limite de sequência do modelo será definido após medir os textos com o tokenizador escolhido, utilizando treino/validação.

O download foi validado quanto a nomes e tamanhos dos splits, colunas, ordem dos 28 rótulos, presença de texto/ID/lista de rótulos e intervalo válido dos IDs de categorias. Os identificadores de comentários são únicos por split e não se repetem entre splits.

Entretanto, existem strings de texto exatamente iguais associadas a IDs diferentes:

| Pares de splits | Strings distintas compartilhadas |
|---|---:|
| Treino e validação | 41 |
| Treino e teste | 32 |
| Validação e teste | 10 |

Esses números contam interseções de conjuntos de strings, não pares de linhas. Não foi realizada auditoria de duplicação aproximada ou semântica. Nenhum exemplo foi removido: preservamos as divisões publicadas. Antes do treinamento, deverá ser registrado se os splits oficiais serão mantidos integralmente para comparabilidade ou se haverá também um experimento separado com deduplicação. As estatísticas de teste aqui são descritivas; não foram usadas para escolher um modelo.

## 8. Como baixar e carregar

Na raiz do projeto, com o ambiente Python ativo e as dependências de `requirements.txt` instaladas:

```bash
python download_dataset.py
```

Também é possível executar `trazendo_datasets.ipynb`, selecionando o kernel do ambiente do projeto. O notebook chama a mesma função do script; não mantém uma implementação duplicada do download. Execute-o com a raiz do projeto como diretório de trabalho.

O script fixa a revisão de origem, valida a estrutura antes de salvar e reutiliza a cópia local nas próximas execuções. Se encontrar uma pasta sem manifesto compatível, interrompe com uma mensagem em vez de sobrescrevê-la. Nesse caso, inspecione a pasta; para refazer um download interrompido, remova somente a cópia incompleta depois de confirmar seu conteúdo.

Para trabalhar com a cópia já salva, sem novo download:

```python
from datasets import load_from_disk

dataset = load_from_disk("datasets/go_emotions")
train = dataset["train"]
validation = dataset["validation"]
test = dataset["test"]
label_names = train.features["labels"].feature.names
```

`datasets/` é ignorado pelo Git. O repositório guarda código e documentação; os arquivos de dados são reproduzidos pelo script. As pastas antigas `datasets/brighter/` e `datasets/go_emotions_ptbr/` foram retiradas do projeto. A remoção no estado atual não apaga versões antigas do histórico Git.

## 9. Próximas decisões

- Construir um baseline TF-IDF + classificadores binários de regressão logística e compará-lo a fine-tuning de um Transformer.
- Definir arquitetura, tokenizador, hiperparâmetros, sementes e orçamento computacional.
- Definir limiares de predição e tratamento de neutro usando validação.
- Decidir política de duplicações, tratamento de classes raras e eventual ponderação da perda.
- Registrar métricas, tempo de treinamento e análise de erros antes de ampliar o escopo.

Esses itens são propostas de execução; ainda não houve treinamento nem seleção de modelo. Nenhum segundo dataset está previsto no código.

## 10. Fontes, limitações e reprodução

Contagens, comprimentos e frequências foram calculados diretamente nos dados baixados na revisão fixada: `len` para linhas, conjuntos para IDs/textos distintos, contagem de IDs em `labels` para frequências e tamanho físico de arquivo para bytes. O arquivo `source.json` registra a proveniência do download.

A distribuição original declara licença Apache 2.0. O corpus reflete linguagem e comunidades do Reddit; não representa automaticamente todos os contextos de comunicação em inglês. A anotação emocional é subjetiva e pode apresentar desacordos. [Fonte: repositório original e licença](https://github.com/google-research/google-research/tree/master/goemotions).

- [GoEmotions no Hugging Face](https://huggingface.co/datasets/google-research-datasets/go_emotions).
- [GoEmotions: A Dataset of Fine-Grained Emotions — artigo](https://aclanthology.org/2020.acl-main.372/).
- [Documentação e dados originais](https://github.com/google-research/google-research/tree/master/goemotions).

Ao escrever o trabalho, citar Demszky et al. (2020), identificar a configuração `simplified` e informar a revisão utilizada. A comparação futura com resultados publicados também deve conferir taxonomia, splits, métricas e política de limiares.
