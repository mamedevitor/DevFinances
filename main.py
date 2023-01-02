from PyQt5 import uic, QtWidgets
from PyQt5 import QtCore
from datetime import date

import sqlite3

# Conectando ao Banco SQLITE
banco = sqlite3.connect('easy_finances.db')

cursor = banco.cursor()
# Pegando da tabela valores_Cards do Banco
cursor.execute('SELECT * FROM valores_cards')
banco_dados = cursor.fetchall()

# Pegando da tabela transaçoes do Banco
cursor.execute('SELECT * FROM transaçoes')
banco_transaçoes = cursor.fetchall()
banco.commit()


class FrmPrincial:
    def __init__(self):
        # Definindo dados['saldo']
        dados['saldo'] = 0

        # Fazendo os calculos dos cards
        if banco_dados != '':
            global banco_transaçoes
            saldo = int(banco_dados[0][0])
            dados['saldo'] = saldo

            for dado in banco_transaçoes:
                if dado[3] == 2:
                    gastos_saidas.append(dado[1])

            frm_principal.lblsaidas.setText(lang.toString(sum(gastos_saidas) * 0.01, 'f', 2))
            frm_principal.lbltotal.setText(lang.toString((dados['saldo'] - sum(gastos_saidas)) * 0.01, 'f', 2))
            frm_principal.lblentrada.setText(lang.toString(saldo * 0.01, 'f', 2))

        # Exibindo FrmPrincipal
        frm_principal.show()

        # Definindo largura de cada coluna da Tabela
        frm_principal.tabela.setColumnWidth(0, 309)
        frm_principal.tabela.setColumnWidth(1, 115)
        frm_principal.tabela.setColumnWidth(2, 115)

        # Deixando invisivel a coluna numérica da esquerda
        frm_principal.tabela.verticalHeader().setVisible(False)

        # insirindo data atual
        frm_remover_alterar_transacao.data.setDate(data_atual)
        frm_transacoes.textdata.setDate(data_atual)

        cursor.execute('SELECT * FROM transaçoes')
        banco_transaçoes = cursor.fetchall()

        # Variável das linhas da tabela
        row = 0

        # Colunas serão igual ao total de dados na Lista dados copy
        frm_principal.tabela.setRowCount(len(banco_transaçoes))

        for item in banco_transaçoes:

            valor = lang.toString(int(item[1]) * 0.01, 'f', 2)

            if item[3] == 1:
                frm_principal.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                frm_principal.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem('+' + valor))
                frm_principal.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(item[2]))
                row += 1

            elif item[3] == 2:
                frm_principal.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                frm_principal.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem('-' + valor))
                frm_principal.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(item[2]))
                row += 1

            frm_remover_alterar_transacao.selecionar_item.addItem(item[0])

        # Botões do FrmPrincipal
        frm_principal.btntransactions.clicked.connect(FrmPrincial.btn_transactions_clicked)
        frm_principal.btn_sair.clicked.connect(FrmPrincial.sair)
        frm_principal.btnremover.clicked.connect(FrmPrincial.btn_remover_alterar_clicked)

        # Chamando FrmRemover_Alterar
        FrmRemover_Alterar()

    def sair(self):
        frm_principal.close()
        frm_transacoes.close()
        frm_remover_alterar_transacao.close()

    def FecharTransactions(self):
        # Fechando FrmTransactions
        frm_transacoes.close()

        # Limpando as Linhas Descrição, Valor e Data
        frm_transacoes.textdescricao.clear()
        frm_transacoes.textvalor.clear()
        frm_transacoes.textdata.clear()

    def btn_transactions_clicked(self):
        # Abrindo FrmTransactions
        frm_transacoes.show()

        # Cliques dos Botões do Formulário
        frm_transacoes.btncancelar.clicked.connect(FrmPrincial.FecharTransactions)
        frm_transacoes.btnsalvar.clicked.connect(FrmPrincial.transactions)

        # Colocando cor Padrão das Mensagens de Erro e da Borda das Linhas
        frm_transacoes.textdescricao.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 2px; border 2px solid white")
        frm_transacoes.textvalor.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 2px; border: 2px solid white;")
        frm_transacoes.lblerror.setStyleSheet('color: rgb(240, 242, 245);')

    def btn_remover_alterar_clicked(self):
        # Abrindo FrmRemover/Alterar Transactions
        frm_remover_alterar_transacao.show()

    def transactions(self):

        # Definindo os Valores Digitados
        dados["descricao"] = frm_transacoes.textdescricao.text()
        dados["valor"] = frm_transacoes.textvalor.text()
        dados["data"] = frm_transacoes.textdata.text()

        # Colocando o valor do dados['valor'] na variálvel valor
        valor = frm_transacoes.textvalor.text()

        # Verificando se a Linha Descrição está vazia
        if frm_transacoes.textdescricao.text().strip() == "":
            frm_transacoes.textdescricao.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 2px; border: 2px solid red;")

        # Verificando se a Linha Valor está vazia
        elif frm_transacoes.textvalor.text().strip() == "":
            frm_transacoes.textvalor.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 2px; border: 2px solid red;")

        # Verificando se A ponto ou virgula na Linha Valor
        elif valor.count(',') or valor.count('.') > 0:
            frm_transacoes.lblerror.setText('Não insira ponto ou virgula!')
            frm_transacoes.lblerror.setStyleSheet('color: red;')

        # Verificando se a Linha valor é um número
        elif not valor.isnumeric():
            frm_transacoes.lblerror.setText('Insira apenas números!')
            frm_transacoes.lblerror.setStyleSheet('color: red;')

        else:

            # Transformando linhaValor em um número Inteiro
            valor = int(frm_transacoes.textvalor.text())

            # Adicionando variável valor no dados['valor']
            dados["valor"] = valor

            # Adicionando dados do dicionário na Lista dadoscopy
            dadoscopy.append(dados.copy())

            # Colunas serão igual ao total de dados na Lista dados copy
            frm_remover_alterar_transacao.selecionar_item.addItem(dados['descricao'])
            for dado in dadoscopy:
                descri = dado['descricao']
                value = dado['valor']
                data = dado['data']



                if frm_transacoes.check_ganho.isChecked() == True:

                    cursor.execute(f"INSERT INTO transaçoes VALUES ('{descri}', '{value}', '{data}', {'1'})")
                    banco.commit()

                    cursor.execute('SELECT * FROM valores_cards')
                    banco_dados = cursor.fetchall()

                    saldo = int(banco_dados[0][0]) + value
                    dados['saldo'] = saldo
                    cursor.execute(f"UPDATE valores_cards set entrada = '{saldo}'")
                    banco.commit()

                if frm_transacoes.check_despesa.isChecked() == True:

                    cursor.execute(f"INSERT INTO transaçoes VALUES ('{descri}', '{value}', '{data}', {'2'})")
                    banco.commit()

                    # Adicionado variável valor na lista Gastos_Saídas
                    gastos_saidas.append(value)
                dadoscopy.clear()

            cursor.execute('SELECT * FROM transaçoes')
            banco_transaçoes = cursor.fetchall()

            # Fazendo os calculos da lblTotal_Saídas, lblTotal_Final
            frm_principal.lblentrada.setText(lang.toString(dados['saldo'] * 0.01, 'f', 2))
            frm_principal.lblsaidas.setText(lang.toString(sum(gastos_saidas) * 0.01, 'f', 2))
            frm_principal.lbltotal.setText(lang.toString((dados['saldo'] - sum(gastos_saidas)) * 0.01, 'f', 2))

            cursor.execute(f"UPDATE valores_cards set saida = '{sum(gastos_saidas)}'")
            banco.commit()

            row = 0

            frm_principal.tabela.setRowCount(len(banco_transaçoes))

            for item in banco_transaçoes:

                valor = lang.toString(int(item[1]) * 0.01, 'f', 2)

                if item[3] == 1:

                    # Adicionando os dados Digitados na Tabela no FrmPrincipal
                    frm_principal.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(item[0]))
                    frm_principal.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem('+' + valor))
                    frm_principal.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(item[2]))
                    row += 1

                elif item[3] == 2:
                    # Adicionando os dados Digitados na Tabela no FrmPrincipal
                    frm_principal.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(item[0]))
                    frm_principal.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem('-' + valor))
                    frm_principal.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(item[2]))
                    row += 1

            # Limpando as linhas de Texto
            frm_transacoes.textdescricao.clear()
            frm_transacoes.textvalor.clear()


