---
title: "Teaching Pre-Trained Language Models to Rank Effectively, Efficiently, and Robustly "
collection: publications
permalink: /publication/thesis
year: 2023
venue: 'The University of Queensland'
authors: <strong>Shengyao Zhuang</strong>.
track: Thesis
---
---

## Abstract
Search engines aim to provide users with a list of relevant documents (i.e., a ranking) from a vast corpus in response to their queries. To accomplish this, the ranking model serves as the core component that generates the ranking list. Traditional ranking models employ bag-of-words (BOW) models that estimate relevance signals between queries and documents based on exact term matching. Recently, pre-trained language models (PLMs) such as BERT have been shown to significantly improve ranking effectiveness due to their superior semantic relevance modelling ability compared to traditional BOW approaches. To further advance these PLM-based ranking models, this thesis proposes fundamental approaches across three critical aspects: effectiveness (produce accurate rankings), efficiency (have low query latency and index footprint), and robustness (be stable to noisy inputs). The aim is to enhance the models' ability to provide more accurate and relevant search results to users, without compromising their efficiency or robustness.

The first part of this thesis investigates the combination of PLMs with traditional BOW approaches based on query likelihood models (QLM). We demonstrate that incorporating PLMs can substantially improve the effectiveness of previous QLM ranking models. Building on this direction, we propose several PLM-based QLM ranking models that maximise efficiency while maintaining high effectiveness levels by modelling terms independently. Compared to existing PLM-based ranking models, our approaches are highly efficient as they do not require a GPU at query time and thus achieve low query latency with excellent effectiveness.

The second part of this thesis assesses and enhances the robustness of PLM-based ranking models. We first identify that current PLM-based models are highly sensitive to noise in user queries, such as misspelled words. To benchmark this issue, we contribute an evaluation framework and a real-world dataset. We then propose a series of methods to significantly improve model robustness, including a data augmentation-based fine-tuning approach, a modification of the backbone PLM model, and a bottleneck pre-training method.

The third part of this thesis focuses on leveraging augmentation signals to enrich the query and document representations for PLM-based ranking models. Specifically, we examine the use of implicit user feedback, such as clicks, and generated queries, as types of augmentation signals to augment query or document representations for dense retrievers and recently developed differentiable search index (DSI) models. Our simple yet effective methods do not increase query latency, and our results demonstrate that these techniques significantly enhance the effectiveness of these models, not only in English-only monolingual retrieval tasks but also in cross-lingual retrieval tasks (where queries and documents are not in the same language).

In summary, this thesis advances the understanding and application of PLM-based ranking models by exploring their effectiveness, efficiency, and robustness. We propose novel approaches that improve query likelihood models, address noise sensitivity, and leverage augmentation signals, resulting in enhanced performance across various retrieval tasks.

[Download my thesis here](https://espace.library.uq.edu.au/view/UQ:db0a1b9)
