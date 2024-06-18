---
title: "PromptReps: Prompting Large Language Models to Generate Dense and Sparse Representations for Zero-Shot Document Retrieval"
collection: publications
permalink: /publication/arxiv2024PromptReps
year: 2024
venue: 'Arxiv Preprint'
authors: <strong>Shengyao Zhuang</strong>, Xueguang Ma, Bevan Koopman, Jimmy Lin, and Guido Zuccon.
track: Long paper
---
---

## Abstract
Utilizing large language models (LLMs) for zero-shot document ranking is done in one of two ways: 1) prompt-based re-ranking methods, which require no further training but are only feasible for re-ranking a handful of candidate documents due to computational costs; and 2) unsupervised contrastive trained dense retrieval methods, which can retrieve relevant documents from the entire corpus but require a large amount of paired text data for contrastive training. 
In this paper, we propose PromptReps, which combines the advantages of both categories: no need for training and the ability to retrieve from the whole corpus. Our method only requires prompts to guide an LLM to generate query and document representations for effective document retrieval. Specifically, we prompt the LLMs to represent a given text using a single word, and then use the last token's hidden states and the corresponding logits associated with the prediction of the next token to construct a hybrid document retrieval system. The retrieval system harnesses both dense text embedding and sparse bag-of-words representations given by the LLM. We further explore variations of this core idea that consider the generation of multiple words, and representations that rely on multiple embeddings and sparse distributions. Our experimental evaluation on the MSMARCO, TREC deep learning and BEIR zero-shot document retrieval datasets illustrates that this simple prompt-based LLM retrieval method can achieve a similar or higher retrieval effectiveness than state-of-the-art LLM embedding methods that are trained with large amounts of unsupervised data, especially when using a larger LLM.

[Download paper here](https://arxiv.org/pdf/2404.18424)

[Code](https://github.com/ielab/PromptReps)