class FrmRemover_Alterar:
    def __init__(self):
        # Cliques dos Botões
        frm_remover_alterar_transacao.btn_ok.clicked.connect(FrmRemover_Alterar.ok_clicked_Alterar)
        frm_remover_alterar_transacao.btnremover.clicked.connect(FrmRemover_Alterar.remover_dados)
        frm_remover_alterar_transacao.btnalterar.clicked.connect(FrmRemover_Alterar.alterar_dados)

    def remover_dados(self):
        # Variável item armazena o texto da ComboBox

        item = frm_remover_alterar_transacao.selecionar_item.currentText()

        # Limpando as Linhas
        frm_remover_alterar_transacao.textdescricao.clear()
        frm_remover_alterar_transacao.textvalor.clear()

        if item != '':

            cursor.execute('SELECT * FROM valores_cards')
            banco_dados = cursor.fetchall()

            cursor.execute('SELECT * FROM transaçoes')
            banco_transaçoes = cursor.fetchall()

            for id, dado in enumerate(banco_transaçoes):
                saldo = banco_dados[0][0]
                if dado[0] == item:
                    if dado[3] == 2:

                        gastos_saidas.remove(int(dado[1]))

                    if dado[3] == 1:
                        saldo -= int(dado[1])
                        cursor.execute(f"UPDATE valores_cards set entrada ='{saldo}'")
                        banco.commit()
                        dados['saldo'] = saldo

                    cursor.execute(f"DELETE FROM transaçoes WHERE descricao ='{dado[0]}'")
                    banco.commit()

                    # Removendo coluna da Tabela do FrmPrincipal
                    frm_principal.tabela.removeRow(id)
                    frm_remover_alterar_transacao.selecionar_item.removeItem(frm_remover_alterar_transacao.selecionar_item.currentIndex())


                cursor.execute('SELECT * FROM valores_cards')
                banco_dado = cursor.fetchall()

                frm_principal.lblentrada.setText(lang.toString(banco_dado[0][0] * 0.01, 'f', 2))
                frm_principal.lbltotal.setText(lang.toString((dados['saldo'] - sum(gastos_saidas)) * 0.01, 'f', 2))
                frm_principal.lblsaidas.setText(lang.toString(sum(gastos_saidas) * 0.01, 'f', 2))

                cursor.execute(f"UPDATE valores_cards set saida = '{sum(gastos_saidas)}' ")
                banco.commit()

    def alterar_dados(self):

        global valors
        item_combobox = frm_remover_alterar_transacao.selecionar_item.currentText()

        cursor.execute("SELECT * FROM transaçoes")
        banco_transaçoes = cursor.fetchall()

        if FrmRemover_Alterar.ok_clicked_Alterar and item_combobox != '' and frm_remover_alterar_transacao.textdescricao.text() != '' and frm_remover_alterar_transacao.textvalor.text() != '':

            nova_descri = frm_remover_alterar_transacao.textdescricao.text()
            novo_valor = int(frm_remover_alterar_transacao.textvalor.text())
            nova_data = frm_remover_alterar_transacao.data.text()

            for id, i in enumerate(banco_transaçoes):

                if item_combobox == i[0]:

                    frm_remover_alterar_transacao.selecionar_item.removeItem(
                        frm_remover_alterar_transacao.selecionar_item.currentIndex())
                    frm_remover_alterar_transacao.selecionar_item.addItem(nova_descri)

                    if frm_remover_alterar_transacao.check_ganho.isChecked() == True:

                        if i[1] in gastos_saidas:
                            gastos_saidas.remove(i[1])
                        else:
                            dados['saldo'] -= i[1]

                        valor_saldo = dados['saldo']

                        cursor.execute(f"UPDATE valores_cards set entrada = '{valor_saldo}', saida = '{sum(gastos_saidas)}'")
                        banco.commit()

                        cursor.execute(f"UPDATE transaçoes set descricao = '{nova_descri}', valor = '{novo_valor}', data = '{nova_data}', ganho_despesa = '1' WHERE descricao = '{item_combobox}'")
                        banco.commit()

                        row = id

                        frm_principal.tabela.setRowCount(len(banco_transaçoes))

                        v = lang.toString(int(novo_valor) * 0.01, 'f', 2)

                        frm_principal.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(nova_descri))
                        frm_principal.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem('+' + v))
                        frm_principal.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(nova_data))
                        row += 1

                        # Limpando as Linhas
                        frm_remover_alterar_transacao.textdescricao.clear()
                        frm_remover_alterar_transacao.textvalor.clear()

                    if frm_remover_alterar_transacao.check_despesa.isChecked() == True:

                        gastos_saidas.append(i[1])
                        dados['saldo'] -= i[1]
                        valor = dados['saldo']

                        cursor.execute(f"UPDATE valores_cards set entrada = '{valor}'")
                        banco.commit()

                        cursor.execute(
                            f"UPDATE transaçoes set descricao = '{nova_descri}', valor = '{novo_valor}', data = '{nova_data}', ganho_despesa = '2' WHERE descricao = '{item_combobox}'")
                        banco.commit()

                        # Variável das linhas da tabela
                        row = id
                        # Colunas serão igual ao total de dados na Lista dados copy
                        frm_principal.tabela.setRowCount(len(banco_transaçoes))

                        v = lang.toString(int(novo_valor) * 0.01, 'f', 2)

                        # Adicionando os dados Digitados na Tabela no FrmPrincipal
                        frm_principal.tabela.setItem(row, 0, QtWidgets.QTableWidgetItem(nova_descri))
                        frm_principal.tabela.setItem(row, 1, QtWidgets.QTableWidgetItem("-" + v))
                        frm_principal.tabela.setItem(row, 2, QtWidgets.QTableWidgetItem(nova_data))
                        row += 1

                    cursor.execute("SELECT * FROM transaçoes")
                    banco_transaçoes = cursor.fetchall()

                    valors.clear()
                    gastos_saidas.clear()
                    for i in banco_transaçoes:
                        if i[3] == 1:
                            valors.append(i[1])
                        if i[3] == 2:
                            gastos_saidas.append(i[1])
                    saldo = sum(valors)
                    # Informando que agora dados['saldo'] é igual a variável saldo
                    dados['saldo'] = saldo

                    cursor.execute(f"UPDATE valores_cards set entrada = '{saldo}'")
                    banco.commit()

                    frm_principal.lblentrada.setText(lang.toString(dados["saldo"] * 0.01, 'f', 2))
                    frm_principal.lblsaidas.setText(lang.toString(sum(gastos_saidas) * 0.01, 'f', 2))
                    frm_principal.lbltotal.setText(lang.toString((saldo - sum(gastos_saidas)) * 0.01, 'f', 2))

                    cursor.execute(f"UPDATE valores_cards set saida = '{sum(gastos_saidas)}'")
                    banco.commit()

    def ok_clicked_Alterar(self):
        # Variável item é igual ao texto selecionado na ComboBox
        item = frm_remover_alterar_transacao.selecionar_item.currentText()

        cursor.execute('SELECT * FROM transaçoes')
        banco_transaçoes = cursor.fetchall()


        # Pegando cada dado da Lista dadoscopy
        for dado in banco_transaçoes:

            # Verificando se o item está nos dado['Descricao']
            if item == dado[0]:
                # colocando os dados nas Linhas de Textos
                frm_remover_alterar_transacao.textdescricao.setText(str(dado[0]))
                frm_remover_alterar_transacao.textvalor.setText(str(dado[1]))


if __name__ == '__main__':
    # Variáveis,Listas e Dicionário
    dados = {}
    data_atual = date.today()
    dadoscopy = []

    loc = QtCore.QLocale.system().name()
    lang = QtCore.QLocale(loc)
    gastos_saidas = []

    valors = list()

    # Configurando Aplicação
    app = QtWidgets.QApplication([])
    frm_principal = uic.loadUi("View/frm_principal.ui")
    frm_saldo = uic.loadUi("View/frm_saldo.ui")
    frm_transacoes = uic.loadUi("View/frm_transacoes.ui")
    frm_remover_alterar_transacao = uic.loadUi("View/frm_remover_alterar_transaçoes.ui")

    # Exibindo FrmPrincipal
    FrmPrincial()

    # inicialiando Aplicação
    app.exec()
