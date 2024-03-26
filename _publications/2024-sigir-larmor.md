---
title: "Leveraging LLMs for Unsupervised Dense Retriever Ranking"
collection: publications
permalink: /publication/sigir2024larmor
year: 2024
venue: 'Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval (SIGIR ’24)'
authors: Ekaterina Khramtsova, <strong>Shengyao Zhuang</strong>, Mahsa Baktashmotlagh, and Guido Zuccon
track: Full paper
---
---

## Abstract
This paper introduces a novel unsupervised technique that utilizes large language models (LLMs) to determine the most suitable dense retriever for a specific test(target) corpus. Selecting the appropriate dense retriever is vital for numerous IR applications that employ these retrievers, trained on public datasets, to encode or conduct searches within a new private target corpus. The effectiveness of a dense retriever can significantly diminish when applied to a target corpus that diverges in domain or task from the original training set. The problem becomes more pronounced in cases where the target corpus is unlabeled, e.g. in zero-shot scenarios, rendering direct evaluation of the model's effectiveness on the target corpus unattainable. Therefore, the unsupervised selection of an optimally pre-trained dense retriever, especially under conditions of domain shift, emerges as a critical challenge. Existing methodologies for ranking dense retrievers fall short in addressing these domain shift scenarios.
To tackle this, our method capitalizes on LLMs to create pseudo-relevant queries, labels, and reference lists by analyzing a subset of documents from the target corpus. This allows for the ranking of dense retrievers based on their performance with these pseudo-relevant signals. Significantly, this strategy is the first to depend exclusively on the target corpus data, removing the necessity for training data and test labels. We assessed the effectiveness of our approach by compiling a comprehensive pool of cutting-edge dense retrievers and comparing our method against traditional dense retriever selection benchmarks. The findings reveal that our proposed solution surpasses the existing benchmarks in both the selection and ranking of dense retrievers.

[Download paper here](https://arxiv.org/pdf/2402.04853.pdf)

[Code (available soon)](https://github.com/ielab/larmor)
