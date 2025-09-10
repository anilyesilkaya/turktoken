---
layout: default
title: Yazarlar
permalink: /yazarlar/
lang: tr
---

<h1>Yazarlar</h1>

{%- assign coll = site.yazarlar -%}

{%- if coll -%}
  {%- assign authors = coll | sort_natural: "author" -%}
  <div class="author-grid">
  {%- for p in authors -%}
    {%- assign name = p.author | default: p.title -%}
    {%- assign slug = p.author_slug | default: p.slug | default: name | slugify -%}
    {%- assign default_img = '/assets/img/yazarlar/' | append: slug | append: '.png' -%}
    {%- assign img = p.image | default: p.author_image | default: default_img -%}
    <a class="author-card" href="{{ p.url | relative_url }}">
      <div class="author-thumb">
        <img src="{{ img | relative_url }}" alt="{{ name }}" loading="lazy"
             onerror="this.closest('.author-thumb').classList.add('no-image'); this.remove();">
        <div class="thumb-fallback"><i class="fas fa-user"></i></div>
      </div>
      <div class="author-meta">
        <span class="author-name">{{ name }}</span>
        <i class="fas fa-arrow-right author-arrow" aria-hidden="true"></i>
      </div>
    </a>
  {%- endfor -%}
  </div>
{%- else -%}
  {%- assign ydata = site.data.yazarlar -%}
  {%- if ydata -%}
    {%- assign slugs = ydata | keys | sort_natural -%}
    <div class="author-grid">
    {%- for slug in slugs -%}
      {%- assign rec   = ydata[slug] -%}
      {%- assign name  = rec.metadata.author | default: slug -%}
      {%- assign default_img = '/assets/img/yazarlar/' | append: slug | append: '.png' -%}
      {%- assign page_ = site.pages | where: "author_slug", slug | first -%}
      {%- if page_ -%}
        <a class="author-card" href="{{ page_.url | relative_url }}">
      {%- else -%}
        <div class="author-card author-card--disabled" tabindex="-1" title="Sayfa yakında">
      {%- endif -%}
          <div class="author-thumb">
            <img src="{{ default_img | relative_url }}" alt="{{ name }}" loading="lazy"
                 onerror="this.closest('.author-thumb').classList.add('no-image'); this.remove();">
            <div class="thumb-fallback"><i class="fas fa-user"></i></div>
          </div>
          <div class="author-meta">
            <span class="author-name">{{ name }}</span>
            <i class="fas fa-arrow-right author-arrow" aria-hidden="true"></i>
          </div>
      {%- if page_ -%}
        </a>
      {%- else -%}
        </div>
      {%- endif -%}
    {%- endfor -%}
    </div>
  {%- else -%}
    <p>Şimdilik listelenecek yazar bulunamadı. Lütfen <code>_config.yml</code> içinde
    <code>collections.yazarlar</code> tanımlayın veya <code>_data/yazarlar/*.json</code> ekleyin.</p>
  {%- endif -%}
{%- endif -%}
