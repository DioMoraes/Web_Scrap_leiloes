import requests
import json
import logging
import os
import time

api_url_base = 'https://parallelum.com.br/fipe/api/v1/carros/marcas'
api_url_mark = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/{}'
api_url_model = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/{}/modelos'
api_url_year = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/{}/modelos/{}/anos/{}'
# api_url_ = 'https://parallelum.com.br/fipe/api/v1/carros/marcas/{}/modelos/{}/anos/{}/veiculos'


def get_fipe_data(mark, model, year):
    response = requests.get(api_url_year.format(mark, model, year))
    return response

def get_marks():
    try:
        response = requests.get(api_url_base)
        data = response.json()
    except Exception as e:
        logging.error(e)
    
    with open('marks.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_models(marks_json):
    
    all_marks = []
    
    
    with open(marks_json, 'r') as f:
        json_data = json.load(f)
        
        for item in json_data:
            all_marks.append(item['codigo'])
    
    all_models = {} 

    for mark in all_marks:
        try:
            url = api_url_model.format(mark)
            response = requests.get(url)
            data = response.json()
            all_models[mark] = data  
        except Exception as e:
            logging.error(f"Erro ao buscar modelos para a marca {mark}: {e}")

    with open('models.json', 'w', encoding='utf-8') as f:
        json.dump(all_models, f, indent=4, ensure_ascii=False)
        
        
def get_fipe_value(mark, model, year):
    url = api_url_year.format(mark, model, year)
    response = requests.get(url)
    data = response.json()
    return data


#get_models(os.path.join(os.path.dirname(__file__ ), 'marks.json'))