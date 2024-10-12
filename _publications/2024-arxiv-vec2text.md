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
The introduction of Vec2Text, a technique for inverting text embeddings, has raised serious privacy concerns within dense retrieval systems utilizing text embeddings, including those provided by OpenAI and Cohere. This threat comes from the ability for a malicious attacker with access to text embeddings to reconstruct the original text.
In this paper, we investigate various aspects of embedding models that could influence the recoverability of text using Vec2Text. Our exploration involves factors such as distance metrics, pooling functions, bottleneck pre-training, training with noise addition, embedding quantization, and embedding dimensions -- aspects not previously addressed in the original Vec2Text paper. Through a thorough analysis of these factors, our aim is to gain a deeper understanding of the critical elements impacting the trade-offs between text recoverability and retrieval effectiveness in dense retrieval systems. This analysis provides valuable insights for practitioners involved in designing privacy-aware dense retrieval systems. Additionally, we propose a straightforward fix for embedding transformation that ensures equal ranking effectiveness while mitigating the risk of text recoverability.
Furthermore, we extend the application of Vec2Text to the separate task of corpus poisoning, where, theoretically, Vec2Text presents a more potent threat compared to previous attack methods. Notably, Vec2Text does not require access to the dense retriever's model parameters and can efficiently generate numerous adversarial passages.
In summary, this study highlights the potential threat posed by Vec2Text to existing dense retrieval systems, while also presenting effective methods to patch and strengthen such systems against such risks.

[Download paper here](https://arxiv.org/pdf/2402.12784.pdf)

[Code](https://github.com/ielab/vec2text-dense_retriever-threat)
