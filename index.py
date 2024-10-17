from src.decodificador import DecodificadorRISCV
from src.arquivos import buscar_arquivos_hex_da_pasta

PASTA_DE_CODIGO_EM_HEX:str = ".\\code"

def main():
    try:
        for arquivo_hex_para_ser_lido in buscar_arquivos_hex_da_pasta(PASTA_DE_CODIGO_EM_HEX):
            print("="*100)
            print(f" Decodificando o código do arquivo \"{arquivo_hex_para_ser_lido}\" ".center(100,"|"))
            print("="*100)
            decodificador_risc_v = DecodificadorRISCV(f"{PASTA_DE_CODIGO_EM_HEX}\\{arquivo_hex_para_ser_lido}")
            decodificador_risc_v.classificar_instrucoes()
            decodificador_risc_v.resolver_conflitos()
            print("="*100)
            decodificador_risc_v.printar_instrucoes()
            print("="*100)
            decodificador_risc_v.printar_estatisticas()
            print("="*100)
            print("\n"*2)
    except Exception as e:
        print("="*100)
        print("  ERRO  ".center(100,"X"))
        print("="*100)
        print(f"Ocorreu um erro: {e}")
        print("="*100)


if __name__ == "__main__":
    main()