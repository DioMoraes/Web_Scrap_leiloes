import google.generativeai as genai
import os


api_key = os.environ.get("GEMINI_API_KEY")

model = 'gemini-1.5-flash-8b-001'
# model = "gemini-2.0-flash"
# model = "gemini-2.5-pro-exp-03-25"
#model = "gemini-2.5-flash-preview-04-17"

def gemini(prompt, file_name, model= model,  temperature=0.0, max_token = 2000):
    
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model)
    
    
    try:
        response = model.generate_content(prompt, generation_config={
            "temperature": temperature,
            "max_output_tokens": max_token
        })
        
        total_token_count = response.usage_metadata.total_token_count

        with open("/tmp/ts/contagem_tokens.txt", 'a') as f:
            f.write(f"\nArquivo: {os.path.basename(file_name)}, Tokens: {total_token_count}")
        
        return response.text.strip()
    
    except Exception as e:
        return f"Erro: {str(e)}"
    
    
def genai_upload(prompt, file_path, model= model, temperature=0.0, max_token = 2000, top_k=1, top_p=0.1):
    """ use genai to upload file to read. args: prompt, file path to upload
       
       Args:
        prompt
        file_path
        model
        temperature
        max_token
        top_k
        top_p

    """
    
    genai.configure(api_key=api_key)
    try:
        file =  genai.upload_file(path=file_path)
        
        
        model_genai = genai.GenerativeModel(model, generation_config={
            "temperature": temperature,
            "max_output_tokens": max_token,
            "top_k": top_k, 
            "top_p": top_p,
        })
        response = model_genai.generate_content(contents=[file, prompt, ])
        total_token_count = response.usage_metadata.total_token_count

        with open("/tmp/ts/contagem_tokens.txt", 'a') as file:
            file.write(f"\nArquivo: {os.path.basename(file_path)}, Tokens: {total_token_count}")
    
        return response.text.strip()
    except Exception as e:
        return f"Erro: Gemini Upload {str(e)}"
    
