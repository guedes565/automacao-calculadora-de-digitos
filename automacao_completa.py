import os
import shutil
import pyautogui
import time
import sys
import re
import string

# Garante a importação da nossa função do outro arquivo
sys.path.append(r"C:\Users\18568\Documents\automacao-digs")
try:
    from calculadora_sku import calcular_digito
    from processa_txt import processar_lista_para_excel
except ImportError:
    print("Erro crítico: Faltou arquivos como calculadora_sku.py ou processa_txt.py na pasta!")
    sys.exit(1)

def ler_txt_e_gerar_planilha():
    print("=== PASSO 1: LENDO O ARQUIVO TXT E SALVANDO PLANILHA ===")
    processar_lista_para_excel()
    print("-" * 50 + "\n")

def renomear_e_transferir():
    print("=== PASSO 2: RENOMEANDO IMAGENS DA PASTA ===")
    pasta_origem = r"C:\Users\18568\Pictures\ENVIAR ELAS"
    pasta_destino = r"C:\Users\18568\Pictures\Envio Sap"

    if not os.path.exists(pasta_origem):
        print(f"Aviso: A pasta {pasta_origem} não foi encontrada. Ignorando renomeação.")
        return

    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)

    arquivos = [f for f in os.listdir(pasta_origem) if os.path.isfile(os.path.join(pasta_origem, f))]
    arquivos_transferidos = 0

    # Dicionário para agrupar imagens que pertencem ao mesmo SKU
    grupos_sku = {}

    for arquivo in arquivos:
        nome, extensao = os.path.splitext(arquivo)
        # Extrai somente os números do início do nome (ignora letras, parênteses, etc)
        match = re.match(r'^(\d+)', nome)
        if match:
            sku = match.group(1)
            if sku not in grupos_sku:
                grupos_sku[sku] = []
            grupos_sku[sku].append(arquivo)
        else:
            print(f"- Ignorando o arquivo {arquivo} (Não possui um SKU no início)")

    alfabeto = string.ascii_uppercase # Contém 'A', 'B', 'C'...

    for sku, lista_arquivos in grupos_sku.items():
        # Ordena a lista de arquivos para a imagem principal ser a primeira (sem sufixo)
        lista_arquivos.sort()
        
        digito = calcular_digito(sku)
        
        for indice, arquivo in enumerate(lista_arquivos):
            _, extensao = os.path.splitext(arquivo)
            
            sufixo = ""
            if indice > 0:
                # 1ª imagem = indice 0 (sufixo vazio)
                # 2ª imagem = indice 1 (sufixo '_A')
                # 3ª imagem = indice 2 (sufixo '_B'), etc.
                letra = alfabeto[(indice - 1) % 26]
                sufixo = f"_{letra}"
                
            novo_nome = f"{sku}-{digito}{sufixo}{extensao}"
            
            caminho_origem = os.path.join(pasta_origem, arquivo)
            caminho_destino = os.path.join(pasta_destino, novo_nome)
            
            # Copia sobrescrevendo se já existir
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"-> Imagem {arquivo} renomeada e enviada como: {novo_nome}")
            arquivos_transferidos += 1

    
    print(f"Total: {arquivos_transferidos} imagens preparadas na pasta de envio Sap.\n")

def interagir_com_sap():
    print("=== PASSO 3: ENVIANDO DADOS PARA O SAP ===")
    print("ATENÇÃO: Clique AGORA na janela do SAP no seu monitor e coloque o cursor no campo branco de transação.")
    print("Você tem 15 SEGUNDOS para ir lá e clicar...\n")
    
    for i in range(15, 0, -1):
        print(f"Começando a digitar no SAP em... {i} segundos")
        time.sleep(1)

    print("\nIniciando o Robô RPA. POR FAVOR, TIRE A MÃO DO MOUSE E DO TECLADO!")
    
    # Digita o comando para a transação. O /n antes é um truque de usuários 
    # mestres de SAP que força a abertura da tela em qualquer lugar do sistema.
    pyautogui.write('/nZIMGITEM')
    time.sleep(0.5)
    pyautogui.press('enter')
    
    print("Aguardando 3 segundos pro SAP carregar a tela...")
    time.sleep(3)

    # Escrevendo o caminho exato com a barra no final
    caminho = r"C:\Users\18568\Pictures\Envio Sap\\"
    pyautogui.write(caminho)
    print("Caminho colado com sucesso...")
    time.sleep(0.8)

    # Pressionando a tecla Tab duas vezes para descer até a caixa do ignorar estoque
    # A ordem da tela do SAP é:
    # 1. Local das imagens
    # [Tab 1x] 2. S/ Carga; Apenas contabilizar
    # [Tab 2x] 3. Ignorar checagem de estoque
    pyautogui.press('tab')
    time.sleep(0.3)
    pyautogui.press('tab')
    time.sleep(0.3)
    
    # A tecla de espaço marca as famosas "checkboxes"
    pyautogui.press('space')
    print("Opção 'Ignorar checagem de estoque' marcada...")
    time.sleep(0.8)

    # Mandando enviar com o atalho nativo de reloginho do SAP (F8)
    pyautogui.press('f8')
    print("Clicou no reloginho (F8)!")

    print("\n✔ Automação de Carga Concluída com Sucesso!")

if __name__ == "__main__":
    ler_txt_e_gerar_planilha()
    renomear_e_transferir()
    interagir_com_sap()
