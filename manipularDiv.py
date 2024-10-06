from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re
import time
import os


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
    print("1 - Crescente")
    print("2 - Decrescente")
    print("3 - Sair")
    print("-=" * 20)
    opc = int(input("Selecione sua opção: "))
    return opc


def main():
    valores_sem_reais = manipularPichau()
    while True:
        opc = menu()
        if opc == 1:
            time.sleep(3)
            os.system("cls")
            produtos_ordenados = insertion_sort(valores_sem_reais.copy())
            print("Produtos ordenados em ordem crescente:")
            print(produtos_ordenados)
        elif opc == 2:
            time.sleep(3)
            os.system("cls")
            produtos_ordenados_desc = insertion_sort_desc(valores_sem_reais.copy())
            print("Produtos ordenados em ordem decrescente:")
            print(produtos_ordenados_desc)
        elif opc == 3:
            time.sleep(3)
            os.system("cls")
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")


main()
