import os
import random
from datetime import datetime
from fpdf import FPDF
import qrcode


def desenhar_codigo_barras_vertical(pdf, x, y, largura, altura):
    pdf.rect(x, y, largura, altura)
    # CORREÇÃO: Gerador isolado para não afetar o sistema global do Python
    gerador = random.Random(42)
    y_atual = y + 1
    while y_atual < y + altura - 2:
        espessura = gerador.choice([0.6, 1.0, 1.4, 0.4])
        pdf.set_fill_color(0, 0, 0)
        pdf.rect(x + 1, y_atual, largura - 2, espessura, style='F')
        y_atual += espessura + gerador.choice([0.4, 0.8, 1.2])


def criar_imagem_qrcode(link, caminho_arquivo):
    """Gera o arquivo de imagem do QR Code."""
    img = qrcode.make(link)
    img.save(caminho_arquivo)
    return caminho_arquivo


def desenhar_via(pdf, x_offset, w_lateral, titulo, dados, numero_bilhete, empresa_nome, tarifas, qr_img, tipo_via, icms,
                 outros_trib, valortotal):
    y_topo = 8 # Cabeçalho
    pdf.set_xy(x_offset, y_topo + 3)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(w_lateral, 4, titulo, align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_xy(x_offset, y_topo + 7)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.cell(w_lateral, 4, 'DOCUMENTO AUXILIAR DE BILHETE DE PASSAGEM ELETRÔNICO', align='C', new_x='LMARGIN',
             new_y='NEXT')

    pdf.set_xy(x_offset + 3, y_topo + 12)
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.cell(65, 3.5, empresa_nome, new_x='LMARGIN', new_y='NEXT')

    pdf.set_xy(x_offset + 3, y_topo + 24) # Itinerário
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Viação: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, f'{empresa_nome.title()}\n')

    pdf.set_x(x_offset + 3)
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Origem: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, f"{dados['origem']}\n")

    pdf.set_x(x_offset + 3)
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Destino: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, f"{dados['destino']}\n")

    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

    pdf.set_x(x_offset + 3)
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Data/Hora: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, f"{dados.get('data_horario', data_atual)}   ")
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Poltrona: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, f"{dados['poltrona']}\n")

    pdf.set_x(x_offset + 3)
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Linha: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, f"{dados['origem']} X {dados['destino']}\n")

    pdf.set_x(x_offset + 3)
    pdf.set_font('Helvetica', size=7)
    pdf.write(4, 'Tipo viagem: ')
    pdf.set_font('Helvetica', 'B', 7.5)
    pdf.write(4, 'HORARIO ORDINARIO          ')

    # Classe e Bilhete
    pdf.set_xy(x_offset + 55, y_topo + 24)
    pdf.set_font('Helvetica', 'B', 7)
    pdf.cell(50, 3.5, 'Classe: CONVENCIONAL', align='R', new_x='LMARGIN', new_y='NEXT')
    pdf.set_x(x_offset + 55)
    pdf.cell(50, 3.5, f'Número Bilhete: {numero_bilhete}', align='R', new_x='LMARGIN', new_y='NEXT')

    desenhar_codigo_barras_vertical(pdf, x=x_offset + 4, y=y_topo + 66, largura=22, altura=65)

    # Dados Passageiro e Valores
    pdf.set_xy(x_offset + 30, y_topo + 68)
    pdf.set_font('Helvetica', size=6.5)
    pdf.write(3.5, 'Passageiro: ')
    pdf.set_font('Helvetica', 'B', 7)
    pdf.write(3.5, f"{dados['passageiro']}\n")

    pdf.set_x(x_offset + 30)
    pdf.set_font('Helvetica', size=6.5)
    pdf.write(3.5, 'Documento: ')
    pdf.set_font('Helvetica', 'B', 7)
    pdf.write(3.5, f"{dados.get('documento', '')}\n")

    pdf.set_x(x_offset + 30)
    pdf.set_font('Helvetica', size=6.5)
    pdf.write(3.5, 'Tipo do desconto: Normal\n\n')

    for rotulo, val in tarifas:
        pdf.set_x(x_offset + 30)
        negrito = 'B' if 'Valor' in rotulo else ''
        pdf.set_font('Helvetica', negrito, 6.5)
        pdf.cell(52, 3.2, rotulo)
        pdf.cell(22, 3.2, val, align='R', new_x='LMARGIN', new_y='NEXT')

    if tipo_via == 'passageiro':
        pdf.ln(2)
        pdf.rect(x_offset + 38, y_topo + 142, 28, 28)
        pdf.image(qr_img, x=x_offset + 39, y=y_topo + 143, w=26, h=26)

        pdf.set_xy(x_offset + 3, y_topo + 180)
        pdf.set_font('Helvetica', size=5.5)
        pdf.multi_cell(
            w_lateral - 6, 2.8,
            f"Tributos Totais Incidentes (Lei Federal 12.741/2012) ICMS: R$ {icms:.2f} (12,00%)\n"
            f"OUTROS TRIB: R$ {outros_trib:.2f} (12,00%)"
        )
    elif tipo_via == 'motorista':
        pdf.rect(x_offset + 24, y_topo + 140, 56, 46)
        pdf.image(qr_img, x=x_offset + 40, y=y_topo + 143, w=24, h=24)

        pdf.set_xy(x_offset + 24, y_topo + 170)
        pdf.set_font('Helvetica', size=6)
        pdf.multi_cell(56, 3, "Utilize esse código para acessar\na área de embarque", align='C')


