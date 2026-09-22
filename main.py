from modulos import interface, gerador_pdf

def coletar_dados_viagem():
    interface.cabecalho("NOVA PASSAGEM DE ÔNIBUS")
    print('Viação das Araucárias\n'.center(42))
    passagem = {}
    passagem['passageiro'] = interface.leia_str("Nome do passageiro: ").title()
    passagem['documento'] = interface.leia_str("Nº do documento (CPF/RG): ").title()
    passagem['origem'] = interface.leia_str("Cidade de origem: ").upper()
    passagem['destino'] = interface.leia_str("Cidade de destino: ").upper()
    passagem['data_horario'] = interface.leia_data("Data e Horário (ex: 15/10/2026 14h00): ")
    passagem['poltrona'] = interface.leia_int("Número do assento/poltrona: ")
    passagem['preco'] = interface.leia_float("Valor da passagem (R$): ")
    return passagem

def main():
    dados = coletar_dados_viagem()
    interface.cabecalho("DADOS REGISTRADOS COM SUCESSO")
    for chave, valor in dados.items():
        if chave == 'preco':
            print(f"{chave.capitalize():<15}: R$ {valor:.2f}")
        else:
            print(f"{chave.capitalize():<15}: {valor}")

    gerador_pdf.gerar_bilhete(dados)
    print('Arquivo criado com sucesso!')

if __name__ == "__main__":
    main()