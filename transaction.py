import pandas as pd
import json
import re
async def get_field_value(page, field_name):
    """
    Pega o valor de um campo específico mesmo quando existem múltiplos elementos similares
    field_name: "Monta", "Origem", "KM", etc. (inclui automaticamente os ":")
    """
    try:
        # Primeiro tentamos pegar o elemento PAI que contém tanto o label quanto o valor
        parent_locator = page.locator(f"text=/{field_name}:/i >> xpath=..")
        
        if await parent_locator.count() > 0:
            # Pega todo o texto do elemento pai e extrai apenas o valor
            full_text = await parent_locator.first.text_content()
            value = full_text.split(f"{field_name}:")[-1].strip()
            return value if value else None
        
        # Fallback: procura pelo texto exato e pega o próximo elemento
        label_locator = page.locator(f"text=/{field_name}:/i").first
        if await label_locator.count() > 0:
            value_locator = label_locator.locator("xpath=following-sibling::*[1]")
            if await value_locator.count() > 0:
                return await value_locator.text_content()
        
        return None
    except Exception as e:
        print(f"Erro ao extrair {field_name}: {str(e)}")
        return None
    
    

def fetch_data_fipe(lines):
    with open("fipe/marks.json", "r") as f:
        json_marcas = json.load(f)

    # Cria um dicionário com nome -> código
    dict_marks = {marca["nome"].lower(): marca["codigo"] for marca in json_marcas}

    result = []

    for line in lines:
        if pd.isna(line):
            result.append(None)
            continue

        line_lower = str(line).lower()
        parts = line_lower.split()
        marca = None
        modelo = None
        ano = None

        if parts:
            # Pega a primeira palavra após remover o prefixo '-'
            first_word = parts[0].lstrip('-')
            if first_word == "chevrolet":
                first_word = "gm - chevrolet"
            if first_word == "volkswagen":
                first_word = "vw - volkswagen"    
            if first_word in dict_marks:
                marca = first_word
                remaining_parts = parts[1:] # O resto são modelo e ano
            # Adiciona uma lógica para tentar encontrar marcas de duas palavras
            elif len(parts) > 1:
                potential_mark_two_words = " ".join(parts[:2]).lstrip('-')
                if potential_mark_two_words in dict_marks:
                    marca = potential_mark_two_words
                    remaining_parts = parts[2:]
                else:
                    remaining_parts = parts[1:] # Se não for marca de duas palavras, o resto começa da segunda palavra
            else:
                remaining_parts = []

            if marca:
                # Tenta encontrar o modelo e ano no restante das partes
                ano_pattern = re.compile(r'\b(20\d{2})\b')
                anos_encontrados = ano_pattern.findall(" ".join(remaining_parts))

                if anos_encontrados:
                    ano = anos_encontrados[0]
                    modelo_parts = [part for part in remaining_parts if part not in anos_encontrados]
                    modelo = " ".join(modelo_parts).strip()
                else:
                    modelo = " ".join(remaining_parts).strip()
            if not (marca and modelo and ano):
                pass

        result.append({"marca": marca, "modelo": modelo, "ano": ano})

    return result



async def get_fipe_codes(vehicles):
    with open("fipe/marks.json", "r", encoding='windows-1252') as f_marks:
        marks_data = json.load(f_marks)
        marks_dict = {mark["nome"].lower(): mark["codigo"] for mark in marks_data}

    with open("fipe/models.json", "r", encoding='utf-8') as f_models:
        models_data = json.load(f_models)

    fipe_requests = []
    for vehicle in vehicles:
        marca_nome = vehicle.get("marca")
        modelo_nome = vehicle.get("modelo")
        ano_str = vehicle.get("ano")

        marca_codigo = None
        modelo_codigo = None
        ano_codigo = None

        if marca_nome:
            marca_codigo = marks_dict.get(marca_nome.lower())

        if marca_codigo:
            marca_info = models_data.get(str(marca_codigo))
            if marca_info:
                modelos = marca_info.get("modelos", [])
                modelo_nome_lower_parts = set(re.findall(r'\w+', modelo_nome.lower()))
                melhor_match_codigo = None
                maior_overlap = 0

                for modelo_fipe in modelos:
                    nome_fipe_lower_parts = set(re.findall(r'\w+', modelo_fipe.get("nome", "").lower()))
                    overlap = len(modelo_nome_lower_parts.intersection(nome_fipe_lower_parts))

                    if overlap > maior_overlap and overlap > 0:
                        maior_overlap = overlap
                        melhor_match_codigo = modelo_fipe.get("codigo")

                modelo_codigo = melhor_match_codigo

                # Busca pelo código do ano
                anos = marca_info.get("anos", [])
                for ano_info in anos:
                    ano_nome_parts = ano_info.get("nome", "").split()
                    if ano_nome_parts and ano_str == ano_nome_parts[0]:
                        ano_codigo = ano_info.get("codigo")
                        break

        if marca_codigo and modelo_codigo and ano_codigo:
            fipe_requests.append({
                "codigoMarca": marca_codigo,
                "codigoModelo": modelo_codigo,
                "anoModelo": ano_codigo
            })
        else:
            print(f"Não foi possível encontrar códigos para: {vehicle}")

    return fipe_requests


async def get_payloead(data):
    vehicles =  fetch_data_fipe(data)
    payloads = await get_fipe_codes(vehicles)
    return payloads
