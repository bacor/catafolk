---
layout: default
title: Datasets
excerpt: >
  A list of all datasets in Catafolk
---

<main class="container mt-5">
  <div class="jumbotron row">
    <div class="w-100">
      <h1 class="display-4">{{ page.title }}</h1>
      {% if page.excerpt %}
      <p class="lead w-75">
          {{ page.excerpt }}
      </p>
      {% endif %}
    </div>
  </div>

  <div class="row mt-5">
    <div class="card w-100">
      <div class="card-header">
        Analyzed datasets
      </div>
      <div class="card-body">
        {% assign datasets = site.datasets | where: "analyzed", true %}
        <table class="table table-responsive-md table-hover">
        <thead>
            <tr>
            <th scope="col" class="border-top-0">id</th>
            <th scope="col" class="border-top-0">name</th>
            <th scope="col">region</th>
            <th scope="col">date</th>
            <th scope="col">pieces</th>
            <th scope="col">symb</th>
            <th scope="col">audio</th>
            <th scope="col">url</th>
            </tr>
        </thead>
        <tbody>
            {% for dataset in datasets %}
            {% assign analysis = site.data[dataset.dataset_id] %}
            <tr>
            <th scope="row">
                <a href="{{ site.baseurl }}{{ dataset.url }}">{{ dataset.dataset_id }}</a>
            </th>
            <td>{{ dataset.name }}</td>
            <td>{{ dataset.region }}</td>
            <td>{{ dataset.release_date }}</td>
            <td>{{ dataset.pieces }}</td>
            <td>{% if dataset.types contains 'symbolic' %}yes{% endif %}</td>
            <td>{% if dataset.types contains 'audio' %}yes{% endif %}</td>
            <td>{% if dataset.dataset_url %}<a href="{{ dataset.dataset_url }}" target="_blank">url</a>{% endif %}</td>
            </tr>
            {% endfor %}
        </tbody>
        </table>
      </div>
    </div>
  </div>
</main>
