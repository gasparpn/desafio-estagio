import urllib
import requests
import re
import hashlib
import sys


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

    try:
        parametrosToUrlEncoded = urllib.parse.urlencode(parametrosUrlBuscaDiario)
        urlBuscaDiario = 'http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diarioTxt.do'
        respostaHtmlBuscaDiario = requests.get(urlBuscaDiario, params=parametrosToUrlEncoded)
        conteudoBusca = respostaHtmlBuscaDiario.content
        regexBuscaIdDiario = re.findall(r'(?<=chamarCaptcha\()(.*?)(?=,)', str(conteudoBusca))
        return regexBuscaIdDiario
    except requests.exceptions.RequestException as httpError:
        print(httpError)
        sys.exit(1)
    except:
        print("Um erro inesperado ocorreu:{}".format(sys.exc_info()[0]))
        sys.exit(1)


def FazHashDiarios(listaDiariosId, dataDiarios):

    try:
        md5Hash = hashlib.md5()
        nomeDiario = dataDiarios.replace('/', '-')
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

            with open('../hash/{}'.format(nomeDiario), 'a+') as arquivo:
                for parte in respostaUrlBaixaDiario.iter_content(chunk_size=1024):
                    md5Hash.update(parte)
                hexadecimalHash = md5Hash.hexdigest()
                arquivo.write(hexadecimalHash)
                arquivo.write('\n')
        print("Os hashs foram salvos no arquivo {} na pasta hash".format(nomeDiario))
    except IOError as ioError:
        print(ioError)
        sys.exit(1)
    except requests.exceptions.RequestException as httpError:
        print(httpError)
        sys.exit(1)
    except:
        print("Um erro inesperado ocorreu:{}".format(sys.exc_info()[0]))
        sys.exit(1)


dataDiarios = input("Entre com uma data no formato: dd/mm/aaaa: ")
print("Aguarde...")
listaIdDiarios = BuscaIdDiarios(dataDiarios)
if not listaIdDiarios:
    print("Nenhum diário foi encontrado para a data {}".format(dataDiarios))
    SystemExit
else:
    FazHashDiarios(listaIdDiarios, dataDiarios)
