#  Gerador de Passagens de Ônibus em Python

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FPDF](https://img.shields.io/badge/FPDF-PDF_Generation-red?style=for-the-badge)
![QRCode](https://img.shields.io/badge/QRCode-Dynamic_Generation-black?style=for-the-badge)

Um sistema interativo via terminal que coleta dados de passageiros e gera, automaticamente, um bilhete de passagem de ônibus em formato PDF. O projeto foi desenvolvido para consolidar conceitos avançados de estruturação de código, manipulação de arquivos e uso de bibliotecas de terceiros.

## Funcionalidades

- **Coleta Segura de Dados:** Interface de terminal com validação rigorosa de tipos (inteiros, floats, strings e formatação de datas) utilizando `try/except`.
- **Geração de PDF Dinâmico:** Criação de um documento A4 em modo paisagem, dividido estruturalmente entre a Via do Passageiro, Direitos do Passageiro (ANTT) e Via do Motorista.
- **QR Codes e Códigos de Barra:** Geração isolada e randômica de códigos de barra verticais e anexação de QR Codes para simular o embarque.
- **Cálculo Automático:** Rateio dinâmico de tarifas, pedágios e tributos (ICMS) com base no valor total informado.

## Arquitetura do Projeto

O projeto adota o princípio de responsabilidade única, dividido em três módulos principais:
- `main.py`: Ponto de entrada da aplicação que orquestra o fluxo.
- `interface.py`: Módulo dedicado à validação de inputs e formatação visual no terminal.
- `gerador_pdf.py`: Módulo responsável pelo cálculo de posições (eixos X e Y) e renderização gráfica utilizando a biblioteca `fpdf`.

## 🚀 Como executar na sua máquina

1. Clone este repositório

2. Crie um ambiente virtual para isolar as dependências:
python -m venv .venv

3. Ative o ambiente virtual recém-criado:
- Windows:
.venv\Scripts\activate

- Linux/Mac:
source .venv/bin/activate

4. Instale as bibliotecas necessárias através do gestor de pacotes:
pip install -r requirements.txt

5. Inicie a aplicação:
python main.py

## Principais Aprendizagens

O desenvolvimento deste projeto consolidou os conhecimentos sobre o âmbito de variáveis e o manuseamento correto de dicionários. A refatoração contínua permitiu eliminar redundâncias no desenho do PDF, enquanto a utilização da estrutura try/finally garantiu que ficheiros de imagem temporários fossem adequadamente excluídos do disco após a geração do documento, mantendo o diretório limpo.