import pandas as pd

def calcular_digito(sku):
    """
    Calcula o dígito verificador do SKU usando a lógica do Módulo 11 do SAP.
    """
    # Extrai apenas os números para fazer a lógica matemática
    sku_str = str(sku).strip()
    sku_nums = [char for char in sku_str if char.isdigit()]
    
    if not sku_nums:
        return '0'
        
    # A lógica enviada do ABAP trabalhando com multiplicadores (10 - SY-INDEX) 
    # é matematicamente equivalente a aplicar pesos da direita para a esquerda,
    # começando com o peso 2 para o último dígito, peso 3 para o penúltimo, etc.
    soma = 0
    peso = 2
    
    for digit in reversed(sku_nums):
        soma += int(digit) * peso
        peso += 1
        
    # Operação final matemática exata do SAP ABAP:
    # DIGITO = ( 11 - ( AC MOD 11 ) ) MOD 10
    resto = soma % 11
    digito = (11 - resto) % 10
    
    return str(digito)

def processar_planilha(arquivo_entrada, arquivo_saida, nome_coluna_sku='SKU'):
    """
    Lê a planilha, calcula o dígito para cada SKU e salva um novo arquivo.
    """
    try:
        print(f"Lendo o arquivo: {arquivo_entrada}...")
        df = pd.read_excel(arquivo_entrada)
        
        if nome_coluna_sku not in df.columns:
            print(f"Erro: A coluna '{nome_coluna_sku}' não foi encontrada. Verifique o cabeçalho da planilha.")
            return

        # Aplica a função de cálculo e formata como SKU-Dígito (ex: 343456-7)
        # Limpamos espaços extras e removemos decimais caso o pandas leia como número
        def formatar_sku(valor):
            if pd.isna(valor):
                return valor
            # Se for lido como float (ex: 343456.0), converte para string ignorando o .0
            sku_limpo = str(valor).split('.')[0].strip()
            digito = calcular_digito(sku_limpo)
            return f"{sku_limpo}-{digito}"

        # Criar a nova coluna
        df['SKU_Processado'] = df[nome_coluna_sku].apply(formatar_sku)

        # Salvar o resultado
        df.to_excel(arquivo_saida, index=False)
        print(f"Sucesso! Arquivo salvo como: {arquivo_saida}")

    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    # Nomes dos arquivos de entrada e saída
    arquivo_origem = 'meus_skus.xlsx'
    arquivo_destino = 'skus_com_digitos.xlsx'
    
    print("Iniciando o script de automação de dígitos...")
    # Executa a função
    processar_planilha(arquivo_origem, arquivo_destino)
