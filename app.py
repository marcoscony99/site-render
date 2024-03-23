from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Olá, <b>tudo bem</b>?"

@app.route('/teste')
def teste():
    return "Essa página é um <b>teste do novo comando</b>."

@app.route('/nome')
def nome():
    return 'Digite seu nome: <form method="post"><input type="text" name="nome"><input type="submit" value="Enviar"></form>'

from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Instalação das bibliotecas necessárias
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])

@app.route('/dados')
def obter_dados_bioma():
    def obter_html(url):
        req = requests.get(url)
        html = req.content
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def raspar_dados_bioma(soup, row, col):
        celulas_coluna = soup.findAll('td', {'class': f'data row{row} col{col}'})
        valores_coluna = [celula.text.strip() for celula in celulas_coluna]
        return valores_coluna[0] if valores_coluna else None

    url = 'http://terrabrasilis.dpi.inpe.br/queimadas/situacao-atual/media/bioma/grafico_historico_mes_atual_estado_amazonia.html'
    soup = obter_html(url)

    data_atual = datetime.now()
    dia_do_mes = data_atual.day

    focos_24h = raspar_dados_bioma(soup, 1, dia_do_mes-2)
    acumulado_mes_atual_bioma = raspar_dados_bioma(soup, 1, 31)
    total_mesmo_mes_ano_passado_bioma = raspar_dados_bioma(soup, 0, 31)

    mapping_meses = {
        'janeiro': 0,
        'fevereiro': 1,
        'março': 2,
        'abril': 3,
        'maio': 4,
        'junho': 5,
        'julho': 6,
        'agosto': 7,
        'setembro': 8,
        'outubro': 9,
        'novembro': 10,
        'dezembro': 11
    }

    mes_atual = datetime.now().month
    nome_mes_atual = None
    for mes, numero in mapping_meses.items():
        if numero == mes_atual - 1:
            nome_mes_atual = mes

    def encontrar_media_e_recorde_mensal(soup, mes_solicitado):
        quantidade_linhas = 27

        if mes_solicitado.lower() in mapping_meses:
            mes_index = mapping_meses[mes_solicitado.lower()]

        celulas_mensal = soup.findAll('td', {'class': f'data row28 col{mes_index}'})
        valores_mensal = [int(celula.text.strip()) for celula in celulas_mensal if celula.text.strip().isdigit()]

        if valores_mensal:
            media_mensal = sum(valores_mensal) / len(valores_mensal)
            resultado_media = f'Média do mês - {int(media_mensal)} focos\n'

        lista_mensal = []
        for y in range(quantidade_linhas):
            celulas_mensal = soup.findAll('td', {'class': f'data row{y} col{mes_index}'})
            valores_mensal = [int(celula.text.strip()) for celula in celulas_mensal if celula.text.strip().isdigit()]
            lista_mensal.extend(valores_mensal)

        if lista_mensal:
            maior_valor_mensal = max(lista_mensal)
            ano_do_recorde_mensal = 1999 + lista_mensal.index(maior_valor_mensal)
            if mes_index >= 5:
                ano_do_recorde_mensal = ano_do_recorde_mensal - 1
            resultado_recorde = f'Recorde do mês - {maior_valor_mensal} focos (no ano {ano_do_recorde_mensal})\n'

        return resultado_media, resultado_recorde

    url2 = 'http://terrabrasilis.dpi.inpe.br/queimadas/situacao-atual/media//bioma/grafico_historico_estado_amazonia.html'
    soup = obter_html(url2)

    media, recorde = encontrar_media_e_recorde_mensal(soup, nome_mes_atual)
    return f"24h - {focos_24h} focos<br>Acumulado do mês atual - {acumulado_mes_atual_bioma} focos (vs {total_mesmo_mes_ano_passado_bioma} focos totais no mesmo mês do ano passado)<br>{media}<br>{recorde}"

if __name__ == "__main__":
    app.run(debug=True)