---
title: "Rank-r1: Enhancing reasoning in llm-based document rerankers via reinforcement learning"
collection: publications
permalink: /publication/arxiv2025Rank-r1
year: 2025
venue: 'arXiv preprint arXiv:2503.06034'
authors: <strong>Shengyao Zhuang</strong>, Xueguang Ma, Bevan Koopman, Jimmy Lin, Guido Zuccon
track: Full paper
---
---

## Abstract
In this paper, we introduce Rank-R1, a novel LLM-based reranker that performs reasoning over both the user query and candidate documents before performing the ranking task. Existing document reranking methods based on large language models (LLMs) typically rely on prompting or fine-tuning LLMs to order or label candidate documents according to their relevance to a query. For Rank-R1, we use a reinforcement learning algorithm along with only a small set of relevance labels (without any reasoning supervision) to enhance the reasoning ability of LLM-based rerankers. Our hypothesis is that adding reasoning capabilities to the rerankers can improve their relevance assessement and ranking capabilities. Our experiments on the TREC DL and BRIGHT datasets show that Rank-R1 is highly effective, especially for complex queries. In particular, we find that Rank-R1 achieves effectiveness on in-domain datasets at par with that of supervised fine-tuning methods, but utilizing only 18\% of the training data used by the fine-tuning methods. We also find that the model largely outperforms zero-shot and supervised fine-tuning when applied to out-of-domain datasets featuring complex queries, especially when a 14B-size model is used. Finally, we qualitatively observe that Rank-R1's reasoning process improves the explainability of the ranking results, opening new opportunities for search engine results presentation and fruition.

[Download paper here](https://arxiv.org/abs/2503.06034)
