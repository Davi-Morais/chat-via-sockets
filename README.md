Equipe: 
- Davi de Morais Farias
- Jose Igor Venancio de Albuquerque

# Chat via Sockets

## Dependências
Tenha o python3 ou maior instalado.

Dependendo da versão do python, talvez seja necessário instalar este pacote:
```
sudo apt-get install python3-tk
```


## Connectando

Primeiro, execute o servidor, passando o endereço ip e porta como argumentos:
```
python3 src/server/main.py 127.0.0.1 3000
```


para se conectar, execute o client passando o ip e porta do servidor:
```
python3 src/client/main.py 127.0.0.1 3000
```
e uma gui irá abrir.


## Enviando mensagens
A primeira coisa que o cliente deve fazer é informar o seu nome. Apenas digite seu nome no prompt e aperte Enter:
```
meu-nickname
```

a partir de agora, qualquer mensagem enviada pelo prompt será compartilhada para todos os usuários online.


Para 'cutucar' algum usuário, use *!poke* no prompt seguido pelo o nickname dele:
```
!poke outro-usuario-nickname
```

Para trocar de nickname:
```
!changenickname novo-nickname
```


use *exit* no client para encerrar a conexão:
```
exit
```