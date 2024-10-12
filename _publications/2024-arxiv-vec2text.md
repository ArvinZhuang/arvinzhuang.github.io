---
title: "Understanding and Mitigating the Threat of Vec2Text to Dense Retrieval Systems"
collection: publications
permalink: /publication/sigirap2024vec2text
year: 2024
venue: 'Proceedings of the 2st International ACM SIGIR Conference on Information Retrieval in the Asia Pacific (SIGIR-AP ’24), 2024'
authors: <strong>Shengyao Zhuang</strong>, Bevan Koopman, Xiaoran Chu, and Guido Zuccon.
track: Full paper
---
---

## Abstract
The emergence of Vec2Text --- a method for text embedding inversion --- has raised serious privacy concerns for dense retrieval systems which use text embeddings, such as those offered by OpenAI and Cohere. This threat comes from the ability for a malicious attacker with access to  embeddings to  reconstruct the original text.
In this paper, we investigate various factors related to embedding models that may impact text recoverability via Vec2Text. We explore factors such as distance metrics, pooling functions, bottleneck pre-training, training with noise addition, embedding quantization, and embedding dimensions, which were not considered in the original Vec2Text paper. Through a comprehensive analysis of these factors, our objective is to gain a deeper understanding of the key elements that affect the trade-offs between the text recoverability and retrieval effectiveness of dense retrieval systems, offering insights for practitioners designing privacy-aware dense retrieval systems. We also propose a simple embedding transformation fix that guarantees equal ranking effectiveness while mitigating the recoverability risk.
Overall, this study reveals that Vec2Text could pose a threat to current dense retrieval systems, but there are some effective methods to patch such systems.


[Download paper here](https://arxiv.org/pdf/2402.12784.pdf)

[Code](https://github.com/ielab/vec2text-dense_retriever-threat)
