#Faça um programa onde eu possa lançar movimentações de estoque dos produtos que estão no json abaixo, dando entrada ou saída da mercadoria no meu depósito, onde cada movimentação deve ter:
#Um número identificador único.
#Uma descrição para identificar o tipo da movimentação realizada
#que ao final da movimentação me retorne a qtde final do estoque do produto movimentado.

# Módulos nativos: json para ler/gravar dados, os para achar a pasta do script
import json
import os

# Monta o caminho do estoque.json na mesma pasta do script
PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA, "estoque_2.json")


def carregar_estoque():
    # Lê o JSON e devolve a lista de produtos
    with open(ARQUIVO, encoding="utf-8") as f:
        return json.load(f)["estoque"]


def salvar_estoque(produtos):
    # Grava o estoque atualizado de volta no arquivo JSON
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump({"estoque": produtos}, f, indent=2, ensure_ascii=False)


def buscar_produto(produtos, codigo):
    # Procura o produto pelo código; devolve None se não existir
    for produto in produtos:
        if produto["codigoProduto"] == codigo:
            return produto
    return None


def lancar_movimentacao(produtos, movimentacoes, codigo, tipo, quantidade, descricao):
    # Localiza o produto
    produto = buscar_produto(produtos, codigo)
    if produto is None:
        raise ValueError("Produto não encontrado.")

    # Quantidade precisa ser positiva
    if quantidade <= 0:
        raise ValueError("A quantidade deve ser maior que zero.")

    # Entrada soma ao estoque
    if tipo == "E":
        produto["estoque"] += quantidade
    # Saída subtrai, mas só se houver estoque suficiente
    elif tipo == "S":
        if quantidade > produto["estoque"]:
            raise ValueError(
                f"Estoque insuficiente. Disponível: {produto['estoque']}."
            )
        produto["estoque"] -= quantidade
    else:
        raise ValueError("Tipo inválido. Use E (entrada) ou S (saída).")

    # O ID único é o próximo número sequencial da lista de movimentações
    movimentacao = {
        "id": len(movimentacoes) + 1,
        "codigoProduto": codigo,
        "tipo": "Entrada" if tipo == "E" else "Saída",
        "descricao": descricao,
        "quantidade": quantidade,
        "estoqueFinal": produto["estoque"],
    }
    movimentacoes.append(movimentacao)
    return movimentacao


def main():
    produtos = carregar_estoque()
    movimentacoes = []  # histórico das movimentações da sessão

    print("=== Controle de Estoque ===")
    for p in produtos:
        print(f"{p['codigoProduto']} - {p['descricaoProduto']} (estoque: {p['estoque']})")

    # Repete até o usuário escolher sair
    while True:
        print()
        try:
            codigo = int(input("Código do produto (0 para sair): "))
            if codigo == 0:
                break

            produto = buscar_produto(produtos, codigo)
            if produto is None:
                print("Produto não encontrado.")
                continue

            tipo = input("Tipo (E = entrada, S = saída): ").strip().upper()
            quantidade = int(input("Quantidade: "))
            descricao = input("Descrição da movimentação: ").strip()

            mov = lancar_movimentacao(
                produtos, movimentacoes, codigo, tipo, quantidade, descricao
            )

            # Grava o novo estoque e mostra o resultado
            salvar_estoque(produtos)
            print(f"\nMovimentação nº {mov['id']} registrada: {mov['tipo']} - {mov['descricao']}")
            print(f"Estoque final de {produto['descricaoProduto']}: {mov['estoqueFinal']}")

        except ValueError as erro:
            # Captura erros de digitação e as regras de negócio
            print(f"Erro: {erro}")

    # Ao sair, mostra o resumo das movimentações da sessão
    print("\n=== Movimentações realizadas ===")
    print(json.dumps(movimentacoes, indent=2, ensure_ascii=False))


# Só executa o programa se o arquivo for rodado diretamente
if __name__ == "__main__":
    main()
