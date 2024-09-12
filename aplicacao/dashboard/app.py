#from shiny import App, ui

#app_ui = ui.page_fluid(
   # ui.panel_title("⚽ Macro Copa")
#)

#def server(input, output, session):
 #   ...
#app = App(app_ui,server)

#So consegui rodar com o comando abaixo 👇 
#shiny run --reload --launch-browser app.py

from shiny import App, ui, render
import pandas as pd
import plotnine as p9

#importação de dados
dados = (
    pd.read_csv("dados_disponibilizados.csv")
    .assign(
        data = lambda x: pd.to_datetime(x.data),
        index = lambda x: x.data
        )
    .set_index("index")
)

#objetos úteis para a interface do usuário/servidor
nomes_variaveis = dados.variavel.unique().tolist()
nomes_paises = dados.pais.unique().tolist()
datas = dados.data.dt.date

app_ui = ui.page_fluid(
    ui.page_navbar(  
        #ui.nav_panel("A", "Page A content"),  
        #ui.nav_panel("B", "Page B content"),  
        #ui.nav_panel("C", "Page C content"),  
        title="⚽ Macro Copa",  
        id="page",
        ),
    ui.page_sidebar( 
    ui.sidebar(
        ui.h5("Entra em campo a seleção de dados macroeconomicos!"),
        ui.p("Defina os times de países e indicadores, explore o jogo de visualizações e marque gol na análise de dados!"),
        ui.input_select(
            id="btn_variavel",
            label ="Selecione uma variável",
            choices=nomes_variaveis,
            selected="PIB (%, cresc. anual)",
            multiple=False
        ),
        ui.input_date_range(
            id = "btn_periodo",
            label = "Selecione o período (Filtre os anos)",
            start = "2000-01-01",
            end = datas.max(),
            min = datas.min(),
            max = datas.max(),
            format = "dd-mm-yyyy",
            startview = "year",
            language = "pt-BR",
            separator = "-"

        ),
        ui.input_radio_buttons(
            id = "btn_graphic_choices",
            label= "Selecione o tipo de gráfico",
            choices=["Gráfico de área","Gráfico de coluna","Gráfico de linha"],
            selected=[None]
        ),
        bg="#f8f8f8"
    ),
    ui.row(
        ui.column(
            6,
            ui.input_select(
                id="btn_pais_01",
                label ="Selecione o 1º pais",
                choices=nomes_paises,
                selected="Brazil",
                multiple=False
            )
        ),
        ui.column(
            6,
             ui.input_select(
                id="btn_pais_02",
                label ="Selecione o 2º pais",
                choices=nomes_paises,
                selected="Argentina",
                multiple=False
            )
        )
    ),
    ui.row(
        ui.column(
            6,
            ui.output_plot("plt_pais_01")
            ),
         ui.column(
            6,
            ui.output_plot("plt_pais_02")
            ),
    )       
    )  
)

# Parte 2: Lógica de Servidor:
def server(input, output, session):
    pass
    @output
    @render.plot
    def plt_pais_01():

        variavel_selecionada = input.btn_variavel()
        pais_selecionado = input.btn_pais_01()
        grafico_selecionado = input.btn_graphic_choices()
        data_inicial = input.btn_periodo()[0]
        data_final = input.btn_periodo()[1]
        

        df1 = dados.query("variavel == @variavel_selecionada and data >= @data_inicial and data <= @data_final and pais == @pais_selecionado")    

        plt1 = (
            p9.ggplot(data=df1)+
            p9.aes(x="data", y="valor")+
            p9.scale_x_date(date_labels = "%Y")+
            p9.ggtitle(pais_selecionado + " - " + variavel_selecionada)+
            p9.ylab("")+ 
            p9.xlab("Ano")+
            p9.labs(caption ="Dados: Banco Mundial | Elaboração: Guilherme")
        )
        if grafico_selecionado == "Gráfico de área":
            plt1 = (plt1 + p9.geom_area())
        elif grafico_selecionado == "Gráfico de coluna":
            plt1 = (plt1 + p9.geom_col())
        elif  grafico_selecionado == "Gráfico de linha":
            plt1 = (plt1 + p9.geom_line())
            
        return plt1
       
    
    @output
    @render.plot
    def plt_pais_02():

        variavel_selecionada = input.btn_variavel()
        pais_selecionado = input.btn_pais_02()
        grafico_selecionado = input.btn_graphic_choices()
        data_inicial = input.btn_periodo()[0]
        data_final = input.btn_periodo()[1]
        

        df2 = dados.query("variavel == @variavel_selecionada and data >= @data_inicial and data <= @data_final and pais == @pais_selecionado")    

        plt2 = (
            p9.ggplot(data=df2)+
            p9.aes(x="data", y="valor")+
            p9.scale_x_date(date_labels = "%Y")+
            p9.ggtitle(pais_selecionado + " - " + variavel_selecionada)+
            p9.ylab("")+ 
            p9.xlab("Ano")+
            p9.labs(caption ="Dados: Banco Mundial | Elaboração: Guilherme")
        )
        if grafico_selecionado == "Gráfico de área":
            plt2 = (plt2 + p9.geom_area())
        elif grafico_selecionado == "Gráfico de coluna":
            plt2 = (plt2 + p9.geom_col())
        elif  grafico_selecionado == "Gráfico de linha":
            plt2 = (plt2 + p9.geom_line())
            
        return plt2
        

    #pass


app = App(app_ui, server)

#Deploy para publicação
#rsconnect deploy shiny /path/to/app --name <NAME> --title my-app

# Deploy para publicação com poetry
#poetry run rsconnect deploy shiny aplicacao/dashboard/ --title poc-auto-python

# shiny run --reload
# rsconnect deploy shiny . --title poc-shiny-python