---
layout: default
title: "Yazarlar"
permalink: /yazarlar/
---

<h1>Yazarlar</h1>
<ul class="author-list">
{% assign keys = site.data.authors | keys | sort %}
{% for k in keys %}
  {% assign a = site.data.authors[k] %}
  <li>
    <a href="{{ '/yazar/' | append: k | append: '/' | relative_url }}">
      {{ a.metadata.author | default: k }}
    </a>
    <small> ({{ a.metadata.titles | size }} kitap)</small>
  </li>
{% endfor %}
</ul>
