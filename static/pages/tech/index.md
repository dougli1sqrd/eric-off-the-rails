---
layout: page
title: Off The Power Rails
permalink: /tech/
feature_image: "/assets/images/vgaterm-self-portrait-banner.jpg"
---
<ul>
{% for page in site.categories["tech"] %}
    <li class="item  item--post">
        <article class="article  article--post  typeset">
        <h3><a href="{{ site.baseurl }}{{ page.url }}">{{ page.title }}</a></h3>
        {% include post-meta.html %}
        {{ page.excerpt | truncatewords: 60 | markdownify }}
        </article>
    </li>
{% endfor %}
</ul>
