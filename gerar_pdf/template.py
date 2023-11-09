from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

class Template:
        
    def __init__(self, local_salvamento, nome_arquivo):
        self.pdf = canvas.Canvas(f"{local_salvamento}.pdf", pagesize=A4)
        self.pdf.setTitle(nome_arquivo)
        self._desenharItensPadrao()

    def desenharInformacoes(self, informacoes):

        self.pdf.setFont('Helvetica-Bold', 18)
        self.pdf.drawString(100, 700, informacoes['titulo'])
        self.pdf.line(100, 697, 490, 697)

        self.pdf.setFont('Helvetica-Bold', 11)

        self.pdf.drawString(145, 660, f'{informacoes["codigo"]} - {informacoes["nome"]}')

        self.pdf.drawString(145, 640, informacoes['fantasia'])
    
        self.pdf.drawString(145, 615, informacoes['endereco'])
    
        self.pdf.drawString(145, 590, informacoes['bairro'])
    
        self.pdf.drawString(145, 565, informacoes['cidade'])

        self.pdf.drawString(145, 540, informacoes['praca'])

        self.pdf.drawString(145, 515, f'{informacoes["rota"]} - {informacoes["cidade"]}')

        self.pdf.drawString(145, 490, informacoes['digitado_por'])

        self.pdf.drawString(145, 470, (informacoes['ref'][:36]).upper())

        self.pdf.drawString(468, 470, informacoes['nf'])

        self.pdf.line(50, 230, 545, 230)
        self.pdf.line(50, 230, 50, 185)
        self.pdf.setFont('Helvetica-Bold', 14)
        self.pdf.drawString(55, 210, 'Obs.:')
        self.pdf.line(50, 185, 545, 185)
        self.pdf.line(545, 230, 545, 185)

        if len(informacoes['obs']) > 56:
            self.pdf.setFont('Helvetica-Bold', 12)
            self.pdf.drawString(95, 210, f'{(informacoes["obs"][:56]).upper()}')
            self.pdf.drawString(95, 195, f'{(informacoes["obs"][56:112]).upper()}')
        else:
            self.pdf.setFont('Helvetica-Bold', 12)
            self.pdf.drawString(95, 210, f'{informacoes["obs"].upper()}')

    def desenharProdutos(self, lista_produtos):
        """
            Quantidade de Caracteres por coluna com fonte tamanho 10 negrito maiusculo:
            Codigo: 9
            Descricao: 33
            QT: 8
            Motivo: 14

            Quantidade de Caracteres por coluna com fonte tamanho 9 negrito maiusculo:
            Codigo: 10
            Descricao: 36
            QT: 9
            Motivo: 16
        """
        x = [42, 82, 132, 172, 252, 502]
        y = 405
        self.pdf.setFont('Helvetica-Bold', 11)
        for produto in lista_produtos:
            self.pdf.drawString(x[0], y, f'{produto[0]}')
            self.pdf.drawString(x[1], y, f'{produto[1]}')
            self.pdf.drawString(x[2], y, f'{produto[2]}')
            self.pdf.drawString(x[3], y, f'{produto[3]}')
            if len(produto[4]) > 36:
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(x[4], y+5, f'{produto[4][:39]}')
                self.pdf.drawString(x[4], y-5, f'{produto[4][39:]}')
            else:
                self.pdf.drawString(x[4], y, f'{produto[4]}')
            if len(produto[5]) > 8:
                self.pdf.setFont('Helvetica-Bold', 10)
                self.pdf.drawString(x[5], y, f'{produto[5]}')
            else:
                self.pdf.setFont('Helvetica-Bold', 11)
                self.pdf.drawString(x[5], y, f'{produto[5]}')
            y -= 25
    
    def _desenharItensPadrao(self):

        self.pdf.drawImage('gerar_pdf/imagens/logo.bmp', 35, 730, 100, 100)
        self.pdf.drawImage('gerar_pdf/imagens/logo_fundo.png', 35, 300, 500, 400)

        self.pdf.setFont('Helvetica-Bold', 11)
        self.pdf.drawString(55, 660, 'CLIENTE: ')
        self.pdf.drawString(55, 640, 'FANTASIA: ')
        self.pdf.drawString(55, 615, 'ENDEREÇO: ')
        self.pdf.drawString(55, 590, 'BAIRRO: ')
        self.pdf.drawString(55, 565, 'CIDADE: ')
        self.pdf.drawString(55, 540, 'PRAÇA: ')
        self.pdf.drawString(55, 515, 'ROTA: ')
        self.pdf.drawString(55, 490, 'DIGITADO POR: ')
        self.pdf.drawString(55, 470, 'REF: ')
        self.pdf.drawString(430, 470, 'N° NF: ')

        self.pdf.setFont('Helvetica-Bold', 14)
        self.pdf.drawString(50, 160, 'Desde já agradecemos a sua preferência pelos nossos produtos e serviços ')
        self.pdf.drawString(50, 140, 'na certeza de que poderemos contar com esta parceria por muitos anos.')

        self.pdf.setFont('Helvetica-Bold', 12)
        self.pdf.drawString(45, 430, 'RUA')
        self.pdf.drawString(82, 430, 'PREDIO')
        self.pdf.drawString(134, 430, 'APTO')
        self.pdf.drawString(195, 430, 'COD')
        self.pdf.drawString(338, 430, 'DESCRICAO')
        self.pdf.drawString(510, 430, 'QTD')

        self._desenharTabela()

        self.pdf.line(60, 100, 400, 100)
        self.pdf.line(410, 100, 440, 100)
        self.pdf.line(442, 100, 445, 120)
        self.pdf.line(445, 100, 475, 100)
        self.pdf.line(477, 100, 480, 120)
        self.pdf.line(480, 100, 530, 100)
        self.pdf.setFont('Helvetica', 12)
        self.pdf.drawString(140, 85, 'ASS. DO CLIENTE E DATA DE RECEBIMENTO')
    
    def _desenharTabela(self):
        quant_linhas = 8
        valores = (40, 445, 555, 120)
        distancia_entre_linhas = 25
        posicao_colunas = [(40, 40), (80, 80),(130, 130),(170, 170),(250, 250),(500, 500),(555, 555)]

        # Desenhar linhas da tabela
        x_inicial = valores[0]
        x_final = valores[2]
        y = valores[1]
        y_final = 0
        for i in range(quant_linhas + 1):
            self.pdf.line(x_inicial, y, x_final, y)
            y -= distancia_entre_linhas
            y_final = y + distancia_entre_linhas

        # Desenha colunas da tabela
        y_inicial = valores[1]
        for pos_coluna in posicao_colunas:
            self.pdf.line(pos_coluna[0], y_inicial, pos_coluna[1], y_final)

    def salvarPDF(self):
        self.pdf.save()