def gerar_bilhete(dados):
    os.makedirs('bilhetes', exist_ok=True)

    pdf = FPDF(orientation='L', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    pdf.set_margins(0, 0, 0)
    pdf.add_page()

    x_col1 = 10
    w_lateral = 107.75
    w_meio = 61.5
    x_col2 = x_col1 + w_lateral
    x_col3 = x_col2 + w_meio
    y_topo = 8
    h_caixa = 194

    pdf.set_draw_color(0, 0, 0)
    pdf.rect(x_col1, y_topo, w_lateral, h_caixa)
    pdf.rect(x_col2, y_topo, w_meio, h_caixa)
    pdf.rect(x_col3, y_topo, w_lateral, h_caixa)

    url_embarque = "https://www.linkedin.com/in/jorgemodrow/"
    url_acesso = "https://www.linkedin.com/in/jorgemodrow/"

    qr_temp1 = "bilhetes/qr_temp1.png"
    qr_temp2 = "bilhetes/qr_temp2.png"
    criar_imagem_qrcode(url_embarque, qr_temp1)
    criar_imagem_qrcode(url_acesso, qr_temp2)

    numero_bilhete = f"{random.randint(1, 999999):06d}"
    empresa_nome = 'VIAÇÃO DAS ARAUCÁRIAS'

    valortotal = dados['preco']
    pedagio = (valortotal * 0.03) if valortotal > 40 else 0.0
    tarifa = valortotal - pedagio
    icms = valortotal * 0.12
    outros_trib = valortotal * 0.12

    tarifas = [
        ('Tarifa', f'{tarifa:.2f}'),
        ('Pedágio', f'{pedagio:.2f}'),
        ('Taxa de Embarque', '0.00'),
        ('Seguro Obrigatório', '0.0'),
        ('Outros', '0.00'),
        ('Valor Total', f'{valortotal:.2f}')
    ]

    # COLUNA 1: Via do Passageiro (Renderizada com a função)
    desenhar_via(pdf, x_col1, w_lateral, 'Via do Passageiro', dados, numero_bilhete, empresa_nome, tarifas, qr_temp1,
                 'passageiro', icms, outros_trib, valortotal)

    # COLUNA 2: Direitos do Passageiro
    pdf.set_xy(x_col2, y_topo + 3)
    pdf.set_font('Helvetica', 'B', 8.5)
    pdf.cell(w_meio, 4, 'DIREITOS DO PASSAGEIRO*', align='C', new_x='LMARGIN', new_y='NEXT')

    texto_direitos = (
        "RESOLUÇÃO ANTT Nº 4.282, DE 17 DE FEVEREIRO DE 2014.\n\n"
        "I - ser transportado com pontualidade, segurança, higiene e conforto;\n\n"
        "II - transportar, gratuitamente, até 30 (trinta) quilos de bagagem no "
        "bagageiro e 5 (cinco) quilos de volume no porta-embrulho;\n\n"
        "III - receber os comprovantes das bagagens transportadas no bagageiro e "
        "ser indenizado por extravio ou dano de bagagem transportada no bagageiro;\n\n"
        "IV - receber a diferença do preço da passagem em veículos de característica "
        "inferior às daquele contratado;\n\n"
        "V - receber, às expensas da transportadora, alimentação e pousada, nos casos "
        "de venda de mais de um bilhete de passagem para a mesma poltrona ou "
        "interrupção/retardamento da viagem, após 3 (três) horas, em razão de defeito, "
        "falha ou outro motivo de responsabilidade da transportadora;\n\n"
        "VI - receber da transportadora, em caso de acidente, imediata e adequada assistência;\n\n"
        "VII - optar, em caso de atraso por período superior a 1 (uma) hora, por: "
        "continuar a viagem em outra empresa às expensas da transportadora; ou receber de "
        "imediato o valor do bilhete de passagem, em caso de desistência; ou continuar a "
        "viagem, pela mesma transportadora, que deverá dar continuidade à viagem num período "
        "máximo de 3 (três) horas após a interrupção;\n\n"
        "VIII - remarcar o bilhete adquirido observado o prazo de um 1 (ano) de validade do bilhete "
        "a contar da data da primeira emissão. A partir de 3 (três) horas antes do início da viagem, "
        "é facultado à transportadora efetuar a cobrança de até 20% (vinte por cento) do valor da "
        "tarifa a título de remarcação;\n\n"
        "IX - transferir o bilhete adquirido, exceto se o contrato de transporte dispuser de outra "
        "maneira, observado o prazo de 1 (um) ano de validade do bilhete a contar da data da primeira "
        "emissão;\n\n"
        "X - receber a importância paga no caso de desistência da viagem, desde que com antecedência "
        "mínima de 3 (três) horas em relação ao horário de partida constante do bilhete, facultado à "
        "transportadora o desconto de 5% (cinco por cento) do valor da tarifa;\n\n"
        "XI - estar garantido pelo Seguro de Responsabilidade Civil contratado pela transportadora;\n\n"
        "XII - não ser obrigado a adquirir seguro facultativo complementar de viagem.\n\n"
        "* Válido para viagens interestaduais e internacionais, sob regulação da ANTT. Para viagens "
        "intermunicipais dentro do mesmo estado, consulte a empresa transportadora para mais informações;\n\n"
        "* Em Minas Gerais, o cancelamento pode ser feito com até 12 (doze) horas de antecedência do embarque. "
        "No Pará, o prazo é de até 8 (oito) horas antes do embarque;"
    )

    pdf.set_xy(x_col2 + 2, y_topo + 9)
    pdf.set_font('Helvetica', size=5.3)
    pdf.multi_cell(w_meio - 4, 2.5, texto_direitos, align='L')

    # COLUNA 3: Via do Motorista
    desenhar_via(pdf, x_col3, w_lateral, 'Via do Motorista', dados, numero_bilhete, empresa_nome, tarifas, qr_temp2,
                 'motorista', icms, outros_trib, valortotal)

    nome_arquivo = f'passagem_{dados["passageiro"].lower().replace(" ", "_")}.pdf'
    caminho_final = f'bilhetes/{nome_arquivo}'

    try: # Limpeza segura de arquivos
        pdf.output(caminho_final)
    finally:
        for temp in (qr_temp1, qr_temp2):
            if os.path.exists(temp):
                os.remove(temp)

    return nome_arquivo