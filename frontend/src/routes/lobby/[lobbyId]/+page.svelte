<script lang="ts">
import { onMount } from 'svelte';
  import { page } from '$app/state';
  type Player = {
    id: string;
    name: string;
    connected?: boolean;
    };

    let lobbyCode = $state(page.params.lobbyId || "");
    let players = $state<Player[]>([]);
    
  let rulesText = $state(`ACTION START BUTTON "Start Game":
    EXIT`); // hidden for now, do not show in a textbox

  

  let userName = $state("username");

  let ruleId = $state("");
  let gameId = $state("");
  let playerId = $state("");
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
    lobbyCode = data.lobbyCode;
    output = JSON.stringify(data, null, 2);
    console.log(output);

    // connect web socket, same call as if joining lobby
    createWebsocket()
  }

  // host doesn't join own lobby since already joined when created
  async function joinLobby() {
    const response = await fetch(`/api/lobbies/${lobbyCode}/join`, {
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
    lobbyCode = data.lobbyCode;
    output = JSON.stringify(data, null, 2);

    // connect web socket, same call as if joining lobby
    createWebsocket()
  }

function createWebsocket() {
    // Ensure you have gameId and playerId from your join logic/page state
    const ws = new WebSocket(`/ws/${gameId}/${playerId}`);
    
    ws.onopen = () => {
      ws.send(JSON.stringify({ type: "JOIN_GAME" }));
    };

    ws.onmessage = (ev) => {
      const message = JSON.parse(ev.data);
      if (message.type === "UPDATE_PLAYERS") {
        players = Object.values(message.players);
      }
    };
    
    socket = ws; // Store in state if needed
  }



</script>


<main class="flex items-center justify-center min-h-screen w-screen bg-gray-200">
    <div class="flex flex-col items-center">
        <h1 class="text-4xl font-extrabold mb-6 py-8">Lobby</h1>

        <!-- Details Card: Now dynamic -->
        <div class="p-10 bg-white shadow-xl rounded-lg border border-gray-200">
            <p class="font-extrabold text-lg mb-2 text-center">Details</p>
            <p>Lobby Code: <span class="font-mono text-blue-600">{output}</span></p>
            <p>Player Count: <span class="font-bold">{players.length}</span></p>
        </div>

        <div class="py-3">
            <button type="button" class="nes-btn is-primary" disabled={players.length === 0}>
                Start Game
            </button>
        </div>

        <div class="py-3">
            <h1 class="text-2xl font-extrabold py-3 text-center">Players:</h1>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                
                {#each players as player, index}
                    <p class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors">
                        {#if index === 0}
                            <i class="nes-icon coin is-small"></i>
                            HOST: 
                        {/if}
                        {player.name}
                        {#if !player.connected}
                            <span class="text-red-500 text-xs">(Disconnected)</span>
                        {/if}
                    </p>
                {:else}
                    <p class="col-span-full text-gray-500 italic">Waiting for players to join...</p>
                {/each}

            </div>
        </div>
    </div>
</main>