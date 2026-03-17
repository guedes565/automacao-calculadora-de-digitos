import os
import pandas as pd
from calculadora_sku import calcular_digito

def processar_lista_para_excel(arquivo_entrada='skus.txt', arquivo_saida='meus_skus.xlsx'):
    # Verifica se o arquivo existe
    if not os.path.exists(arquivo_entrada):
        print(f"O arquivo {arquivo_entrada} não foi encontrado.")
        return

    print(f"Lendo SKUs de {arquivo_entrada}...")
    
    dados = []
    
    # Lendo o arquivo TXT
    with open(arquivo_entrada, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
        
    for linha in linhas:
        sku = linha.strip()  # Remove espaços invisíveis e quebras de linha
        if sku: # Se a linha não estiver vazia
            digito = calcular_digito(sku)
            resultado = f"{sku}-{digito}"
            dados.append({
                'SKU_Original': sku,
                'Digito_Calculado': digito,
                'SKU_Mapeado': resultado
            })
            print(f"Processado: {resultado}")
            
    # Salvando no arquivo de saída Excel
    if dados:
        # Cria um DataFrame do pandas com as colunas organizadas
        df = pd.DataFrame(dados)
        
        # Salva o resultado no formato Excel sem a coluna de índice numérico
        df.to_excel(arquivo_saida, index=False)
        
        print(f"\nSucesso! {len(dados)} SKUs processados.")
        print(f"Planilha foi salva e atualizada como: {arquivo_saida}")
    else:
        print("Nenhum SKU foi encontrado no arquivo de texto.")

if __name__ == "__main__":
    processar_lista_para_excel()
