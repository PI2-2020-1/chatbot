# A2P2 Bot

## Instalação

1. Instale o [ngrok](https://ngrok.com/download).

2. Instale o [virtualenv](https://virtualenv.pypa.io/en/latest/).

3. Crie o ambiente.
```
python3 -m venv ./env 
```
4. Entre no ambiente.
```
source ./venv/bin/activate
```
5. Instale as dependências.
```
pip3 install -r requirements.txt
```



## Execução

1. Rode a [API](https://github.com/PI2-2020-1/api/) e cadastre um usuário com seu Telegram real para ter acesso a todas as funcionalidades do bot.

2. Rode o ngrok com a porta do rasa em uma aba.
```
./ngrok http 5005
```
3. Substitua em *credentials.yml* o id fornecido pelo ngrok no passo anterior e o token atual do bot no Telegram (verificar com um admin do repositório).
```yml
connector.connector.CustomTelegramInput:
  access_token: "XXXXXXXXXXXXX" #AQUI
  verify: "a2p2_bot"
  webhook_url: "https://XXXXXXXXXXX.ngrok.io/webhooks/telegram/webhook" #AQUI

```
4. Rode o servidor de *actions* em outra aba.
 ```
rasa run actions
```
5. Rode o servidor do bot em outra aba.
```
rasa run
```
6. Tudo pronto. Agora você pode conversar com o A2P2bot (@a2p2_bot) no Telegram.

