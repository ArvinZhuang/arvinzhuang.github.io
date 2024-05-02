---
title: "PromptReps: Prompting Large Language Models to Generate Dense and Sparse Representations for Zero-Shot Document Retrieval"
collection: publications
permalink: /publication/arxiv2024PromptReps
year: 2024
venue: 'Arxiv Preprint'
authors: <strong>Shengyao Zhuang</strong>, Xueguang Ma, Bevan Koopman, Jimmy Lin, and Guido Zuccon.
track: Short paper
---
---

## Abstract
The current use of large language models
(LLMs) for zero-shot document ranking follows one of two ways: 1) prompt-based reranking methods, which require no further training but are feasible for only re-ranking a handful of candidate documents due to the associated computational costs; and 2) unsupervised
contrastive trained dense retrieval methods,
which can retrieve relevant documents from
the entire corpus but require a large amount of
paired text data for contrastive training. In this
paper, we propose PromptReps, which combines the advantages of both categories: no
need for training and the ability to retrieve from
the whole corpus. Our method only requires
prompts to guide an LLM to generate query
and document representations for effective document retrieval. Specifically, we prompt the
LLMs to represent a given text using a single word, and then use the last token’s hidden
states and the corresponding logits associated
to the prediction of the next token to construct
a hybrid document retrieval system. The retrieval system harnesses both dense text embedding and sparse bag-of-words representations
given by the LLM. Our experimental evaluation on the BEIR zero-shot document retrieval
datasets illustrates that this simple promptbased LLM retrieval method can achieve a
similar or higher retrieval effectiveness than
state-of-the-art LLM embedding methods that
are trained with large amounts of unsupervised
data, especially when using a larger LLM.1

[Download paper here](https://arxiv.org/pdf/2404.18424)

[Code](https://github.com/ielab/PromptReps)
