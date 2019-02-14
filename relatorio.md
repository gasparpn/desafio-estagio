# Relatório

##### Considerações iniciais: 
Neste documento estará descrito o processo para solução do desafio proposto, indicarei as soluções proposta no início, ao se identificar o problema, até a possível solução de fato para o mesmo. O relatório será construído no decorrer das tentativas de soluções. Dessa forma,  discorrerei em primeira pessoa para uma melhor fluidez do texto.

Primeiro dia – 12/02: Após ler o desafio tentei identificar o que eu precisava aprender e os problemas que eu iria precisar resolver para se chegar a solução. A se aprender identifiquei:
- Como a função MD5 funciona
- Entender o básico de como “quebrar” captcha
- Manipulação de PDF utilizando python

Os problemas que consegui encontrar foram:
- Tentar encontrar um padrão nas perguntas geradas pelo captcha do site indicado.
	Ao fazer algumas requisições utilizando o navegador e verificando o código fonte e devtools vi que na página principal havia um iframe que englobava a página [http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/] e no javascript desta havia a função chamarCaptcha que “chama” o captcha através de um POST [http://inter03.tse.jus.br/sadJudDiarioDeJusticaConsulta/captcha.do] e a resposta a pergunta recebida é feita também por um POST, tendo como content-type ‘application/x-www-form-urlencoded; utf-8’ e os parâmetros eram: resposta e pergunta.
	Dessa forma, me propus a utilizar um meio externo, que não o browser, para fazer as requisições e analisar as respostas. Minha intenção foi encontrar um padrão nas perguntas e respostas e verificar como iria precisar fazer o post (já que terei de fazer isso no programa em python).
Encontrei um padrão nas perguntas e respotas e a solução imediata que pensei foi criar um dicionário que tem um padrão como chave e indica uma forma de tratamento no campo valor.
Utilizei como fonte de pesquisa: [Referência](https://gist.github.com/subfuzion/08c5d85437d5d4f00e58)

- Um outro problema que enfrentei foi como encriptar o pdf. Pesquisando encontrei o seguinte site www.md5online.org que criptografa uma string inserida para o seu MD5. Pensei primeiramente em fazer um post e passando o pdf, mas há um parâmetro “g-recaptcha-response” que ainda não sei como funciona. Então resolvi me preocupar primeiro com o que eu sei fazer.