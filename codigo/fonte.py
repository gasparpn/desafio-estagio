import urllib
import requests
import re
import hashlib


def BuscaIdDiarios(data):
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
    regexBuscaIdDiario = re.findall(r'(?<=chamarCaptcha\()(.*?)(?=,)', str(conteudoBusca))

    return regexBuscaIdDiario


def FazHashDiarios(listaDiariosId, dataDiarios):

    md5Hash = hashlib.md5()
    for index, diarioId in enumerate(listaDiariosId):
        parametrosUrlBaixaDiario = {
            'action': 'downloadDiario',
            'pergunta': '',
            'captchaValidacao': 'ok',
            'resposta': '',
            'id': diarioId, 'tribunal': 'TSE'}

        parametrosUrlBaixaDiario = urllib.parse.urlencode(parametrosUrlBaixaDiario)
        urlBaixaDiarios = 'http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diario.do'
        respostaUrlBaixaDiario = requests.get(urlBaixaDiarios, params=parametrosUrlBaixaDiario)

        nomeDiario = dataDiarios.replace('/', '-')

        with open('../cadernos/{}'.format(nomeDiario), 'a+') as arquivo:
            for parte in respostaUrlBaixaDiario.iter_content(chunk_size=1024):
                md5Hash.update(parte)
            hexadecimalHash = md5Hash.hexdigest()
            arquivo.write(hexadecimalHash)
            arquivo.write('\n')


dataDiarios = input("Entre com uma data no formato: dd/mm/aaaa: ")
listaIdDiarios = BuscaIdDiarios(dataDiarios)
if not listaIdDiarios:
    print("Nenhum diário foi encontrado para a data {}".format(dataDiarios))
    SystemExit
else:
    FazHashDiarios(listaIdDiarios, dataDiarios)
