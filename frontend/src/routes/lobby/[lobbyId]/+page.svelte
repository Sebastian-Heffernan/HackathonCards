<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import { env } from "$env/dynamic/public";

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
  const apiUrl = (env.PUBLIC_API_URL || "http://localhost:8000").replace(/\/$/, "");
  const wsUrl = apiUrl.replace(/^http/, "ws");

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
    socket = new WebSocket(`${wsUrl}/ws/${gameId}/${playerId}`);

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

<main class="flex flex-col min-h-screen w-screen bg-gray-200">
  <!-- TITLE -->
  <h1 class="text-4xl font-extrabold py-8 text-center">Lobby</h1>

  <!-- TOP SECTION (LEFT + RIGHT) -->
  <div
    class="flex w-full max-w-6xl mx-auto flex-1 items-stretch flex-col md:flex-row gap-4 md:gap-0 justify-center"
  >
    <!-- LEFT HALF -->
    <div class="w-full md:w-1/2 flex justify-center">
      <div class="flex flex-col items-center gap-4">
        <div class="p-10 bg-white shadow-xl rounded-lg border border-gray-400">
          <p class="font-extrabold text-lg mb-2 text-center">Details</p>
          <p>
            Lobby Code:
            <span class="font-mono text-blue-600">{lobbyCode}</span>
          </p>
          <p>Player Count: <span class="font-bold">{players.length}</span></p>
        </div>

        <button
          type="button"
          class="nes-btn is-primary"
          disabled={players.length === 0}
          onclick={startGame}
        >
          Start Game
        </button>
      </div>
    </div>

    <!-- RIGHT HALF -->
    <div class="w-4/5 md:w-1/2 flex justify-center mx-auto">
      <div
        class="w-[420px] h-full bg-white shadow-lg rounded-lg p-4 border border-gray-400"
      >
        <h2 class="text-xl font-bold text-center">Instructions</h2>

        <textarea
          class="w-full h-[180px] border rounded p-2 text-sm resize-none"
          readonly
          bind:value={gameDescription}
        ></textarea>
      </div>
    </div>
  </div>

  <!-- PLAYERS (BELOW BOTH HALVES) -->
  <div class="py-6 w-full max-w-6xl mx-auto">
    <h2 class="text-2xl font-extrabold py-3 text-center">Players</h2>

    <div class="flex flex-wrap justify-center gap-4">
      {#each players as player, index}
        <p class="bg-white border rounded p-4 text-center font-semibold">
          {#if index === 0}
            HOST:
          {/if}
          {player.name}
        </p>
      {:else}
        <p class="col-span-full text-gray-500 italic text-center">
          Waiting for players to join...
        </p>
      {/each}
    </div>
  </div>

  {#if showErrorPopup}
    <div
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    >
      <div
        class="bg-white rounded-lg shadow-lg max-w-lg w-[90vw] p-6 border border-gray-400"
      >
        <h2 class="text-xl font-bold mb-3 text-red-600 text-center">
          Setup Error
        </h2>

        <p class="mb-6 whitespace-pre-wrap text-gray-800">
          {errorMessage}
        </p>

        <div class="flex justify-center">
          <button
            type="button"
            class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-800"
            onclick={() => (showErrorPopup = false)}
          >
            OK
          </button>
        </div>
      </div>
    </div>
  {/if}
</main>
