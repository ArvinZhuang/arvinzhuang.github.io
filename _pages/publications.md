---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{%- assign publications = site.data.publications | group_by:"year" -%}
{% for year in publications %}
  <h2>{{ year.name }}</h2>
  <ul>
  {%- for pub in year.items -%}
    <li>
      {%- if pub.url -%}
        <a href="{{ pub.url }}">{{ pub.title }}</a>
      {%- else -%}
        {{ pub.title }}
      {%- endif -%}
      {%- if pub.venue != "" -%}
        <br /><small>{{ pub.venue }}</small>
      {%- endif -%}
      {%- if pub.authors != "" -%}
        <br /><small>{{ pub.authors }}</small>
      {%- endif -%}
    </li>
  {%- endfor -%}
  </ul>
{% endfor %}
