<center>
    <h1>Decodificador de Código HEX</h1>
</center>

**Autor: Eduardo de Oliveira Duarte**
<br/>
**Versão: 1.0.0**

## Descrição
Descodificador de códigos em hexadecimal.


## Como Instalar
- Ter o Python instalado.
- Criar um ambiente virtual `venv`
- Instalar os pacotes dentro de `requirements.txt`
- Colocar os arquivos `.hex` na pasta `code` dentro da pasta do projeto ou alterar o caminho na constante `PASTA_DE_CODIGO_EM_HEX`
    - A pasta já possui algum arquivos de exemplo;
        - `big-big.hex`
        - `codigo2.hex`
        - `codigo.hex`
- Rodar o arquivo `index.py`
- Exemplo de saida:
```txt
====================================================================================================
|||||||||||||||||||||||||| Decodificando o código do arquivo "codigo.hex" ||||||||||||||||||||||||||
====================================================================================================
====================================================================================================
Formato = I, rd = 2, f3 = 0, rs1 = 0, imed = 5
Formato = I, rd = 0, f3 = 0, rs1 = 0, imed = 0
Formato = R, rd = 2, f3 = 0, rs1 = 1, rs2 = 2, f7 = 0
Formato = J, rd = 0, imed = 0
Formato = I, rd = 0, f3 = 0, rs1 = 0, imed = 0
Formato = B, f3 = 0, rs1 = 0, rs2 = 0, imed = 8174
Formato = I, rd = 4, f3 = 2, rs1 = 2, imed = 0
Formato = I, rd = 0, f3 = 0, rs1 = 0, imed = 0
Formato = S, f3 = 2, rs1 = 2, rs2 = 4, imed = 0
Formato = I, rd = 0, f3 = 0, rs1 = 0, imed = 0
Formato = U, rd = 5, imed = 0
====================================================================================================
Estatísticas: {'total': 7, 'alu': 8, 'jump': 2, 'branch': 2, 'memory': 4, 'other': 2, 'nops_inseridos': 4}
====================================================================================================
```
