---
permalink: /
title: "Shengyao (Arvin) Zhuang 庄胜尧"
excerpt: "About me"
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---
I am an Applied Scientist at Amazon’s AGI group, specializing in advancing web search technologies that power Amazon’s product ecosystem. My research focuses on information retrieval, large language model–based neural rankers, and natural language processing. Previously, I was a Postdoctoral Researcher at CSIRO’s Australian e-Health Research Centre, where I developed LLM-driven search systems for the medical domain. I earned my Ph.D. in Computer Science from the University of Queensland’s ielab, under the supervision of Professor Guido Zuccon.
<hr>

{% include base_path %}
{%- assign publications = site.publications | sort:"year" | reverse | group_by:"year" -%}

<h1>Publications</h1>
{% for year in publications %}
  <h2>{{ year.name }}</h2>
  <ul>
  {%- for post in year.items -%}
    {% include archive-single.html %}
  {%- endfor -%}
 </ul>
{% endfor %}

