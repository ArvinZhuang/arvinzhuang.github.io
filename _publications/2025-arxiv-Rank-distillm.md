---
title: "Rank-distillm: Closing the effectiveness gap between cross-encoders and llms for passage re-ranking"
collection: publications
permalink: /publication/arxiv2025Rank-distillm
year: 2025
venue: 'Preprint'
authors: Ferdinand Schlatt, Maik Fröbe, Harrisen Scells, <strong>Shengyao Zhuang</strong>, Bevan Koopman, Guido Zuccon, Benno Stein, Martin Potthast, Matthias Hagen
track: Full paper
---
---

## Abstract
Cross-encoders distilled from large language models (LLMs) are often more effective re-rankers than cross-encoders fine-tuned on manually labeled data. However, distilled models do not match the effectiveness of their teacher LLMs. We hypothesize that this effectiveness gap is due to the fact that previous work has not applied the best-suited methods for fine-tuning cross-encoders on manually labeled data (e.g., hard-negative sampling, deep sampling, and listwise loss functions). To close this gap, we create a new dataset, Rank-DistiLLM. Cross-encoders trained on Rank-DistiLLM achieve the effectiveness of LLMs while being up to 173 times faster and 24 times more memory efficient. Our code and data is available at https://github.com/webis-de/ECIR-25.

[Download paper here](https://link.springer.com/chapter/10.1007/978-3-031-88714-7_31)
