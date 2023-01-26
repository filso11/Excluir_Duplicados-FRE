import fdb

# Conecta no BD
con = fdb.connect(
    dsn='localhost:C:/FREACCESSCOND.GDB',
    user='SYSDBA',
    password='masterkey'
)

# Variaveis de select
SELECTDUPLICADOS = (
    "SELECT VTE_NOME FROM VISITANTE GROUP BY VTE_NOME HAVING COUNT(VTE_NOME) > 1")
SELECT_VISITANTE = ("SELECT VTE_ID,VTE_NOME FROM VISITANTE")

# Cria o cursor
cur = con.cursor()

# Roda a query no BD
cur.execute(SELECT_VISITANTE)
visitante = cur.fetchall()
cur.execute(SELECTDUPLICADOS)
duplicados = cur.fetchall()

# variavel que armazenas cadastros duplicados com seus ID's
visitantesDuplicados = []

for i in range(len(visitante)):
    teste = visitante[i][1]
    for c in range(len(duplicados)):
        teste2 = duplicados[c]
        if teste in teste2:
            visitantesDuplicados.append(visitante[i])

# Funções


def deletaVisitante(id):

    # VARS

    sqluPessoaIdentificador = (
        f"UPDATE PESSOA_IDENTIFICADOR SET PSI_STATUS = 'I' WHERE PSI_USER_ID = {id} AND PSI_TIPOPESSOA = 'E' ")
    sqluPessoaNivel = (
        f"UPDADE PESSOA_NIVEL SET PNV_STATUS = 'I' WHERE PNV_USER_ID = {id} AND PNV_TIPOUSER = 'E' ")
    sqldPessoaIdentificador = (
        f"DELETE FROM PESSOA_IDENTIFICADOR WHERE PSI_USER_ID = {id} AND PSI_TIPOPESSOA = 'E' ")
    sqldImagens = (
        f"DELETE FROM IMAGENS WHERE IMG_CODUSER = {id} AND IMG_INDTIPOUSER = 'E' ")
    sqldPessoaNivel = (
        f"DELETE FROM PESSOA_NIVEL WHERE PNV_USER_ID = {id} AND PNV_TIPOUSER = 'E' ")
    sqldBiometria = (
        f"DELETE FROM BIOMETRIA WHERE BIO_USER_ID = {id} AND BIO_TIPOUSER = 'E' ")
    sqlsVisita = (f"SELECT VTA_ID FROM VISITA WHERE VTA_VTE_ID = {id} ")
    sqldVisita = (f"DELETE FROM VISITA WHERE VTA_VTE_ID = {id}")
    sqldVisitante = (f"DELETE FROM VISITANTE WHERE VTE_ID = {id}")

    # Update Pessoa Identificador
    cur.execute(sqluPessoaIdentificador)

    # Delete Pessoa Nivel
    cur.execute(sqldPessoaNivel)

    # Delete Pessoa Identificador
    cur.execute(sqldPessoaIdentificador)

    # Delete Imagens
    cur.execute(sqldImagens)

    # Delete Biometria
    cur.execute(sqldBiometria)

    # Select Visita and Fetchall

    cur.execute(sqlsVisita)
    visita = cur.fetchall()
    lvisita = []

    for a in range(len(visita)):
        lvisita.append(visita[a])

    for b in range(len(lvisita)):
        cur.execute(
            f"DELETE FROM VISITAPROPRIEDADE WHERE VPD_VTA_ID = {lvisita[b][0]}")
    for c in range(len(lvisita)):
        cur.execute(
            f"DELETE FROM VISITA_ACOMPANHANTE WHERE VAC_VTA_ID = {lvisita[c][0]}")

    # Delete Visita
    cur.execute(sqldVisita)

    # Delete Visitante
    cur.execute(sqldVisitante)


repetidos = []

for itens in range(len(visitantesDuplicados)):
    for itens2 in range(itens + 1, len(visitantesDuplicados)):
        if visitantesDuplicados[itens2][1] == visitantesDuplicados[itens][1]:
            if visitantesDuplicados[itens2][0] not in repetidos:
                repetidos.append(visitantesDuplicados[itens2][0])

repetidos.sort()
for i in range(len(repetidos)):
    deletaVisitante(repetidos[i])
    print(f"ID EXCLUIDO = {repetidos[i]}")

# Fecha o cursor e a conexão
cur.close()
con.commit()
con.close()