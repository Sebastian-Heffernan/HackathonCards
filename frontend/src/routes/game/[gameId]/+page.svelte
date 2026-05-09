<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import Game from "$lib/components/Game.svelte";

  type Card = {
    suit: string;
    value: string;
  };

  type PlayerState = {
    uuid: string | number;
    variables: unknown[] | Record<string, unknown>;
    hand: Card[];
    actions: string[];
    opponent_hand?: Card[][];
    opponent_names?: string[];
  };

  let gameVars = $state<Record<string, unknown>>({});

  let gameId = $state(page.params.gameId || "");
  let playerId = $state("");
  let socket = $state<WebSocket | null>(null);
  let playerNames = $state<string[]>([]);

  let playerState = $state<PlayerState>({
    uuid: "",
    variables: [],
    hand: [],
    actions: [],
    opponent_hand: [],
    opponent_names: []
  });

  onMount(() => {
    playerId = sessionStorage.getItem("playerId") || "";

    const initialPlayerState = sessionStorage.getItem("initialPlayerState");

    if (initialPlayerState) {
      playerState = JSON.parse(initialPlayerState);
    }

    if (gameId && playerId) {
      socket = new WebSocket(`ws://localhost:8000/ws/${gameId}/${playerId}`);

      socket.onmessage = (ev) => {
        const message = JSON.parse(ev.data);
        if (message.type === "GO_HOME") {
          sessionStorage.clear();
          goto("/");
          return;
        }
        if (message.type === "GAME_STATE" || message.type === "START_GAME") {
          playerState = message.playerState;
          gameVars = message.gameVars ?? {};
          playerNames = message.playerNames ?? playerNames;
        }
      };
    }
  });

  function restartGame() {
    socket?.send(JSON.stringify({
      type: "RESTART_GAME"
    }));
  }

  function goHomeAll() {
    socket?.send(JSON.stringify({
      type: "GO_HOME"
    }));
  }

  function sendAction(action: string, selectedCardId: number | null) {
    socket?.send(JSON.stringify({
      type: action,
      selectedCardId: selectedCardId
    }));
  }
</script>

<Game
  {playerState}
  {gameVars}
  {playerNames}
  {sendAction}
  {restartGame}
  {goHomeAll}
/>