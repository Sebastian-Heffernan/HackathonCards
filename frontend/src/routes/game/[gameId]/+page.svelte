<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import Game from "$lib/components/Game.svelte";

  let gameId = $state(page.params.gameId || "");
  let playerId = $state("");
  let socket = $state<WebSocket | null>(null);

  let gameState = $state<any>({
    actions: [],
    cards: [],
    masked_cards: []
  });

  let output = $state("");

  onMount(() => {
    playerId = sessionStorage.getItem("playerId") || "";

    if (!gameId || !playerId) {
      output = "Missing gameId or playerId";
      return;
    }

    socket = new WebSocket(`ws://localhost:8000/ws/${gameId}/${playerId}`);

    socket.onopen = () => {
      socket?.send(JSON.stringify({
        type: "SYNC"
      }));
    };

    socket.onmessage = (ev) => {
      const message = JSON.parse(ev.data);
      output = JSON.stringify(message, null, 2);

      if (message.type === "GAME_STATE" || message.type === "START_GAME") {
        gameState = message.gameState;
      }
    };
  });

  function sendAction(action: string, cards: any[]) {
    socket?.send(JSON.stringify({
      type: action,
      cards
    }));
  }
</script>

<Game {gameState} {sendAction} />

