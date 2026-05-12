<script lang="ts">
  import { onMount } from "svelte";
  import { page } from "$app/state";
  import { goto } from "$app/navigation";
  import Game from "$lib/components/Game.svelte";
  import { env } from "$env/dynamic/public";
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

  let showGameErrorPopup = $state(false);
  let gameErrorMessage = $state("");

  let playerState = $state<PlayerState>({
    uuid: "",
    variables: [],
    hand: [],
    actions: [],
    opponent_hand: [],
    opponent_names: [],
  });

  onMount(() => {
    const baseURL = (env.PUBLIC_API_URL || "http://localhost:8000").replace(
      /\/$/,
      "",
    );

    const url = new URL(baseURL);
    url.protocol = url.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = url.href.replace(/\/$/, "");
    playerId = sessionStorage.getItem("playerId") || "";

    const initialPlayerState = sessionStorage.getItem("initialPlayerState");
    const initialGameVars = sessionStorage.getItem("initialGameVars");
    const initialPlayerNames = sessionStorage.getItem("initialPlayerNames");
    if (initialPlayerState) {
      playerState = JSON.parse(initialPlayerState);
    }
    if (initialGameVars) {
      gameVars = JSON.parse(initialGameVars);
    }
    if (initialPlayerNames) {
      playerNames = JSON.parse(initialPlayerNames);
    }

    if (gameId && playerId) {
      socket = new WebSocket(`${wsUrl}/ws/${gameId}/${playerId}`);

      socket.onmessage = (ev) => {
        const message = JSON.parse(ev.data);
        if (message.type === "GO_HOME") {
          sessionStorage.clear();
          goto("/");
          return;
        }
        if (message.type === "GAME_ERROR") {
          gameErrorMessage = message.message;
          showGameErrorPopup = true;
          return;
        }
        if (message.type === "GAME_STATE" || message.type === "START_GAME") {
          playerState = message.playerState;
          gameVars = message.gameVars ?? {};
          playerNames = message.playerNames ?? playerNames;

          if (message.type === "START_GAME") {
            sessionStorage.setItem(
              "initialPlayerState",
              JSON.stringify(message.playerState),
            );
          }
        }
      };
    }
  });

  function restartGame() {
    socket?.send(
      JSON.stringify({
        type: "RESTART_GAME",
      }),
    );
  }

  function goHomeAll() {
    socket?.send(
      JSON.stringify({
        type: "GO_HOME",
      }),
    );
  }

  function sendAction(action: string, selectedCardId: number | null) {
    socket?.send(
      JSON.stringify({
        type: action,
        selectedCardId: selectedCardId,
      }),
    );
  }
</script>

<Game
  {playerState}
  {gameVars}
  {playerNames}
  {sendAction}
  {restartGame}
  {goHomeAll}
  {showGameErrorPopup}
  {gameErrorMessage}
/>
