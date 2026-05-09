<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import { goto } from "$app/navigation"

  type Player = {
    id: string;
    name: string;
    connected?: boolean;
  };

  let gameState = $state({
    actions: [],
    cards: [],
    masked_cards: []
  });

  let lobbyCode = $state(page.params.lobbyId || "");
  let userName = $state("username");

  let gameId = $state("");
  let playerId = $state("");
  let players = $state<Player[]>([]);
  let output = $state("");
  let socket = $state<WebSocket | null>(null);

  onMount(() => {
    gameId = sessionStorage.getItem("gameId") || "";
    playerId = sessionStorage.getItem("playerId") || "";

    if (gameId && playerId) {
      createWebsocket();
    }
  });

  // async function joinFromLobbyPage() {
  //   const response = await fetch(`/api/lobbies/${lobbyCode}/join`, {
  //     method: "POST",
  //     headers: {
  //       "Content-Type": "application/json"
  //     },
  //     body: JSON.stringify({
  //       name: userName
  //     })
  //   });

  //   const data = await response.json();

  //   gameId = data.gameId;
  //   playerId = data.playerId;

  //   sessionStorage.setItem("gameId", gameId);
  //   sessionStorage.setItem("playerId", playerId);
  //   sessionStorage.setItem("lobbyCode", lobbyCode);

  //   createWebsocket();
  // }

  function createWebsocket() {
    socket = new WebSocket(`ws://localhost:8000/ws/${gameId}/${playerId}`);

    socket.onopen = () => {
      socket?.send(JSON.stringify({
        type: "JOIN_GAME"
      }));
    };

    socket.onmessage = (ev) => {
      const message = JSON.parse(ev.data);
      output = JSON.stringify(message, null, 2);

      if (message.type === "UPDATE_PLAYERS") {
        players = Object.entries(message.players).map(([id, playerData]) => {
          const player = playerData as { name: string; connected?: boolean };

          return {
            id,
            name: player.name,
            connected: player.connected ?? true
          };
        });
      }

      if (message.type === "START_GAME") {
        sessionStorage.setItem("initialPlayerState", JSON.stringify(message.playerState));
        goto(`/game/${gameId}`);
      }
    };
  }

  function startGame() {
    socket?.send(JSON.stringify({
      type: "START_GAME"
    }));
  }
</script>


<main class="flex items-center justify-center min-h-screen w-screen bg-gray-200">
    <div class="flex flex-col items-center">
        <h1 class="text-4xl font-extrabold mb-6 py-8">Lobby</h1>

        <!-- Details Card: Now dynamic -->
        <div class="p-10 bg-white shadow-xl rounded-lg border border-gray-200">
            <p class="font-extrabold text-lg mb-2 text-center">Details</p>
            <p>Lobby Code: <span class="font-mono text-blue-600">{lobbyCode}</span></p>
            <p>Player Count: <span class="font-bold">{players.length}</span></p>
        </div>

        <div class="py-3">
            <button
              type="button"
              class="nes-btn is-primary"
              disabled={players.length === 0}
              onclick={startGame}
            >
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