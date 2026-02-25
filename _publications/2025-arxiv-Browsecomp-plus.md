---
title: "Browsecomp-plus: A more fair and transparent evaluation benchmark of deep-research agent"
collection: publications
permalink: /publication/arxiv2025Browsecomp-plus
year: 2025
venue: 'arXiv preprint arXiv:2508.06600'
authors: Zijian Chen*, Xueguang Ma*, <strong>Shengyao Zhuang</strong>*, Ping Nie, Kai Zou, Andrew Liu, Joshua Green, Kshama Patel, Ruoxi Meng, Mingyi Su, Sahel Sharifymoghaddam, Yanxi Li, Haoran Hong, Xinyu Shi, Xuye Liu, Nandan Thakur, Crystina Zhang, Luyu Gao, Wenhu Chen, Jimmy Lin
track: Full paper
---
---

## Abstract
Deep-Research agents, which integrate large language models (LLMs) with search tools, have shown success in improving the effectiveness of handling complex queries that require iterative search planning and reasoning over search results. Evaluations on current benchmarks like BrowseComp relies on black-box live web search APIs, have notable limitations in (1) fairness: dynamic and opaque web APIs hinder fair comparisons and reproducibility of deep research methods; (2) transparency: lack of control over the document corpus makes it difficult to isolate retriever contributions. In other words, the current evaluations may compare a complete deep research system at a given time, but they do not foster well-controlled experiments to provide insights into the capability of underlying deep research LLMs. To address these challenges, we introduce BrowseComp-Plus, a benchmark derived from BrowseComp, employing a fixed, carefully curated corpus. Each query in BrowseComp-Plus includes human-verified supporting documents and mined challenging negatives, enabling controlled experimentation. The benchmark is shown to be effective in distinguishing the performance of deep research systems. For instance, the open-source model Search-R1, when paired with the BM25 retriever, achieves 3.86% accuracy, whereas the GPT-5 achieves 55.9%. Integrating the GPT-5 with the Qwen3-Embedding-8B retriever further enhances its accuracy to 70.1% with fewer search calls. This benchmark allows comprehensive evaluation and disentangled analysis of deep research agents and retrieval methods, fostering insights into retrieval …

[Download paper here](https://arxiv.org/abs/2508.06600)
