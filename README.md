# sports-ranked-queue

Sistema simples de filas para partidas de esportes. Suporta futebol, basquete e vôlei.
Grupos podem entrar na fila em modo normal ou ranked. No modo ranked os grupos
precisam ter MMR parecido para a partida ser formada.

## Como usar

```bash
python sports_queue.py
```

O exemplo no final do arquivo `sports_queue.py` demonstra a criação de alguns
jogadores e grupos para o esporte **futebol** e como a fila forma uma partida
quando há jogadores suficientes com MMR semelhante.
```

## Rodando o servidor

Para executar o sistema como um servidor HTTP simples:

```bash
python server.py
```

Por padrao ele escuta na porta 8000 e oferece dois endpoints:
`/add_group` para adicionar grupos e `/match` para tentar formar uma partida.

## Aplicativo mobile

O diretório `mobile/` possui um exemplo de aplicativo React Native que funciona
tanto no Android quanto no iOS. O fluxo começa em uma **tela de login**,
depois permite escolher entre **Ranked** ou **Normal Game** e só então mostra
os botões para gerenciar o grupo. Use **Chamar amigo** para adicionar um
jogador real e **Adicionar dummy** para incluir um amigo sem conta. Depois
pressione **Buscar partida** para adicionar o grupo à fila e tentar formar uma
partida automaticamente.

Para rodar o app com o Expo:

```bash
cd mobile
npm install
npx expo start
```

Lembre-se de iniciar o `server.py` antes de abrir o aplicativo.

## Testes

Execute os testes com:

```bash
python -m unittest discover
```
