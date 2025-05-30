import re
from playwright.async_api import async_playwright
import pandas as pd
from src.service.transaction import get_field_value

async def get_verified_text(page, main_selector, verification_text=None, parent_level=1):
    try:
       
        locator = page.locator(main_selector).first
        if not await locator.count():
            return None
            
      
        if verification_text:
            parent = locator
            for _ in range(parent_level):
                parent = parent.locator("xpath=..")
            
            parent_text = await parent.text_content()
            if verification_text not in parent_text:
                return None
        
        return (await locator.text_content()).strip()
    except:
        return None


async def run_urls(urls):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        all_data = []

        for url in urls:
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")
            
            try:
             
                lote = await page.locator("xpath=//*[@id='content']/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div[3]/h1").text_content()
                
             
                km_locator = page.locator("text=KM >> xpath=..")
                km_element = await km_locator.text_content()
                km = km_element.replace("KM", "").strip() if km_element else None
           
                origem = await get_field_value(page,'origem')
                
                
           
                monta = await get_field_value(page, "Monta")
                
            
                obs = await get_verified_text(
                    page,
                    "text=Observações >> xpath=following::p[1]",
                    "Observações"
                ) or await get_verified_text(
                    page,
                    "text=Obs. >> xpath=following::p[1]",
                    "Obs."
                )
                
             
                lance_atual = None
                bid_boxes = [
                    "div[style*='background-color: rgb(0, 129, 119)']",
                    "div.lance-box",
                    "div.current-bid"
                ]
                
                for box_selector in bid_boxes:
                    if lance_atual:
                        break
                    
                    box = page.locator(box_selector)
                    if await box.count():
                        box_text = await box.text_content()
                        if any(x in box_text.lower() for x in ["lance atual", "lance inicial"]):
                            match = re.search(r'R\$\s*([\d\.,]+)', box_text)
                            if match:
                                lance_atual = match.group(1)
                
                all_data.append({
                    'Lote': lote,
                    'KM': km,
                    'Origem': origem,
                    'Monta': monta,
                    'Obs': obs,
                    'Lance Atual': lance_atual,
                    'url': url
                })
                
            except Exception as e:
                print(f"Erro ao processar {url}: {str(e)}")
                continue

        df = pd.DataFrame(all_data)
        df.to_excel('dados_seguros.xlsx', index=False)

        await browser.close()

# Exemplo de uso
#asyncio.run(run_urls(["https://www.pestanaleiloes.com.br/agenda-de-leiloes/5038/365422"]))