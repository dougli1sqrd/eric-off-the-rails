---
layout: page
title: Contributors
permalink: /contributors/
---

<ul>
  {% for author in site.authors %}
    <li>
      <h4><a href="{{ author.url }}">{{ author.name }}</a></h4>
      <h5>{{ author.position }}</h5>
      <p>{{ author.content | markdownify }}</p>
    </li>
  {% endfor %}
</ul>
