import os
import shutil
import sys

# Garante que o diretório atual está no path para importar o módulo calculadora_sku
sys.path.append(r"C:\Users\18568\Documents\automacao-digs")
try:
    from calculadora_sku import calcular_digito
except ImportError:
    print("Erro: Não foi possível importar a função calcular_digito de calculadora_sku.py")
    sys.exit(1)

def renomear_e_transferir_imagens():
    pasta_origem = r"C:\Users\18568\Pictures\ENVIAR ELAS"
    pasta_destino = r"C:\Users\18568\Pictures\Envio Sap"

    # Verifica se a pasta de origem existe
    if not os.path.exists(pasta_origem):
        print(f"Pasta de origem não encontrada: {pasta_origem}")
        return

    # Cria a pasta de destino caso não exista
    if not os.path.exists(pasta_destino):
        os.makedirs(pasta_destino)
        print(f"Pasta de destino criada: {pasta_destino}")

    print(f"Analisando arquivos na pasta: {pasta_origem}\n")

    arquivos = os.listdir(pasta_origem)
    arquivos_transferidos = 0

    for arquivo in arquivos:
        # Obtem o nome do arquivo sem a extensão e a própria extensão
        nome, extensao = os.path.splitext(arquivo)
        
        # Ignora arquivos como desktop.ini e testa se o nome é formado por números (que deduzimos ser o SKU)
        if nome.isdigit():
            sku = nome
            # Calcula o dígito desse SKU usando aquela nossa mesma regra
            digito = calcular_digito(sku)
            novo_nome = f"{sku}-{digito}{extensao}"
            
            caminho_origem = os.path.join(pasta_origem, arquivo)
            caminho_destino = os.path.join(pasta_destino, novo_nome)
            
            # Copiando (transferindo) o arquivo para a nova pasta com o novo nome
            shutil.copy2(caminho_origem, caminho_destino)
            print(f"-> Imagem {arquivo} renomeada e enviada como: {novo_nome}")
            arquivos_transferidos += 1
        else:
            print(f"- Ignorando o arquivo {arquivo} (Não é um SKU válido)")

    print(f"\nFinalizado! {arquivos_transferidos} imagens foram renomeadas e salvas em: {pasta_destino}")

if __name__ == "__main__":
    renomear_e_transferir_imagens()
