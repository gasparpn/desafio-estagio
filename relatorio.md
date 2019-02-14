Primeiro dia – 12/02: 
Após ler o desafio tentei identificar o que eu precisava aprender e os problemas que eu iria precisar resolver para se chegar a solução. A se aprender identifiquei:
- Como a função MD5 funciona
- Entender o básico de como “quebrar” captcha
- Manipulação de PDF utilizando python

Os problemas que consegui encontrar foram:
- Tentar encontrar um padrão nas perguntas geradas pelo captcha do site indicado.
	Ao fazer algumas requisições utilizando o navegador e verificando o código fonte e devtools vi que na página principal havia um [iframe](http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/) que englobava a página  e no javascript desta havia a função chamarCaptcha que “chama” o captcha através de um [POST](http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/captcha.do) e a resposta a pergunta recebida é feita também por um POST, tendo como content-type ‘application/x-www-form-urlencoded; utf-8’ e os parâmetros eram: resposta e pergunta.
	Dessa forma, me propus a utilizar um meio externo, que não o browser, para fazer as requisições e analisar as respostas. Minha intenção foi encontrar um padrão nas perguntas e respostas e verificar como iria precisar fazer o post (já que terei de fazer isso no programa em python).
Encontrei um padrão nas perguntas e respotas e a solução imediata que pensei foi criar um dicionário que tem um padrão como chave e indica uma forma de tratamento no campo valor.
Utilizei como fonte de pesquisa: [Curl](https://gist.github.com/subfuzion/08c5d85437d5d4f00e58)

- Um outro problema que enfrentei foi como encriptar o pdf. Pesquisando encontrei o seguinte site [MD5 encrypt](www.md5online.org) que criptografa uma string inserida para o seu MD5. Pensei primeiramente em fazer um post e passando o pdf, mas há um parâmetro “g-recaptcha-response” que ainda não sei como funciona. Então resolvi me preocupar primeiro com o que eu sei fazer.

13/02: 
Analisando o código fonte da página, novamente percebi que o form feito após o captcha ser resolvido pode ser realizado diretamente através de um get (apesar de o form indicar um post): http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diario.do?action=downloadDiario&pergunta=&captchaValidacao=ok&resposta=&id=96579&tribunal=TSE. Sendo os parâmetros pergunta e respota vazios e captchaValidacao sendo 'ok'.Assim, descartei, pelo menos por enquanto, a ideia de fazer um dicionário que verifica os padrões para quebrar o captcha, como eu havia pensado anteriormente.
Diante disso, me propus a fazer este get utilizando python e passando um id de alguns dos diários (escolhidos no código fonte da página).
    Ao tentar realizar essa tarefa cheguei ao seguinte trecho de código:

    import urllib
    import requests

    dictParametrosUrlBaixaDiario = {
        'action': 'downloadDiario',
        'pergunta': '',
        'captchaValidacao': 'ok',
        'resposta': '',
        'id': 96753, 'tribunal': 'TSE'}
    parametrosUrlBaixaDiarioEnconded = urllib.parse.urlencode(dictParametrosUrlBaixaDiario)
    urlBaixaDiario = 'http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diario.do'
    respostaUrlBaixaDiario = requests.get(urlBaixaDiario, params=parametrosUrlBaixaDiarioEnconded)
    print(respostaUrlBaixaDiario)
    with open('cadernos/testeteete', 'wb') as file:
        for parte in respostaUrlBaixaDiario.iter_content(chunk_size=128):
            file.write(parte)'

O parâmetro id foi testado com vários valores de id encontrados no código fonte da página.
Da biblioteca urllib foi utilizado o método parse.urlencode() que recebe um dicionário representando os parâmetros, e então, o converte para url string. Isso é devido ao fato de o content-type da requisição ser application/x-www-form-urlencoded; charset=UTF-8.
Referência: 
* [urlLib.parse.urlencode](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode)

Da biblioteca requests foi utilizado o médoto get que recebe uma string representando a url e os parâmetros definidos acima
Referência: 
* [Biblioteca requests](https://requests.readthedocs.io/en/latest/user/quickstart/)

Para manipulação do arquivo no qual o PDF será guardado foi utlizado o with statement, o qual, além de lidar com exceções, fecha o arquivo automaticamente. Além disso, como o arquivo não é grande optei por utilizar "resposta.iter_content" e transferir o arquivo de forma compassada em vez de usar "resposta.Raw", pois além de economizar memória RAM, também não vou precisar lidar com alguma conversões que eu teria de fazer se usar o segundo.
Referências: 
* [Ler e escrever arquivos](https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python)
* [Ajuda do stackoverflow](https://stackoverflow.com/questions/34503412/download-and-save-pdf-file-with-python-requests-module)

Após fazer o download do arquivo PDF e salvá-lo em uma pasta, procurei resolver o problema de como entrar o id de um diário, sabendo a data deste.

Verifiquei que no código fonte da página há um form para "pesquisa avançada", neste há dois campos que recebem data inicial e data final. Verifiquei que, em se colocar a mesma data como inicial e final a respota é um HTML contento o(s) caderno(s) desta data. É possível fazer o seguinte get para realizar essa tarefa: http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diarioTxt.do?action=buscarDiarios&voDiarioSearch.tribunal=TSE&page=diarioPageTextualList.jsp&voDiarioSearch.livre=&voDiarioSearch.numero=&voDiarioSearch.ano=&voDiarioSearch.dataPubIni=01%2F10%2F2018&voDiarioSearch.dataPubFim=01%2F10%2F2018. Neste os parâmetros voDiarioSearch.dataPubIni e voDiarioSearch.dataPubFim são a mesma string que representa a data citada anteriormente.

Diante disse cheguei ao seguinte código:

    import urllib
    import requests
    import re

    parametrosUrlBuscaDiario = {
        'action': 'buscarDiarios',
        'voDiarioSearch.tribunal': 'TSE',
        'page': 'diarioPageTextualList.jsp',
        'voDiarioSearch.tribunal': 'TSE',
        'voDiarioSearch.livre': '',
        'voDiarioSearch.numero': '',
        'voDiarioSearch.ano': '',
        'voDiarioSearch.dataPubIni': '01/10/2018',
        'voDiarioSearch.dataPubFim': '01/10/2018'
    }

    parametrosToUrlEncoded = urllib.parse.urlencode(parametrosUrlBuscaDiario)

    urlBuscaDiario = 'http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/diarioTxt.do'
    respostaHtmlBuscaDiario = requests.get(urlBuscaDiario, params=parametrosToUrlEncoded)
    conteudoBusca = respostaHtmlBuscaDiario.content

    regexBuscaIdDiario = re.findall(r'(?<=chamarCaptcha\()(.*)(?=,)', str(conteudoBusca))

Para encontrar o(s) Id(s) do(s) diário(s) na resposta HTML utilzei a biblioteca re. Utilizei o método findall e apliquei o seguinte padrão: "(?<=chamarCaptcha\()(.*)(?=,)", que garante que será retornado tudo que está entre a string 'chamarCaptcha' e o caracter ','. Assim será retornado uma lista contento o(s) id(s) do(s) diário(s) em formato de string.
Referências: 
* [Video de auxlio](https://www.youtube.com/watch?v=GEshegZzt3M)
* [Teste da expressão regular](https://regexr.com/48b7r)
* [Docs para html parser](https://docs.python.org/2/library/htmlparser.html)

Após isso, juntei as duas funções, colocando a primeira dentro de um "for" e baixando os diários para cada id encontrado na segunda função.

Outras referências:
* [.gitinore](https://github.com/github/gitignore/blob/master/Python.gitignore)
* [stackoverflow - urlencode](https://stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode)
* [Ajuda da documentação](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)