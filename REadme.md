# Projeto LeilãoScraper

Automação para captura e análise de dados de veículos em leilões online, incluindo valores da tabela FIPE, para facilitar a avaliação de margens de desconto e oportunidades de compra.

Site que esta sendo raspado:
https://www.pestanaleiloes.com.br/

---

## Sobre

Este projeto tem como objetivo coletar dados de um site de leilões de veículos, fazendo *scraping* das informações relevantes dos carros disponíveis. Além disso, a automação será estendida para buscar os valores da tabela FIPE correspondentes a cada veículo, permitindo montar uma tabela consolidada com dados importantes para análise de preços, descontos e tendências do mercado.

---

## Funcionalidades

- Extração automática de informações de veículos em leilões (modelo, ano, lance, monta, origem,, url etc).
- Integração futura com dados da tabela FIPE para comparação de preços.
- Cálculo e análise de margem de desconto em relação ao valor de mercado.
- Geração de relatórios e tabelas com dados consolidados para apoio à decisão.

---

## Tecnologias

- Python 3.x
- Bibliotecas: `requests`, `playwright`, `pandas` (e outras para scraping e análise)


---

## Como usar

1. Clone este repositório:

   ```bash
   git clone git@github.com:seu-usuario/leilaoscraper.git
   cd leilaoscraper

2. Intale requirements.txt (use playwright install  para atualizar browsers)


3. Execute o Runner, capture as urls de cada lote e depois processe o txt gerado para capturar os dados de cada lote capturado
