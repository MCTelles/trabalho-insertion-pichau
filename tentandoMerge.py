from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import time
import os
import tempfile
import heapq


def insertion_sort(produtos):
    for i in range(1, len(produtos)):
        key = produtos[i]
        j = i - 1
        while j >= 0 and key < produtos[j]:
            produtos[j + 1] = produtos[j]
            j -= 1
        produtos[j + 1] = key
    return produtos


def insertion_sort_desc(produtos):
    for i in range(1, len(produtos)):
        key = produtos[i]
        j = i - 1
        while j >= 0 and key > produtos[j]:
            produtos[j + 1] = produtos[j]
            j -= 1
        produtos[j + 1] = key
    return produtos


def merge_sort_externo(precos, chunk_size=10):
    temp_files = []

    # Passo 1: Dividir e ordenar os preços
    for i in range(0, len(precos), chunk_size):
        chunk = precos[i : i + chunk_size]
        chunk.sort()  # Ordena a parte
        temp_file = tempfile.NamedTemporaryFile(delete=False, mode="w+t")
        temp_file.writelines(f"{valor}\n" for valor in chunk)
        temp_file.flush()
        temp_files.append(temp_file.name)

    # Passo 2: Mesclar os arquivos temporários
    sorted_file = "saida_ordenada.txt"
    with open(sorted_file, "w") as out_file:
        min_heap = []

        # Usar um dicionário para armazenar arquivos abertos
        file_handles = {}

        for temp_file in temp_files:
            f = open(temp_file, "r")
            file_handles[temp_file] = f  # Armazenar o arquivo no dicionário
            line = f.readline()
            if line:
                heapq.heappush(min_heap, (float(line.strip()), temp_file))

        while min_heap:
            smallest_value, temp_file = heapq.heappop(min_heap)
            out_file.write(f"{smallest_value}\n")
            next_line = file_handles[temp_file].readline()
            if next_line:
                heapq.heappush(min_heap, (float(next_line.strip()), temp_file))

    # Fechar os arquivos abertos
    for f in file_handles.values():
        f.close()

    # Limpar arquivos temporários
    for temp_file in temp_files:
        os.remove(temp_file)

    return sorted_file


def manipularPichau():
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico)

    driver.get("https://www.pichau.com.br/promocao/bgs")
    time.sleep(3)

    div = driver.find_element(By.CLASS_NAME, "infinite-scroll-component__outerdiv")
    texto = div.text
    valores = re.findall(r"R\$[\s\d.,]+", texto)

    arrayTexto = [valor.strip() for valor in valores]
    valores_sem_reais = [
        float(
            valor.replace("R$", "").replace(" ", "").replace(".", "").replace(",", ".")
        )
        for valor in arrayTexto
    ]
    driver.quit()
    return valores_sem_reais


def menu():
    print("-=" * 20)
    print("1 - Crescente (Insertion)")
    print("2 - Decrescente (Insertion)")
    print("3 - MergeSort Externo")
    print("4 - Sair")
    print("-=" * 20)
    opc = int(input("Selecione sua opção: "))
    return opc


def main():
    valores_sem_reais = manipularPichau()
    while True:
        opc = menu()
        if opc == 1:
            time.sleep(2)
            os.system("cls")
            produtos_ordenados = insertion_sort(valores_sem_reais.copy())
            print("Produtos ordenados em ordem crescente:")
            print(produtos_ordenados)
        elif opc == 2:
            time.sleep(2)
            os.system("cls")
            produtos_ordenados_desc = insertion_sort_desc(valores_sem_reais.copy())
            print("Produtos ordenados em ordem decrescente:")
            print(produtos_ordenados_desc)
        elif opc == 3:
            merge_sortE = merge_sort_externo(valores_sem_reais.copy())
            print(merge_sortE)
        elif opc == 4:
            time.sleep(2)
            os.system("cls")
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")


main()
