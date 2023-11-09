from tkinter import Label, Text, Button, Frame, ttk, Toplevel, font
from tkinter import filedialog as fd
from tkcalendar import Calendar
from InformacoesBanco import InformacoesBanco
from datetime import date
from numero import lerNumeroDocumento, atualizarNumeroDocumento
from gerar_pdf import template

class Tela:

    def __init__(self, tk):
        self.ano, self.mes, self.dia = f'{date.today()}'.split('-')
        self.data = f'{self.dia}/{self.mes}/{self.ano}'
        self.data_inicial = '01/03/2023'
        self.data_final = f'{self.dia}/{self.mes}/{self.ano}'

        self.numero_documento = lerNumeroDocumento()

        self.unidades_medida = ['UND', 'KG', 'PTE', 'CX', 'SC', 'FA']

        self.tk = tk
        self.banco = InformacoesBanco()
        self.ultimo_codigo_cliente = ''
        self.cliente = {
            'codigo':'',
            'nome':'',
            'fantasia':'',
            'endereco':'',
            'bairro':'',
            'cidade':'',
            'praca':'',
            'rota':''
        }

        self.digitado_por = 'CLAUDIO CARLOS'
        self.primeira_nota_fiscal = None
        self.ref = None
        self.obs = ''

        self.produtos_selecionados = []
        self.ultimo_produto_selecionado = None

        self.fonte_padrao_titulo = font.Font(size=15, weight='bold')
        self.fonte_padrao_texto = font.Font(size=10)
        self.fonte_padrao_texto_bold = font.Font(size=10, weight='bold')
        self.background_campos = '#e3e1e1'

        print("Variaveis iniciadas! \n",
              f"Data {self.data} \n",
              f"Data Inicial {self.data_inicial} \n",
              f"Data Final {self.data_final} \n",
              f"Cliente {self.cliente} \n",
              f"Digitado por {self.digitado_por} \n",
              f"Nota Fiscal {self.primeira_nota_fiscal} \n",
              f"Ref {self.ref} \n",
              f"Produtos selecionados {self.produtos_selecionados} \n",
              f"Ultimo Produto selecionado {self.ultimo_produto_selecionado} \n",
              f"OBS {self.obs} \n"
              "Iniciando Janela Principal"
              )
        self._janelaPrincipal()
        self._alterarDigitadoPorTela(self.digitado_por)

    def _buscarCliente(self):
        try:
            codigo_cliente = self._getCodigoCliente()
            if self.ultimo_codigo_cliente == '' or self.ultimo_codigo_cliente == None:
                self.ultimo_codigo_cliente = codigo_cliente
            elif codigo_cliente != self.ultimo_codigo_cliente:
                self.ultimo_codigo_cliente = codigo_cliente
                self._reiniciarTudo()
                self._alterarCodigoClienteTela(self.ultimo_codigo_cliente)
            else:
                self.ultimo_codigo_cliente = codigo_cliente
            cliente, fantasia, endercob, bairrocob, municcob, codpraca, praca, rota = self.banco.cliente(self.ultimo_codigo_cliente)
            self.cliente['codigo'] = codigo_cliente
            self.cliente['nome'] = cliente
            self.cliente['fantasia'] = fantasia
            self.cliente['endereco'] = endercob
            self.cliente['bairro'] = bairrocob
            self.cliente['cidade'] = municcob
            self.cliente['praca'] = f'{codpraca} - {praca}'
            self.cliente['rota'] = rota
            print(self.cliente)
            self._alterarDadosClienteTela()
            self._janelaAdicionarProduto()
        except:
            self._reiniciarTudo()

    def _buscarProduto(self):
        codigo_produto = self._getCodigoProduto()
        codigo_cliente = f'{self.cliente["codigo"]}'
        dados = self.banco.informacoesProdutosCompradosCliente(codigo_cliente, codigo_produto, self.data_inicial, self.data_final)
        self._limparListaProdutosBuscados()
        for dado in dados:
            aux = []
            aux.append(dado[7])
            aux.append(dado[3])
            aux.append(dado[4])
            aux.append(dado[5])
            aux.append(dado[0])
            aux.append(int(dado[1]))
            aux.append(dado[2])
            aux.append(dado[6])
            print(aux)
            self._inserirProdutosArvore(aux)

    def _alterarDadosClienteTela(self):
        try:
            self._alterarClienteTela(self.cliente['nome'])
        except Exception as e:
            self._alterarClienteTela('Indisponivel')
            self.cliente['nome'] = 'Indisponivel'
            print("Não foi possivel alterar a exibição do cliente da tela - Atribuindo Valor Padrão")

        try:
            self._alterarFantasiaTela(self.cliente['fantasia'])
        except Exception as e:
            self._alterarFantasiaTela('Indisponivel')
            self.cliente['fantasia'] = 'Indisponivel'
            print("Não foi possivel alterar a exibição da fantasia da tela - Atribuindo Valor Padrão")

        try:
            self._alterarEnderecoTela(self.cliente['endereco'])
        except Exception as e:
            self._alterarEnderecoTela('Indisponivel')
            self.cliente['endereco'] = 'Indisponivel'
            print("Não foi possivel alterar a exibição do endereco da tela - Atribuindo Valor Padrão")

        try:
            self._alterarBairroTela(self.cliente['bairro'])
        except Exception as e:
            self._alterarBairroTela('Indisponivel')
            self.cliente['bairro']= 'Indisponivel'
            print("Não foi possivel alterar a exibição do bairro da tela - Atribuindo Valor Padrão")

        try:
            self._alterarCidadeTela(self.cliente['cidade'])
        except Exception as e:
            self._alterarBairroTela('Indisponivel')
            self.cliente['cidade'] = 'Indisponivel'
            print("Não foi possivel alterar a exibição da cidade da tela - Atribuindo Valor Padrão")

        try:
            self._alterarPracaTela(self.cliente['praca'])
        except Exception as e:
            self._alterarBairroTela('Indisponivel')
            self.cliente['praca'] = 'Indisponivel'
            print("Não foi possivel alterar a exibição da praca da tela - Atribuindo Valor Padrão")

        try:
            self._alterarRotaTela(f'{self.cliente["rota"]} - {self.cliente["cidade"]}')
        except Exception as e:
            self._alterarBairroTela('Indisponivel')
            print("Não foi possivel alterar a exibição da rota da tela - Atribuindo Valor Padrão")

        try:
            self._alterarDigitadoPorTela(self.digitado_por)
        except Exception as e:
            self._alterarBairroTela('Indisponivel')
            self.digitado_por = ''
            print("Não foi possivel alterar a exibição do digitado por da tela - Atribuindo Valor Padrão")

    def _alterarClienteTela(self, cliente):
        self.cliente_codigo_nome_texto.config(state='normal')
        self.cliente_codigo_nome_texto.delete('1.0', 'end')
        self.cliente_codigo_nome_texto.insert('1.0', cliente)
        self.cliente_codigo_nome_texto.config(state='disabled')

    def _alterarFantasiaTela(self, fantasia):
        self.fantasia_texto.config(state='normal')
        self.fantasia_texto.delete('1.0', 'end')
        self.fantasia_texto.insert('1.0', fantasia)
        self.fantasia_texto.config(state='disabled')

    def _alterarEnderecoTela(self, endereco):
        self.endereco_texto.config(state='normal')
        self.endereco_texto.delete('1.0', 'end')
        self.endereco_texto.insert('1.0', endereco)
        self.endereco_texto.config(state='disabled')

    def _alterarBairroTela(self, bairro):
        self.bairro_texto.config(state='normal')
        self.bairro_texto.delete('1.0', 'end')
        self.bairro_texto.insert('1.0', bairro)
        self.bairro_texto.config(state='disabled')

    def _alterarCidadeTela(self, cidade):
        self.cidade_texto.config(state='normal')
        self.cidade_texto.delete('1.0', 'end')
        self.cidade_texto.insert('1.0', cidade)
        self.cidade_texto.config(state='disabled')
    
    def _alterarPracaTela(self, praca):
        self.praca_texto.config(state='normal')
        self.praca_texto.delete('1.0', 'end')
        self.praca_texto.insert('1.0', praca)
        self.praca_texto.config(state='disabled')

    def _alterarRotaTela(self, rota):
        self.rota_texto.config(state='normal')
        self.rota_texto.delete('1.0', 'end')
        self.rota_texto.insert('1.0', rota)
        self.rota_texto.config(state='disabled')
    
    def _alterarDigitadoPorTela(self, digitado_por):
        self.digitado_por_texto.delete('1.0', 'end')
        self.digitado_por_texto.insert('1.0', digitado_por)
    
    def _alterarNotaFiscalTela(self, nota_fiscal):
        self.nf_texto.delete('1.0', 'end')
        self.nf_texto.insert('1.0', nota_fiscal)

    def _alterarCodigoClienteTela(self, codigo):
        self.codigo_cliente_input.delete('1.0', 'end')
        self.codigo_cliente_input.insert('1.0', codigo)
    
    def _alterarRefTela(self, ref):
        self.ref_texto.delete('1.0', 'end')
        self.ref_texto.insert('1.0', ref)
    
    def _alterarObsTela(self, obs):
        self.obs_texto.delete('1.0', 'end')
        self.obs_texto.insert('1.0', obs)
        
    def _getCodigoCliente(self):
        codigo_cliente = self.codigo_cliente_input.get('1.0', 'end').split('\n')
        return codigo_cliente[0]

    def _getCodigoProduto(self):
        codigo_produto = self.codigo_produto_input.get('1.0', 'end').split('\n')
        return codigo_produto[0]

    def _getQuantidadeProdutoRecolhimento(self):
        quant = self.quantidade_input.get('1.0', 'end').split('\n')[0]
        quant_unidade = self.quantidade_lista_input.get()
        quantidade = f'{quant} {quant_unidade}'
        return quantidade
    
    def _atualizarDataInicial(self):
        self.data_inicial_variavel.configure(state='normal')
        self.data_inicial_variavel.delete('1.0', 'end')
        self.data_inicial_variavel.insert('1.0', self.data_inicial)
        self.data_inicial_variavel.configure(state='disabled')
    
    def _atualizarCodigoCliente(self, event):
        self.cliente['codigo'] = self.codigo_cliente_input.get('1.0', 'end').split('\n')[0]

    def _atualizarDataFinal(self):
        self.data_final_variavel.configure(state='normal')
        self.data_final_variavel.delete('1.0', 'end')
        self.data_final_variavel.insert('1.0', self.data_final)
        self.data_final_variavel.configure(state='disabled')
    
    def _atualizarNotaFiscal(self, event):
        self.primeira_nota_fiscal = self.nf_texto.get('1.0', 'end').split('\n')[0]
    
    def _atualizarRef(self, event):
        self.ref = self.ref_texto.get('1.0', 'end').split('\n')[0]
        tamanho_max = 36
        tamanho_alerta = 30
        if len(self.ref) > tamanho_max:
            self.ref_texto.config(background='#ED3030')
        elif len(self.ref) > tamanho_alerta:
            self.ref_texto.config(background='#EDEA4A')
        else:
            self.ref_texto.config(background='#ffffff')
    
    def _atualizarDigitadoPor(self, event):
        self.digitado_por = self.digitado_por_texto.get('1.0', 'end').split('\n')[0]

    def _atualizarObs(self, event):
        self.obs = self.obs_texto.get('1.0', 'end').split('\n')[0]
        tamanho_max = 112
        tamanho_alerta = 106
        if len(self.obs) > tamanho_max:
            self.obs_texto.config(background='#ED3030')
        elif len(self.obs) > tamanho_alerta:
            self.obs_texto.config(background='#EDEA4A')
        else:
            self.obs_texto.config(background='#ffffff')
    
    def _cancelarSelecionarProdutos(self, event):
        self._fecharJanelaSelecionarProdutos()
    
    def _fecharJanelaSelecionarProdutos(self):
        self.segunda_janela.destroy()
    
    def _prevenirQuebraLinhaCodigoClienteInput(self, event):
        self.codigo_cliente_botao.invoke()
        return "break"
    
    def _prevenirQuebraLinhaCodigoProdutoInput(self, event):
        self.buscar_produto.invoke()
        return "break"
    
    def _prevenirQuebraLinhaAdicionarMotivoQuantidade(self, event):
        self.adicionar.invoke()
        return "break"
    
    def _cancelarQuantidadeEscape(self, event):
        self._fecharJanelaQuantidadeItem()

    def _fecharJanelaQuantidadeItem(self):
        self.janela_quantidade_motivo.destroy()
    
    def _inserirDataInicial(self):
        data = self.calendario_data_inicial.get_date()
        self.data_inicial = f'{data}'
        self.data_inicial_variavel.configure(state='normal')
        self.data_inicial_variavel.delete('1.0', 'end')
        self.data_inicial_variavel.insert('1.0', self.data_inicial)
        self.data_inicial_variavel.configure(state='disabled')
        # self.adicionarProdutosArvore()
        self.janela_selecionar_data_inicial.destroy()
        self._buscarProduto()

    def _inserirDataFinal(self):
        data = self.calendario_data_final.get_date()
        self.data_final = f'{data}'
        self.data_final_variavel.configure(state='normal')
        self.data_final_variavel.delete('1.0', 'end')
        self.data_final_variavel.insert('1.0', self.data_final)
        self.data_final_variavel.configure(state='disabled')
        # self.adicionarProdutosArvore()
        self.janela_selecionar_data_final.destroy()
        self._buscarProduto()
    
    def _inserirProdutosArvore(self, produto):
        self.tree.insert('', 'end', values=produto)
    
    def _itemSelecionadoTree(self, event):
        for item_selecionado in self.tree.selection():
            item = self.tree.item(item_selecionado)
            self.ultimo_produto_selecionado = item['values']

            self._janelaQuantidadeItem()
            self._fecharJanelaSelecionarProdutos()
        
    def _adicionarItemSelecionado(self):
        quantidade = self._getQuantidadeProdutoRecolhimento()
        self.ultimo_produto_selecionado.insert(3, quantidade)
        aux = [str(self.ultimo_produto_selecionado[5]),
               str(self.ultimo_produto_selecionado[6]),
               str(self.ultimo_produto_selecionado[7]),
               str(self.ultimo_produto_selecionado[1]),
               str(self.ultimo_produto_selecionado[2]),
               str(self.ultimo_produto_selecionado[3]),
               ]
        self.produtos_selecionados.append(aux)
        if self.primeira_nota_fiscal == None or self.primeira_nota_fiscal == '':
            self.primeira_nota_fiscal = self.ultimo_produto_selecionado[0]
            self._alterarNotaFiscalTela(self.primeira_nota_fiscal)
        self._fecharJanelaQuantidadeItem()
        self._atualizarListaProdutosSelecionados()
    
    def _fecharJanelaSelecionarProdutos(self):
        self.segunda_janela.destroy()
    
    def _atualizarListaProdutosSelecionados(self):
        self._limparListaProdutosSelecionados()
        for produto in self.produtos_selecionados:
            self.produtos_arvore.insert('', 'end', values=produto)

    def _limparListaProdutosBuscados(self):
        try:
            self.tree.delete(*self.tree.get_children())
        except Exception as e:
            print('Erro ao Apagar a Lista de Produtos Buscados!', e)

    def _limparListaProdutosSelecionados(self):
        try:
            self.produtos_arvore.delete(*self.produtos_arvore.get_children())
        except Exception as e:
            print('Erro ao Apagar a Lista de Produtos Selecionados!', e)
    
    def _fecharJanelaErroRefEvento(self, event):
        self.janela_erro_ref.destroy()

    def _fecharJanelaErroRef(self):
        self.janela_erro_ref.destroy()

    def _fecharJanelaErroNotaFiscalEvento(self, event):
        self.janela_erro_nf.destroy()

    def _fecharJanelaErroNotaFiscal(self):
        self.janela_erro_nf.destroy()
    
    def _prepararListasImprimirPDF(self):
        print("Preparando para imprimir")
        if self.ref == '' or self.ref == None:
            self._janelaErroRef()
        elif self.primeira_nota_fiscal == '' or self.primeira_nota_fiscal == None:
            self._janelaErroNotaFiscal()
        else:
            filetypes = (('PDF', '*.pdf'), ('Todos os Arquivos', '*.*'))
            caminho = fd.asksaveasfilename(title="Escolha o Local de Salvamento", initialdir='C://Desktop/', filetypes=filetypes)
            pdf = template.Template(str(caminho), "Pdf")
            try:
                informacoes = {
                    'titulo':f'CARTA DE BÔNUS  Nº: {self.numero_documento} - DATA: {self.data}',
                    'codigo':str(self.cliente['codigo']),
                    'nome':str(self.cliente['nome']),
                    'fantasia':str(self.cliente['fantasia']),
                    'endereco':str(self.cliente['endereco']),
                    'bairro':str(self.cliente['bairro']),
                    'cidade':str(self.cliente['cidade']),
                    'praca':str(self.cliente['praca']),
                    'rota':str(self.cliente['rota']),
                    'digitado_por':self.digitado_por,
                    'ref':self.ref,
                    'nf':str(self.primeira_nota_fiscal),
                    'obs': self.obs
                }
                print(informacoes)
                pdf.desenharInformacoes(informacoes)
            except Exception as e:
                print("Não foi possivel desenhar as informações no PDF!", e)
            try:
                print(self.produtos_selecionados)
                pdf.desenharProdutos(self.produtos_selecionados)
            except Exception as e:
                print("Não foi possivel desenhar os produtos no PDF!", e)
            try:
                print("Iniciando salvamento do PDF")
                pdf.salvarPDF()
                print("PDF salvo \nIniciando atualizacao do numero do documento")
                atualizarNumeroDocumento()
                self._reiniciarTudo()
                self.numero_documento = lerNumeroDocumento()
                self.titulo.config(text=f'CARTA DE BÔNUS  Nº: {self.numero_documento} - DATA: {self.data}')
                print("Numero do documento atualizado com sucesso")
                self.janela_principal_frame.update_idletasks()
                self.codigo_cliente_input.focus_set()
            except Exception as e:
                print("Erro ao Gerar PDF!", e)

    def _reiniciarTudo(self):
        print("Inciando reinicio das variaveis e estruturas")
        try:
            self.cliente['codigo'] = ''
            self.cliente['nome'] = ''
            self.cliente['fantasia'] = ''
            self.cliente['endereco'] = ''
            self.cliente['bairro'] = ''
            self.cliente['cidade'] = ''
            self.cliente['praca'] = ''
            self.cliente['rota'] = ''
            self._alterarDadosClienteTela()
            self._alterarCodigoClienteTela(self.cliente['codigo'])
            self.ref_texto.config(background='#ffffff')
            self.obs_texto.config(background='#ffffff')
        except Exception as e:
            print("Erro ao alterar informações do cliente para vazio!", e)
        try:
            self._limparListaProdutosSelecionados()
        except Exception as e:
            print("Erro ao tentar limpar lista de produtos selecionado!", e)
        try:
            self.primeira_nota_fiscal = ''
            self._alterarNotaFiscalTela(self.primeira_nota_fiscal)
        except Exception as e:
            print("Erro ao tentar limpar valor da nota fiscal!", e)
        try:
            self.produtos_selecionados = []
        except Exception as e:
            print("Erro ao tentar reescrever a lista de produtos selecionados para uma lista vazia!", e)
        try:
            self.ref = ''
            self._alterarRefTela(self.ref)
        except Exception as e:
            print("Erro ao tentar reescrever o referencial!", e)
        try:
            self.obs = ''
            self._alterarObsTela(self.obs)
        except Exception as e:
            print("Erro ao tentar reescrever a observacao!", e)
        print("Reinicio finalizado")
    
    def _janelaPrincipal(self):
        
        self.janela_principal_frame = Frame(self.tk)
        
        self.titulo = Label(self.janela_principal_frame, text=f'CARTA DE BÔNUS  Nº: {self.numero_documento} - DATA: {self.data}', font=(self.fonte_padrao_titulo))

        codigo_cliente_label = Label(self.janela_principal_frame, text='CÓDIGO DO CLIENTE:', font=(self.fonte_padrao_texto_bold))
        self.codigo_cliente_input = Text(self.janela_principal_frame, height=1, width=20)
        self.codigo_cliente_input.focus_set()
        self.codigo_cliente_input.bind('<Return>', self._prevenirQuebraLinhaCodigoClienteInput)
        self.codigo_cliente_input.bind("<KeyRelease>", self._atualizarCodigoCliente)
        self.codigo_cliente_botao = Button(self.janela_principal_frame, text='Buscar', width=15, command=self._buscarCliente, font=(self.fonte_padrao_texto), bg='#373aa3', fg='white')

        cliente_label = Label(self.janela_principal_frame, text='CLIENTE:', font=(self.fonte_padrao_texto))
        self.cliente_codigo_nome_texto = Text(self.janela_principal_frame, height=1, width=40, state='disabled', background=self.background_campos)
        fantasia_label = Label(self.janela_principal_frame, text='FANTASIA:', font=(self.fonte_padrao_texto))
        self.fantasia_texto = Text(self.janela_principal_frame, height=1 ,width=40, state='disabled', background=self.background_campos)
        endereco_label = Label(self.janela_principal_frame, text='ENDEREÇO:', font=(self.fonte_padrao_texto))
        self.endereco_texto = Text(self.janela_principal_frame, height=1 ,width=40, state='disabled', background=self.background_campos)
        bairro_label = Label(self.janela_principal_frame, text='BAIRRO:', font=(self.fonte_padrao_texto))
        self.bairro_texto = Text(self.janela_principal_frame, height=1 ,width=40, state='disabled', background=self.background_campos)
        cidade_label = Label(self.janela_principal_frame, text='CIDADE:', font=(self.fonte_padrao_texto))
        self.cidade_texto = Text(self.janela_principal_frame, height=1 ,width=40, state='disabled', background=self.background_campos)
        praca_label = Label(self.janela_principal_frame, text='PRAÇA:', font=(self.fonte_padrao_texto))
        self.praca_texto = Text(self.janela_principal_frame, height=1 ,width=40, state='disabled', background=self.background_campos)
        rota_label = Label(self.janela_principal_frame, text='ROTA:', font=(self.fonte_padrao_texto))
        self.rota_texto = Text(self.janela_principal_frame, height=1 ,width=40, state='disabled', background=self.background_campos)
        digitado_por_label = Label(self.janela_principal_frame, text='DIGITADO POR:', font=(self.fonte_padrao_texto))
        self.digitado_por_texto = Text(self.janela_principal_frame, height=1 ,width=40)
        self.digitado_por_texto.bind("<KeyRelease>", self._atualizarDigitadoPor)
        ref_label = Label(self.janela_principal_frame, text='REF:', font=(self.fonte_padrao_texto))
        self.ref_texto = Text(self.janela_principal_frame, height=1 ,width=40)
        self.ref_texto.bind("<KeyRelease>", self._atualizarRef)
        nf_label = Label(self.janela_principal_frame, text='NF:', font=(self.fonte_padrao_texto))
        self.nf_texto = Text(self.janela_principal_frame, height=1 ,width=20)
        self.nf_texto.bind("<KeyRelease>", self._atualizarNotaFiscal)

        adicionar_produto_botao = Button(self.janela_principal_frame, text='Adicionar Produto', width=20, command=self._janelaAdicionarProduto, font=(self.fonte_padrao_texto), bg='#373aa3', fg='white')

        obs_label = Label(self.janela_principal_frame, text='OBSERVAÇÕES:', font=(self.fonte_padrao_texto))
        self.obs_texto = Text(self.janela_principal_frame, height=3 ,width=40)
        self.obs_texto.bind("<KeyRelease>", self._atualizarObs)

        colunas = [ 'rua', 'predio', 'apto', 'cod', 'desc', 'qtd']

        self.produtos_arvore = ttk.Treeview(self.janela_principal_frame, columns=colunas, show='headings', height=5)
        self.produtos_arvore.column(0, anchor="center", width=8)
        self.produtos_arvore.column(1, anchor="center", width=8)
        self.produtos_arvore.column(2, anchor="center", width=8)
        self.produtos_arvore.column(3, anchor="center", width=20)
        self.produtos_arvore.column(4, anchor="center", width=200)
        self.produtos_arvore.column(5, anchor="center", width=20)

        self.produtos_arvore.heading('rua', text='RUA')
        self.produtos_arvore.heading('predio', text='PREDIO')
        self.produtos_arvore.heading('apto', text='APTO')
        self.produtos_arvore.heading('cod', text='CÓD')
        self.produtos_arvore.heading('desc', text='DESCRIÇÂO')
        self.produtos_arvore.heading('qtd', text='QTD')

        self.botao_gerar_pdf = Button(self.janela_principal_frame, text='Gerar PDF', font=(self.fonte_padrao_texto), command= self._prepararListasImprimirPDF, width=15, bg='#282a7a', fg='white')

        self.titulo.grid(column=1, row=0, sticky='nsew', columnspan=5, padx=25, pady=25)
        codigo_cliente_label.grid(column=0, row=1, sticky='w', padx=5, pady=5)
        self.codigo_cliente_input.grid(column=1, row=1, sticky='nsew', padx=5, pady=5)
        self.codigo_cliente_botao.grid(column=2, row=1, sticky='w', padx=5, pady=5)

        cliente_label.grid(column=0, row=2, sticky='w', padx=5, pady=5)
        self.cliente_codigo_nome_texto.grid(column=1, row=2, columnspan=2 ,sticky='e', padx=5, pady=5)
        fantasia_label.grid(column=0, row=3, sticky='w', padx=5, pady=5)
        self.fantasia_texto.grid(column=1, row=3, columnspan=2 ,sticky='e', padx=5, pady=5)
        endereco_label.grid(column=0, row=4, sticky='w', padx=5, pady=5)
        self.endereco_texto.grid(column=1, row=4, columnspan=2 ,sticky='e', padx=5, pady=5)
        bairro_label.grid(column=0, row=5, sticky='w', padx=5, pady=5)
        self.bairro_texto.grid(column=1, row=5, columnspan=2 ,sticky='e', padx=5, pady=5)
        cidade_label.grid(column=0, row=6, sticky='w', padx=5, pady=5)
        self.cidade_texto.grid(column=1, row=6, columnspan=2 ,sticky='e', padx=5, pady=5)
        praca_label.grid(column=0, row=7, sticky='w', padx=5, pady=5)
        self.praca_texto.grid(column=1, row=7, columnspan=2 ,sticky='e', padx=5, pady=5)
        rota_label.grid(column=0, row=8, sticky='w', padx=5, pady=5)
        self.rota_texto.grid(column=1, row=8, columnspan=2 ,sticky='e', padx=5, pady=5)
        digitado_por_label.grid(column=0, row=9, sticky='w', padx=5, pady=5)
        self.digitado_por_texto.grid(column=1, row=9, columnspan=2 ,sticky='e', padx=5, pady=5)
        ref_label.grid(column=0, row=10, sticky='w', padx=5, pady=5)
        self.ref_texto.grid(column=1, row=10, columnspan=2 ,sticky='e', padx=5, pady=5)
        nf_label.grid(column=3, row=10, sticky='w', padx=5, pady=5)
        self.nf_texto.grid(column=4, row=10, sticky='e', padx=5, pady=5)
        obs_label.grid(column=0, row=11, sticky='w', padx=5, pady=5)
        self.obs_texto.grid(column=1, row=11, sticky='e', padx=5, pady=5, columnspan=2)

        adicionar_produto_botao.grid(column=1, row=12, sticky='nsew', padx=5, pady=5, columnspan=2)

        self.produtos_arvore.grid(column=0, row=14, sticky='nsew', padx=5, pady=5, columnspan=5)

        self.botao_gerar_pdf.grid(column=1, row=15, pady=10, sticky='nsew', columnspan=2)

        self.janela_principal_frame.pack()
    
    def _janelaAdicionarProduto(self):
        self.segunda_janela = Toplevel(self.tk)
        self.segunda_janela.title('Selecionar Produto')

        titulo_segunda_janela = Label(self.segunda_janela, text='Adicionar Produtos', font=(self.fonte_padrao_titulo))

        codigo_produto = Label(self.segunda_janela, text='Código produto: ', font=(None, 13))
        self.codigo_produto_input = Text(self.segunda_janela, height=1, width=25, font=(self.fonte_padrao_texto))
        self.codigo_produto_input.focus_set()
        self.codigo_produto_input.bind('<Return>', self._prevenirQuebraLinhaCodigoProdutoInput)
        self.buscar_produto = Button(self.segunda_janela, text='Buscar', width=13, command=self._buscarProduto, font=(self.fonte_padrao_texto), bg='#373aa3', fg='white')
 
        self.data_inicial_botao = Button(self.segunda_janela, text="Data Inicial", command=self._janelaSelecionarDataInicial, bg='#282a7a', fg='white')
        self.data_inicial_variavel = Text(self.segunda_janela, width=13, height=1, state='disabled', bg=self.background_campos, fg='black')

        self.data_final_botao = Button(self.segunda_janela, text="Data Final", command=self._janelaSelecionarDataFinal, bg='#282a7a', fg='white')
        self.data_final_variavel = Text(self.segunda_janela, width=13, height=1, state='disabled', bg=self.background_campos, fg='black')

        titulo_segunda_janela.grid(column=0, row=0, columnspan=5, pady=15, padx=5)
        codigo_produto.grid(column=1, row=1, pady=5, padx=5, sticky='e')
        self.codigo_produto_input.grid(column=2, row=1, pady=5, padx=5, sticky='nsew')
        self.buscar_produto.grid(column=3, row=1, pady=5, padx=5, sticky='w')
        self.data_inicial_botao.grid(column=1, row=2, sticky='e', pady=15, padx=5)
        self.data_inicial_variavel.grid(column=2, row=2, sticky='w', pady=15, padx=5)
        self.data_final_botao.grid(column=2, row=2, sticky='e', pady=15, padx=5)
        self.data_final_variavel.grid(column=3, row=2, sticky='w', pady=15, padx=5)

        columns = ('num_nota', 'cod_prod', 'descricao', 'data')

        self.tree = ttk.Treeview(self.segunda_janela, columns=columns, show='headings')
        self.tree.column(0, anchor="center")
        self.tree.column(1, anchor="center")
        self.tree.column(2, anchor="center")
        self.tree.column(3, anchor="center")

        self.tree.heading('num_nota', text='Nota Fiscal')
        self.tree.heading('cod_prod', text='Cod Produto')
        self.tree.heading('descricao', text='Produto')
        self.tree.heading('data', text='Data')

        self.tree.bind('<Double-1>', self._itemSelecionadoTree)

        self.tree.grid(row=4, column=0, sticky='nsew', columnspan=5, pady=2.5, padx=5)

        self.segunda_janela.bind('<Escape>', self._cancelarSelecionarProdutos)

        self._atualizarDataInicial()
        self._atualizarDataFinal()

        largura_janela = self.segunda_janela.winfo_reqwidth()
        altura_janela = self.segunda_janela.winfo_reqheight()

        self.segunda_janela.geometry(f'+{largura_janela+80}+{altura_janela-100}')
    
    def _janelaSelecionarDataInicial(self):
        self.janela_selecionar_data_inicial = Toplevel(self.tk)

        self.janela_selecionar_data_inicial.title("Selecione uma data")

        # Crie um widget de calendário na janela pop-up
        dia, mes, ano = self.data_inicial.split('/')
        self.calendario_data_inicial = Calendar(self.janela_selecionar_data_inicial, locale='pt_br', cursor="hand2", year=int(ano), month=int(mes), day=int(dia))
        inserir_data = Button(self.janela_selecionar_data_inicial, text="Inserir Data", command=self._inserirDataInicial, bg='#282a7a', fg='white')

        self.calendario_data_inicial.pack(padx=10, pady=10)
        inserir_data.pack(padx=10, pady=10)

        largura_janela = self.janela_selecionar_data_inicial.winfo_reqwidth()
        altura_janela = self.janela_selecionar_data_inicial.winfo_reqheight()

        self.janela_selecionar_data_inicial.geometry(f'+{largura_janela+300}+{altura_janela}')
    
    def _janelaSelecionarDataFinal(self):
        self.janela_selecionar_data_final = Toplevel(self.tk)

        self.janela_selecionar_data_final.title("Selecione uma data")

        # Crie um widget de calendário na janela pop-up
        dia, mes, ano = self.data_final.split('/')
        self.calendario_data_final = Calendar(self.janela_selecionar_data_final, locale='pt_br', cursor="hand2", year=int(ano), month=int(mes), day=int(dia))
        inserir_data = Button(self.janela_selecionar_data_final, text="Inserir Data", command=self._inserirDataFinal, bg='#282a7a', fg='white')

        self.calendario_data_final.pack(padx=10, pady=10)
        inserir_data.pack(padx=10, pady=10)

        largura_janela = self.janela_selecionar_data_final.winfo_reqwidth()
        altura_janela = self.janela_selecionar_data_final.winfo_reqheight()

        self.janela_selecionar_data_final.geometry(f'+{largura_janela+500}+{altura_janela}')
    
    def _janelaQuantidadeItem(self):
        self.janela_quantidade_motivo = Toplevel(self.tk)
        self.janela_quantidade_motivo.title("Quantidade")
        
        titulo = Label(self.janela_quantidade_motivo, text='Quantidade do Item: ', font=(self.fonte_padrao_titulo))

        item_selecionado = self.ultimo_produto_selecionado[2]
        item_texto = Label(self.janela_quantidade_motivo, text=item_selecionado, font=(None, 12, 'bold', 'underline'))
        
        quantidade = Label(self.janela_quantidade_motivo, text='Quantidade: ', font=(self.fonte_padrao_texto))
        self.quantidade_input = Text(self.janela_quantidade_motivo, height=1, width=10)
        self.quantidade_input.focus_set()
        self.quantidade_input.bind('<Return>', self._prevenirQuebraLinhaAdicionarMotivoQuantidade)
        self.quantidade_lista_input = ttk.Combobox(self.janela_quantidade_motivo, values=self.unidades_medida, width=10)
        self.quantidade_lista_input.set(self.unidades_medida[0])
        self.adicionar = Button(self.janela_quantidade_motivo, text='Adicionar', command=self._adicionarItemSelecionado, font=(self.fonte_padrao_texto), bg='#373aa3', fg='white')
        self.cancelar = Button(self.janela_quantidade_motivo, text='Cancelar', command=self._fecharJanelaQuantidadeItem, font=(self.fonte_padrao_texto), bg='#f53838', fg='white')

        titulo.grid(column=0, row=0, columnspan=3, pady=15, padx=5)
        item_texto.grid(column=0, row=1, columnspan=3, pady=15, padx=5)
        quantidade.grid(column=0, row=3, sticky='w', pady=2.5, padx=5)
        self.quantidade_input.grid(column=1, row=3, sticky='w', pady=2.5, padx=5)
        self.quantidade_lista_input.grid(column=2, row=3, sticky='e', pady=2.5, padx=5)
        self.adicionar.grid(column=1, row=4, sticky='nsew', pady=2.5, padx=5)
        self.cancelar.grid(column=2, row=4, sticky='nsew', pady=2.5, padx=5)

        self.janela_quantidade_motivo.bind('<Escape>', self._cancelarQuantidadeEscape)

        largura_janela = self.segunda_janela.winfo_reqwidth()
        altura_janela = self.segunda_janela.winfo_reqheight()
        self.janela_quantidade_motivo.geometry(f"+{largura_janela//2}+{altura_janela//2}")
    
    def _janelaErroRef(self):
        self.janela_erro_ref = Toplevel(self.tk)
        self.janela_erro_ref.title("ERRO")
        
        titulo = Label(self.janela_erro_ref, text='CAMPO REF ESTA VAZIO! ', font=(self.fonte_padrao_titulo))

        self.continuar = Button(self.janela_erro_ref, text='Continuar', command=self._fecharJanelaErroRef, font=(self.fonte_padrao_texto), bg='#373aa3', fg='white')
 
        self.continuar.focus_force()

        titulo.grid(column=0, row=0, columnspan=3, pady=15, padx=5)
        self.continuar.grid(column=1, row=4, sticky='nsew', pady=2.5, padx=5)

        self.continuar.bind('<Escape>', self._fecharJanelaErroRefEvento)
        self.continuar.bind('<Return>', self._fecharJanelaErroRefEvento)

        largura_janela = self.janela_principal_frame.winfo_reqwidth()
        altura_janela = self.janela_principal_frame.winfo_reqheight()
        self.janela_erro_ref.geometry(f"+{(largura_janela//2)+100}+{altura_janela//2}")
    
    def _janelaErroNotaFiscal(self):
        self.janela_erro_nf = Toplevel(self.tk)
        self.janela_erro_nf.title("ERRO")
        
        titulo = Label(self.janela_erro_nf, text='CAMPO NOTA FISCAL ESTA VAZIO! ', font=(self.fonte_padrao_titulo))

        self.continuar = Button(self.janela_erro_nf, text='Continuar', command=self._fecharJanelaErroNotaFiscal, font=(self.fonte_padrao_texto), bg='#373aa3', fg='white')
 
        self.continuar.focus_force()

        titulo.grid(column=0, row=0, columnspan=3, pady=15, padx=5)
        self.continuar.grid(column=1, row=4, sticky='nsew', pady=2.5, padx=5)

        self.continuar.bind('<Escape>', self._fecharJanelaErroNotaFiscalEvento)
        self.continuar.bind('<Return>', self._fecharJanelaErroNotaFiscalEvento)

        largura_janela = self.janela_principal_frame.winfo_reqwidth()
        altura_janela = self.janela_principal_frame.winfo_reqheight()
        self.janela_erro_nf.geometry(f"+{(largura_janela//2)+100}+{altura_janela//2}")