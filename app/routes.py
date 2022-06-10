from app import app
from flask import render_template, redirect, url_for, request
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from app.models.product import Product

def get_item(ancestor, selector, attribute=None, return_list=False):
    try:
        if return_list:
            pros = ancestor.select(selector)
            return [item.get_text().strip() for item in pros]
        if attribute:
            return ancestor.select_one(selector)[attribute]
        return ancestor.select_one(selector).get_text().strip()
    except (AttributeError, TypeError):
        return None

selectors = {
    'author': ["span.user-post__author-name"],
    'recommendation': ['span.user-post__author-recomendation > em'],
    'stars': ['span.user-post__score-count'],
    'content': ['div.user-post__text'],
    'useful': ['button.vote-yes > span'],
    'useless': ['button.vote-no > span'],
    'published': ['span.user-post__published > time:nth-child(1)', 'datetime'],
    'purchased': ['span.user-post__published > time:nth-child(2)', 'datetime'],
    'pros': ["div[class$=\"positives\"] ~ div.review-feature__item", None, True],
    'cons': ["div[class$=\"negatives\"] ~ div.review-feature__item", None, True]
}

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/extract', methods=["POST", "GET"])
def extract():
    if not request.method == 'POST':
        product_id = request.form.get('product_id')
        product = Product(product_id)
        product.extract_name()
        if product.procuct_name:
            product.extract_opinion()
        else:
            pass

        if not os.dir.exists('app/opinions'):
            os.makedirs('app/opinions')
        with open(f'app/opinions/{product_id}.json', 'w', encoding='UTF-8') as file:
            json.dump(all_opinions, file, indent=4, ensure_ascii=False)
        return redirect (url_for('product', product_id=product_id))
        
@app.route('/products')
def products():
    products = [filename.split('.')[0] for filename in os.listdir('app/opinions')]
    return render_template('products.html.jinja', products=products)

@app.route('/author')
def author():
    return render_template('author.html.jinja')

@app.route('/product/<product_id>')
def product(product_id):   
    return render_template('product.html.jinja', product_id=product_id, stats=stats, opinions=opinions)