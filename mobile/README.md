# Mobile App

Este diretório contém um exemplo simples de aplicativo React Native que consome a API do servidor Python.

## Requisitos

- Node.js e npm (ou yarn)
- Expo CLI (`npm install -g expo-cli`)

## Rodando

```bash
cd mobile
npm install
npx expo start
```

O aplicativo fará requisições para `http://localhost:8000` por padrão, portanto inicie `server.py` antes de rodá-lo. Ele começa em uma **tela de login**, em seguida apresenta a escolha entre **Ranked** ou **Normal Game**. A terceira tela contém os botões **Chamar amigo**, **Adicionar dummy** e **Buscar partida**. Esse último adiciona o grupo à fila e busca a partida de uma só vez.
