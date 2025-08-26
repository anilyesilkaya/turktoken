---
layout: default
title: Yazarlar
permalink: /yazarlar/
lang: tr
---

<h1>Yazarlar</h1>

{%- comment -%}
Önce koleksiyon tanımlıysa (_config.yml -> collections.yazarlar) onu kullan.
Yoksa _data/yazarlar/*.json üzerinden sayfaları (author_slug eşleşmesiyle) bul.
Tüm durumlarda nil güvenli (nil-safe) olacak şekilde yazıldı.
{%- endcomment -%}

{%- assign coll = site.yazarlar -%}

{%- if coll -%}
  {%- assign authors = coll | sort_natural: "author" -%}
  <ul class="author-list">
  {%- for p in authors -%}
    {%- assign name = p.author | default: p.title -%}
    <li><a href="{{ p.url }}">{{ name }}</a></li>
  {%- endfor -%}
  </ul>
{%- else -%}
  {%- assign ydata = site.data.yazarlar -%}
  {%- if ydata -%}
    {%- assign slugs = ydata | keys | sort_natural -%}
    <ul class="author-list">
    {%- for slug in slugs -%}
      {%- assign rec   = ydata[slug] -%}
      {%- assign name  = rec.metadata.author | default: slug -%}
      {%- assign page_ = site.pages | where: "author_slug", slug | first -%}
      <li>
        {%- if page_ -%}
          <a href="{{ page_.url }}">{{ name }}</a>
        {%- else -%}
          {{ name }}
        {%- endif -%}
      </li>
    {%- endfor -%}
    </ul>
  {%- else -%}
    <p>Şimdilik listelenecek yazar bulunamadı. Lütfen <code>_config.yml</code> içinde
    <code>collections.yazarlar</code> tanımlayın veya <code>_data/yazarlar/*.json</code> ekleyin.</p>
  {%- endif -%}
{%- endif -%}
