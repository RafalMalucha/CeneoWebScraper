from bs4 import BeautifulSoup
import bs4
import requests
from app.models.opinion import Opinion
from app.utils import get_item
import os
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from app.models.product import Product
import json

class Product():
    def __init__(self, product_id, product_name='', opinions=[], opinions_count=0, 
    pros=[], cons=[], average_scroce=0):
        self.procuct_id = product_id
        self.procuct_name = product_name
        self.opinions = opinions
        self.opinions_count = opinions_count
        self.pros = pros
        self.cons = cons
        self.average_score = average_scroce

    def extract_name(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        response = requests.get(url)
        page = BeautifulSoup(response.text, 'html.parser')
        self.product_name = get_item(page,'h1.product-top__product-info__name')
        return self

    def extract_opinions(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab=reviews"
        while(url):    
            response = requests.get(url)
            page = BeautifulSoup(response.text, 'html.parser')
            opinions = page.select('div.js_product-review')
            for opinion in opinions:
                single_opinion = Opinion().extract_opinion(opinion)
                self.opinions.append(single_opinion)
            try:
                url = 'https://www.ceneo.pl'+get_item('a.pagination__next')['href']
            except TypeError:
                url = None
        return self

    def calculate_stats(self):
        opinions = pd.read_json('app/opinions/'+self.product_id+'.json')
        opinions['stars'] = opinions['stars'].map(lambda x: float(x.split('/')[0].replace(',', '.')))

        stats = {
            'opinions_count': len(opinions),
            'pros_count': opinions['pros'].map(bool).sum(),
            'cons_count': opinions['cons'].map(bool).sum(),
            'average_score': opinions['stars'].mean().round(2)
        }    
        if not os.path.exists('app/plots'):
            os.makedirs('app/plots')
        recommendation = opinions['recommendation'].value_counts(dropna=False).sort_index().reindex(['Nie polecam', 'Polecam', None], fill_value=0)
        recommendation.plot.pie(
            label='',
            autopct=lambda p: '{:.1f}%'.format(round(p)) if p > 0 else '',
            colors=['crimson', 'forestgreen', 'lightskyblue'],
            labels=['Nie polecam', 'Polecam', 'Nie mam zdania']
        )
        plt.title('Rekomendacje')
        plt.savefig(f'app/plots/{self.product_id}_recommendations.png')
        plt.close()

        stars = opinions['stars'].value_counts().sort_index().reindex(list(np.arange(0,5.5,0.5)), fill_value=0)
        stars.plot.bar(
            color='red'
        )
        plt.title('Oceny produktu')
        plt.xlabel('Liczba gwiazdek')
        plt.ylabel('Liczba opinii')
        plt.grid(True, axis='y')
        plt.xticks(rotation=0)
        plt.savefig(f'app/plots/{self.product_id}_stars.png')
        plt.close()

    def __str__(self) -> str:
        pass

    def __repr__(self) -> :
        pass

    def to_dict(self):
        pass

    def export_opinions(self):
        if not os.path.exists('app/opinions'):
            os.makedirs('app/opinions')
        with open(f'app/opinions/{self.procuct_id}.json', 'w', encoding='UTF-8') as file:
            json.dump([opinion.to_dict for opinion in self.opinions()], file, indent=4, ensure_ascii=False)
        pass

    def export_product(self):
        pass