import urllib
import requests
import re
import hashlib
import os


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


def FazDownloadDiarios(listaDiariosId, dataDiarios):

    listaNome = []
    for index, diarioId in enumerate(listaDiariosId):
        parametrosUrlBaixaDiario = {
            'action': 'downloadDiario',
            'pergunta': '',
            'captchaValidacao': 'ok',
            'resposta': '',
            'id': diarioId, 'tribunal': 'TSE'}

        parametrosUrlBaixaDiario = urllib.parse.urlencode(parametrosUrlBaixaDiario)
        respostaUrlBaixaDiario = requests.get('http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diario.do', params=parametrosUrlBaixaDiario)
        nomeDiario = dataDiarios.replace('/', '-')
        if index == 0:
            nomePasta = '../cadernos/{}'.format(nomeDiario)
            listaNome.append(nomePasta)
            if os.path.isdir('../cadernos/{}'.format(nomePasta)) is True:
                print("Já existe uma pasta para essa data, para tentar novamente a apague: {}".format(nomePasta))
                SystemExit
            else:
                os.mkdir(nomePasta)

        nomeDiario = '{}-{}'.format(nomeDiario, index+1)
        listaNome.append(nomeDiario)
        with open('{}/{}'.format(nomePasta, nomeDiario), 'wb') as arquivo:
            for parte in respostaUrlBaixaDiario.iter_content(chunk_size=1024):
                arquivo.write(parte)
        arquivo.close()
    return listaNome


def FazHashDiarios(listaNome):
    md5Hash = hashlib.md5()
    for index, nomeDiario in enumerate(listaNome):
        if index == len(listaNome) - 1:
            break
        with open('{}/{}'.format(listaNome[0], listaNome[index+1]), 'rb') as arquivo:
            while True:
                parte = arquivo.read(1024)
                if parte == b'':
                    break
                else:
                    md5Hash.update(parte)
        with open('{}-hash'.format(listaNome[0], listaNome[0]), 'a+') as arquivo:
            hexadecimalHash = md5Hash.hexdigest()
            arquivo.write(hexadecimalHash)
            arquivo.write('\n')
        arquivo.close()


dataDiarios = input("Entre com uma data no formato: dd/mm/aaaa: ")
listaIdDiarios = BuscaIdDiarios(dataDiarios)
if not listaIdDiarios:
    print("Nenhum diário foi encontrado para a data {}".format(dataDiarios))
    SystemExit
else:
    listaNome = FazDownloadDiarios(listaIdDiarios, dataDiarios)
    if not listaNome:
        print("Falha ao tentar fazer downloads dos diários para a data {}".format(dataDiarios))
        SystemExit
    else:
        FazHashDiarios(listaNome)
