<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
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

        if (message.type === "GAME_STATE" || message.type === "START_GAME") {
          playerState = message.playerState;
          gameVars = message.gameVars ?? {};
        }
      };
    }
  });

  function sendAction(action: string, selectedCardId: number | null) {
    socket?.send(JSON.stringify({
      type: action,
      selectedCardId: selectedCardId
    }));
  }
</script>

<Game {playerState} {gameVars} {sendAction} />