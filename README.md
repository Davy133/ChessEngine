# ChessEngine - Bot de Xadrez em Python
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Davy133/ChessEngine) </br>
![ChessEngine♟](https://github.com/Davy133/ChessEngine/assets/55928285/d04cdc09-537c-4f61-8dea-edcb2fd6e947)

Integrantes do grupo: NATAN HUGO CARVALHO EVANGELISTA, SALOMÃO DAVY DOS SANTOS COÊLHO, TAMIRES SANTIAGO OLIVEIRA, ALVARO LUIZ SANTOS NASCIMENTO

ChessEngine é um bot de xadrez desenvolvido em Python que utiliza a biblioteca Flask e Flask-SocketIO para criar uma interface web interativa para jogar xadrez contra o bot. O bot utiliza uma engine de xadrez personalizada chamada `chessEngine` para calcular os melhores movimentos.

## Funcionalidades

- Jogue xadrez contra o bot.
- Comunique-se com o bot por meio de comandos de voz ou selecionando movimentos no tabuleiro.
- Opção de inverter a orientação do tabuleiro.
- Reinicie o jogo a qualquer momento.

## Pré-requisitos

Certifique-se de ter os seguintes requisitos instalados em sua máquina:

- Python 3.6 ou superior
- Flask
- Flask-SocketIO

## Instalação

1. Clone o repositório do projeto:

```bash
git clone https://github.com/Davy133/ChessEngine.git
```


2. Acesse o diretório do projeto:
```bash
cd ChessEngine
```


3. Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

## Uso

Execute o arquivo `app.py` para iniciar o servidor Flask:
```bash
python app.py
```


Acesse o aplicativo em seu navegador através do link [http://localhost:5000](http://localhost:5000).

## Como jogar

1. Ao acessar o aplicativo, o tabuleiro de xadrez será exibido.
2. Realize um movimento selecionando uma peça e um destino ou usando comandos de voz.
3. Aguarde a resposta do bot enquanto ele processa o movimento.
4. O bot realizará o seu movimento e a resposta será exibida no tabuleiro.
5. Repita os passos 2-4 até o final do jogo.

## Contribuição

Contribuições são bem-vindas! Se você deseja melhorar ou adicionar recursos ao IxculaChess, siga estas etapas:

1. Fork o repositório.
2. Crie um branch para a sua nova funcionalidade (`git checkout -b feature/nova-funcionalidade`).
3. Faça as alterações desejadas no código.
4. Commit suas alterações (`git commit -am 'Adiciona nova funcionalidade'`).
5. Push para o branch (`git push origin feature/nova-funcionalidade`).
6. Abra um Pull Request.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo LICENSE para obter mais informações.
