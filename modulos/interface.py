from datetime import datetime

def linha(tam=42):
    return '-' * tam

def cabecalho(texto):
    print(linha())
    print(texto.center(42))
    print(linha())


def leia_int(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print('\033[31mERRO: por favor, digite um número inteiro válido.\033[m')
        except KeyboardInterrupt:
            print('\n\033[31mUsuário preferiu não digitar esse número.\033[m')
            return 0
        else:
            return n

def leia_float(msg):
    while True:
        try:
            entrada = input(msg).replace(',', '.').strip()
            n = float(entrada)
        except (ValueError, TypeError):
            print('\033[31mERRO: por favor, digite um preço válido (ex: 120.50).\033[m')
        except KeyboardInterrupt:
            print('\n\033[31mUsuário preferiu não digitar esse número.\033[m')
            return 0.0
        else:
            return n

def leia_str(msg):
    while True:
        valor = str(input(msg)).strip()
        if valor == '':
            print('\033[31mERRO: o campo não pode ficar em branco.\033[m')
        else:
            return valor

def leia_data(msg):
    formato = "%d/%m/%Y %Hh%M"
    while True:
        try:
            entrada = str(input(msg)).strip()
            # Tenta converter a string para o formato especificado
            datetime.strptime(entrada, formato)
        except ValueError:
            print(
                "\033[31mERRO: Formato inválido ou data inexistente! "
                "Use o padrão DD/MM/AAAA HHhMM (ex: 15/10/2026 14h00).\033[m"
            )
        except KeyboardInterrupt:
            print("\n\033[31mUsuário preferiu não digitar a data.\033[m")
            return ""
        else:
            return entrada