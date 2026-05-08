<script>
// @ts-nocheck

  let rulesText = `ACTION START BUTTON "Start Game":
    EXIT`;

  let userName = "PlayerName";

  let ruleId = "";
  let gameId = "";
  let playerId = "";

  // @ts-ignore
  /**
     * @type {string | any[] | null | undefined}
     */
  let players = [];

  let output = "";


  // @ts-ignore
  let socket = null;

  async function sendRules() {
    const response = await fetch("/api/rules", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        source: rulesText
      })
    });

    const data = await response.json();

    ruleId = data.ruleId;
    output = JSON.stringify(data, null, 2);
  }

  async function createLobby() {
    const response = await fetch("/api/lobbies", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        rule_id: ruleId,
        host_name: userName
      })
    });

    const data = await response.json();

    gameId = data.gameId;
    playerId = data.playerId;
    output = JSON.stringify(data, null, 2);

    // connect web socket, same call as if joining lobby
    createWebsocket()
  }

  // host doesn't join own lobby since already joined when created
  async function joinLobby() {
    const response = await fetch(`/api/lobbies/${gameId}/join`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: userName,
      })
    });

    const data = await response.json();

    gameId = data.gameId;
    playerId = data.playerId;
    output = JSON.stringify(data, null, 2);

    // connect web socket, same call as if joining lobby
    createWebsocket()
  }

  function createWebsocket() {
    const socket = new WebSocket(`ws://localhost:8000/ws/${gameId}/${playerId}`)
    // @ts-ignore
    socket.onopen = (ev) => {
      socket.send(JSON.stringify({
        "type": "JOIN_GAME"
      }));
    } 

    // player leave lobby onclose?

    socket.onmessage = (ev) => {
      const messageData = ev.data;
      const message = JSON.parse(messageData);
      if (message.type == "UPDATE_PLAYERS") {
        // update list of players on page
        players = Object.values(message.players);
      }
    }
  }
</script>

<main>
  <h1>Cardssembly Cards Test</h1>

  <section>
    <h2>Rules</h2>

    <textarea bind:value={rulesText}></textarea>

    <br />

    <button on:click={sendRules}>
      Send Rules
    </button>
  </section>

  <section>
    <h2>Create Lobby</h2>
    <p>username:</p>
    <input bind:value={userName} placeholder="Host name" />

    <br />

    <button on:click={createLobby} disabled={!ruleId}>
      Create Lobby
    </button>

    <br />

    <h3>Join Lobby</h3>
    <p>gameId: </p>
    <textarea bind:value={gameId}></textarea>
    <button on:click={joinLobby}>
      Join Lobby
    </button>
  </section>

  <section>
    <h2>Current IDs</h2>

    <p><strong>Rule ID:</strong> {ruleId || "none"}</p>
    <p><strong>Game ID:</strong> {gameId || "none"}</p>
    <p><strong>Player ID:</strong> {playerId || "none"}</p>
    <p><strong>Players in Lobby:</strong></p>
    {#if players.length > 0}
    <ul>
      {#each players as player}
        <li>{player.name}</li>
      {/each}
    </ul>
    {/if}

  </section>

  <section>
    <h2>Response</h2>
    <pre>{output}</pre>
  </section>
</main>

