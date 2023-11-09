from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from template import Template

informacoes = {
                'codigo':'CARCAS',
                'nome':'CARCAS',
                'fantasia':'CARCAS',
                'endereco':'CARCAS',
                'bairro':'CARCAS',
                'cidade':'CARCAS',
                'praca':'CARCAS',
                'rota':'CARCAS',
                'digitado_por':'JOSE',
                'titulo':'CARCAS',
                'ref':'RKFSF',
                'nf':'1235456'
            }

produtos = [
            ['9', '22', '206', '878730', '5X76G5X76G5X76G5X76G5X76G5X76G5X76G5X7 5X76G5X76G5X76G5X76G5X76G5X76G5X76G5X7 5X76G5X76G5X76G5X76G5X76G5X76G5X76G5X7', '12111 UND'],
            ['9', '17', '204', '879340', '5X76G5X76G5X76G5X76G5X76G5X76G5X76G5X76G5X76G', '12111 UND']
        ]

pdf = Template("teste.pdf", "TESTE")
pdf.desenharInformacoes(informacoes)
pdf.desenharProdutos(produtos)
pdf.salvarPDF()