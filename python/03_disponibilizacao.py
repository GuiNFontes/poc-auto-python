# Importar as biibliotecas -------
import pandas as pd
from sqlite3 import connect

# Conexão com o Banco de dados SQLite
conexao_sql = connect(database = "dados/dados.db")

# Coleta de dados tratados
tbl_tratados = pd.read_sql_query("SELECT * FROM tbl_tratados", con=conexao_sql)


#Salvar tabela como um arquivo csv
tbl_tratados.to_csv(path_or_buf="aplicacao/dashboard/dados_disponibilizados.csv",index=False)



#-----------------------------------------------------------------

#Códigos abaixo foram realizados no arquivo etl.py antes de separar as etapas(Extração>Transformação>Disponibilização), utilizando banco de dados SQL

# Salvar dados -----

# Salva arquivo CSV
#if not os.path.exists("dados"): os.mkdir("dados")
#dados.to_csv(path_or_buf = "dados/dados.csv", index = False)