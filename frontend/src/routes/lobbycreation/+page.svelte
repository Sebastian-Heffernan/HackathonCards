<script lang="ts">
import { goto } from '$app/navigation'; // Add this import
  type Player = {
    id: string;
    name: string;
    connected?: boolean;
  };

  let rulesText = $state(`
ACTION START BUTTON "Start Game":
    DECK MAKE deck
    DECK SHUFFLE deck
    MOVE_CARD deck active
    GET_ATTR last_moved_card value current_val
    SET_VAR score 0
    SET_VAR status "Guess higher or lower"
    END_TURN

ACTION HIGHER BUTTON "Higher":
    CALL SWAP_CARD
    GET_ATTR last_moved_card value next_val
    COMPARE next_val > current_val
    GOTO WIN
    GOTO LOSE

ACTION LOWER BUTTON "Lower":
    CALL SWAP_CARD
    GET_ATTR last_moved_card value next_val
    COMPARE next_val < current_val
    GOTO WIN
    GOTO LOSE

LABEL SWAP_CARD:
    MOVE_CARD active discard
    MOVE_CARD deck active
    RETURN

LABEL WIN:
    MATH score + 1
    SET_VAR current_val next_val
    SET_VAR status "Correct"
    END_TURN

LABEL LOSE:
    SET_VAR score 0
    SET_VAR status "Wrong"
    END_TURN
  `);

  let userName = $state("username");

  let ruleId = $state("");
  let gameId = $state("");
  let playerId = $state("");
  let lobbyCode = $state("");

  let players = $state<Player[]>([]);

  let output = $state("");

  let socket = $state<WebSocket | null>(null);

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
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        rule_id: ruleId,
        host_name: userName
      })
    });

    const data = await response.json();

    if (data.lobbyCode) {
      // Redirect to the dynamic route
      // This ensures the URL changes to /lobby/ABCDE
      sessionStorage.setItem("gameId", data.gameId);
      sessionStorage.setItem("playerId", data.playerId);
      sessionStorage.setItem("lobbyCode", data.lobbyCode);

      goto(`/lobby/${data.lobbyCode}`);
    }
  }

  // host doesn't join own lobby since already joined when created
  async function joinLobby() {
    const response = await fetch(`/api/lobbies/${lobbyCode}/join`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: userName
      })
    });

    const data = await response.json();

    sessionStorage.setItem("gameId", data.gameId);
    sessionStorage.setItem("playerId", data.playerId);
    sessionStorage.setItem("lobbyCode", data.lobbyCode);

    goto(`/lobby/${data.lobbyCode}`);
  }

  
</script>

<main>
  <h1>Cardssembly Cards Test</h1>

  <section>
    <h2>Rules</h2>

    <textarea bind:value={rulesText}></textarea>

    <br />

    <button onclick={sendRules}>
      Send Rules
    </button>
  </section>

  <section>
    <h2>Create Lobby</h2>
    <p>username:</p>
    <input bind:value={userName} placeholder="Host name" />

    <br />

    <button onclick={createLobby} disabled={!ruleId}>
      Create Lobby
    </button>

    <br />

    <h3>Join Lobby</h3>
    <p>gameId: {gameId || "none"}</p>
    <input bind:value={lobbyCode} placeholder="Code" />
    <button onclick={joinLobby}>
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

