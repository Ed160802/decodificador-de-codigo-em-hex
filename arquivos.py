import os

def buscar_arquivos_hex_da_pasta(pasta_com_o_codigo:str):
    arquivos_no_diretorio = os.listdir(pasta_com_o_codigo)
    return [arquivo for arquivo in arquivos_no_diretorio if arquivo.endswith(".hex") ]