import React, {useState} from 'react';
import {StyleSheet, View, Button, Text, TextInput} from 'react-native';

export default function App() {
  const [screen, setScreen] = useState('login');
  const [username, setUsername] = useState('');
  const [ranked, setRanked] = useState(true);
  const [match, setMatch] = useState(null);
  const [players, setPlayers] = useState([
    {id: 'p1', mmr: 1000},
    {id: 'p2', mmr: 1000}
  ]);
  const [dummyCount, setDummyCount] = useState(0);

  function login() {
    setScreen('mode');
  }

  function chooseMode(isRanked) {
    setRanked(isRanked);
    setScreen('queue');
  }

  function addFriend() {
    const next = players.filter(p => !p.is_dummy).length + 1;
    setPlayers([...players, {id: `p${next}`, mmr: 1000}]);
  }

  function addDummy() {
    const next = dummyCount + 1;
    setDummyCount(next);
    setPlayers([...players, {id: `dummy${next}`, mmr: 1000, is_dummy: true}]);
  }

  async function findMatch() {
    await fetch('http://localhost:8000/add_group', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({sport: 'futebol', players})
    });

    const resp = await fetch('http://localhost:8000/match', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({sport: 'futebol', ranked})
    });
    const data = await resp.json();
    setMatch(data.match);
  }

  if (screen === 'login') {
    return (
      <View style={styles.container}>
        <TextInput
          style={styles.input}
          placeholder="Usuário"
          value={username}
          onChangeText={setUsername}
        />
        <Button title="Entrar" onPress={login} />
      </View>
    );
  }

  if (screen === 'mode') {
    return (
      <View style={styles.container}>
        <Button title="Ranked" onPress={() => chooseMode(true)} />
        <Button title="Normal Game" onPress={() => chooseMode(false)} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Button title="Chamar amigo" onPress={addFriend} />
      <Button title="Adicionar dummy" onPress={addDummy} />
      <Text>Grupo com {players.length} jogadores</Text>
      <Button title="Buscar partida" onPress={findMatch} />
      {match && <Text>A partida possui {match.length} grupos.</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center'
  },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 8,
    width: '80%',
    marginBottom: 12
  }
});
