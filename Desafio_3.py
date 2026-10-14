#3. Faça um programa que a partir de um valor e de uma data de vencimento, calcule o valor dos juros na data de hoje considerando que a multa seja de 2,5% ao dia.


from datetime import datetime, date

valor = float(input("Digite o valor (R$): ").replace(",", "."))
vencimento_texto = input("Digite a data de vencimento (dd/mm/aaaa): ")

vencimento = datetime.strptime(vencimento_texto, "%d/%m/%Y").date()
hoje = date.today()

dias_atraso = (hoje - vencimento).days

if dias_atraso <= 0:
    print("A conta não está vencida. Não há juros.")
else:
    taxa_diaria = 0.025  # 2,5% ao dia
    juros = valor * taxa_diaria * dias_atraso
    total = valor + juros

    print(f"Dias em atraso: {dias_atraso}")
    print(f"Juros: R$ {juros:.2f}")
    print(f"Valor total a pagar: R$ {total:.2f}")