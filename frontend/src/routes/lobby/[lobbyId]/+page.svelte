<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";

  type Player = {
    id: string;
    name: string;
    connected?: boolean;
  };

  let gameState = $state({
    actions: [],
    cards: [],
    masked_cards: [],
  });

  let lobbyCode = $state(page.params.lobbyId || "");
  let userName = $state("username");

  let showErrorPopup = $state(false);
  let errorMessage = $state("");
  
  let gameId = $state("");
  let playerId = $state("");
  let players = $state<Player[]>([]);
  let gameDescription = $state("");
  let output = $state("");
  let socket = $state<WebSocket | null>(null);

  onMount(() => {
    gameId = sessionStorage.getItem("gameId") || "";
    playerId = sessionStorage.getItem("playerId") || "";
    gameDescription = sessionStorage.getItem("gameDescription") || "";
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
      socket?.send(
        JSON.stringify({
          type: "JOIN_GAME",
        }),
      );
    };

    socket.onmessage = (ev) => {
      const message = JSON.parse(ev.data);
      output = JSON.stringify(message, null, 2);

      if (message.description !== undefined) {
        gameDescription = message.description;
        sessionStorage.setItem("gameDescription", gameDescription);
      }

      if (message.type === "LOBBY_ERROR") {
        errorMessage = message.message;
        showErrorPopup = true;
        return;
      }

      if (message.type === "UPDATE_PLAYERS") {
        players = Object.entries(message.players).map(([id, playerData]) => {
          const player = playerData as { name: string; connected?: boolean };

          return {
            id,
            name: player.name,
            connected: player.connected ?? true,
          };
        });
      }

      if (message.type === "GO_HOME") {
        sessionStorage.clear();
        goto("/");
        return;
      }

      if (message.type === "START_GAME") {
        sessionStorage.setItem(
          "initialPlayerState",
          JSON.stringify(message.playerState),
        );
        sessionStorage.setItem(
          "initialGameVars",
          JSON.stringify(message.gameVars ?? {}),
        );
        sessionStorage.setItem(
          "initialPlayerNames",
          JSON.stringify(message.playerNames ?? []),
        );

        goto(`/game/${gameId}`);
      }
    };
  }

  function startGame() {
    socket?.send(
      JSON.stringify({
        type: "START_GAME",
      }),
    );
  }
</script>

<main
  class="flex items-center justify-center min-h-screen w-screen bg-gray-200"
>
  <div class="flex flex-row gap-8 items-start">
    <h1 class="text-4xl font-extrabold mb-6 py-8">Lobby</h1>

    <!-- Left Side -->
    <div class="flex flex-col items-center">
      <!-- Details Card: Now dynamic -->
      <div class="p-10 bg-white shadow-xl rounded-lg border border-gray-200">
        <p class="font-extrabold text-lg mb-2 text-center">Details</p>
        <p>
          Lobby Code: <span class="font-mono text-blue-600">{lobbyCode}</span>
        </p>
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
            <p
              class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors"
            >
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
            <p class="col-span-full text-gray-500 italic">
              Waiting for players to join...
            </p>
          {/each}
        </div>
      </div>
    </div>
    <!-- RIGHT SIDE -->
    <div class="w-[320px] bg-white shadow-lg rounded-lg p-4">
      <h2 class="text-xl font-bold mb-3">Instructions</h2>
      <textarea
        class="w-full h-[400px] border rounded p-2 text-sm resize-none"
        readonly
        value={gameDescription}
      ></textarea>
    </div>
    {#if showErrorPopup}
      <div
        class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      >
        <div class="bg-white rounded-lg shadow-lg max-w-lg w-[90vw] p-6">
          <h2 class="text-xl font-bold mb-3 text-red-600">Setup Error</h2>

          <p class="mb-6 whitespace-pre-wrap">
            {errorMessage}
          </p>

          <div class="flex justify-center">
            <button
              class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-800"
              onclick={() => (showErrorPopup = false)}
            >
              OK
            </button>
          </div>
        </div>
      </div>
    {/if}
  </div>
</main>
