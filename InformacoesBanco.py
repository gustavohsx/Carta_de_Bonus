import cx_Oracle
import sys
from datetime import date
import credenciais


class InformacoesBanco:

    def __init__(self):
        ano, mes, dia = f'{date.today()}'.split('-')
        # print(ano, mes, dia )
        self.data = f"{dia}/{mes}/{ano}"

    def __conector(self):
        try:
            connection = cx_Oracle.connect(credenciais.credenciais['string_conexao_banco'])
        except cx_Oracle.DatabaseError:
            print(cx_Oracle.DatabaseError)
            sys.exit()
        else:
            # print('Conectado', connection.version)
            return connection.cursor()

    def cliente(self, cod_cliente):
        conn = self.__conector()
        conn.execute(
            """
            SELECT p.cliente, p.fantasia, p.endercob, p.bairrocob, p.municcob, pp.codpraca, pp.praca, pp.rota 
            FROM pcpraca pp JOIN pcclient p ON pp.codpraca = p.codpraca 
            WHERE p.codcli = :cod_cliente
            """, cod_cliente=cod_cliente)
        consulta = conn.fetchall()
        conn.close()
        return consulta[0]
    
    def informacoesProdutosCompradosCliente(self, codigo_cliente, codigo_produto, data_inicial, data_final=None):
        if data_final == None:
            data_final = self.data
        conn = self.__conector()
        conn.execute("""
            SELECT pp.rua, pp.numero, pp.apto, pi.codprod, pp.descricao, TO_CHAR(pc.data, 'DD/MM/YYYY'), pc.dtcancel, pc.numnota
            FROM pcpedc pc JOIN pcpedi pi ON pc.numped = pi.numped JOIN pcclient p ON 
            p.codcli = pc.codcli JOIN pcprodut pp ON pi.codprod = pp.codprod
            WHERE p.codcli = :codigo_cliente
            AND pi.codprod = :codigo_produto
            AND pc.data BETWEEN TO_DATE(:data_inicial, 'DD/MM/YYYY') AND TO_DATE(:data_final, 'DD/MM/YYYY')
            ORDER BY pc.data DESC
            """, data_inicial=data_inicial, data_final=data_final, codigo_cliente=codigo_cliente, codigo_produto=codigo_produto)
        consulta = conn.fetchall()
        conn.close()
        return consulta


# info = InformacoesBanco()
# # lista = ['879340', '878730']
# cod_cliente = '17185'
# #
# # for cod_produto in lista:
# #     print(info.descricaoProduto(cod_produto))
#
# print(info.cliente('17185'))
# print(info.pedidoCliente(cod_cliente='17185', cod_produto='879340'))
#lista = ['17185', '878740']
# print(info.informacoesProdutosCompradosCliente(codigo_cliente='13386', codigo_produto='878885', data_inicial='01/05/2023'))
# print(info.funcionarioResponsavel('946'))
#print(info.motivosDevolucao())