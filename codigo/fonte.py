import urllib
import requests
import re

data = '03/10/2018'
parametrosUrlBuscaDiario = {
    'action': 'buscarDiarios',
    'voDiarioSearch.tribunal': 'TSE',
    'page': 'diarioPageTextualList.jsp',
    'voDiarioSearch.tribunal': 'TSE',
    'voDiarioSearch.livre': '',
    'voDiarioSearch.numero': '',
    'voDiarioSearch.ano': '',
    'voDiarioSearch.dataPubIni': data,
    'voDiarioSearch.dataPubFim': data
}

parametrosToUrlEncoded = urllib.parse.urlencode(parametrosUrlBuscaDiario)

urlBuscaDiario = 'http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diarioTxt.do'
respostaHtmlBuscaDiario = requests.get(urlBuscaDiario, params=parametrosToUrlEncoded)
conteudoBusca = respostaHtmlBuscaDiario.content

regexBuscaIdDiario = re.findall(r'(?<=chamarCaptcha\()(.*)(?=,)', str(conteudoBusca))
if regexBuscaIdDiario == []:
    print('Nenhum caderno encontrado para a data indicada')
    SystemExit

for index, diarioId in enumerate(regexBuscaIdDiario):
    parametrosUrlBaixaDiario = urllib.parse.urlencode({
        'action': 'downloadDiario',
        'pergunta': '',
        'captchaValidacao': 'ok',
        'resposta': '',
        'id': diarioId, 'tribunal': 'TSE'})

    respostaUrlBaixaDiario = requests.get('http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diario.do', params=parametrosUrlBaixaDiario)
    data = data.replace('/', '-')
    with open('../cadernos/{}-{}'.format(data, index+1), 'wb') as file:
        for parte in respostaUrlBaixaDiario.iter_content(chunk_size=128):
            file.write(parte)
