# Importa o módulo nativo do Python para ler e escrever JSON
import json

# Define uma função que recebe o valor de uma venda e devolve a comissão dela
def calcular_comissao(valor):
    # Vendas abaixo de R$ 100,00 não geram comissão; o return encerra a função
    if valor < 100:
        return 0
    # Se chegou aqui, o valor é 100 ou mais; se for menor que 500, a comissão é 1%
    if valor < 500:
        return valor * 0.01
    # Se chegou aqui, o valor é 500 ou mais (inclusive exatamente 500): comissão de 5%
    return valor * 0.05

# Abre o arquivo vendas.json; o "with" fecha o arquivo sozinho ao terminar
# encoding="utf-8" garante que acentos como "João" sejam lidos corretamente
with open("vendas.json", encoding="utf-8") as arquivo:
    # Converte o conteúdo do JSON em dicionário/lista do Python
    dados = json.load(arquivo)

# Cria um dicionário vazio que guardará a comissão acumulada de cada vendedor
totais = {}

# Percorre cada venda da lista, uma por vez
for venda in dados["vendas"]:
    # Pega o nome do vendedor da venda atual
    vendedor = venda["vendedor"]
    # Pega o valor da venda atual
    valor = venda["valor"]
    # totais.get(vendedor, 0) busca o total já acumulado (ou 0 se for a primeira venda dele)
    # Soma a comissão da venda atual e guarda de volta no dicionário
    totais[vendedor] = totais.get(vendedor, 0) + calcular_comissao(valor)

# Monta o dicionário final que será convertido em JSON
resultado = {
    # Lista com um item por vendedor
    "comissoes": [
        # Para cada vendedor, cria {"vendedor": nome, "comissao": total arredondado em 2 casas}
        {"vendedor": nome, "comissao": round(total, 2)}
        # Percorre cada par (nome, total) do dicionário de totais
        for nome, total in totais.items()
    ]
}

# Converte o dicionário em texto JSON e imprime na tela
# indent=2 deixa o JSON indentado e legível
# ensure_ascii=False mantém os acentos (sem isso, "João" viraria "Jo\u00e3o")
print(json.dumps(resultado, indent=2, ensure_ascii=False))