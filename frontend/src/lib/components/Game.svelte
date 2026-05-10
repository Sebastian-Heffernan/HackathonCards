<script lang="ts">
  import Hand from "./Hand.svelte";
  import Deck from "./Deck.svelte";

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

  let {
    playerState,
    gameVars = {},
    playerNames = [],
    sendAction,
    restartGame,
    goHomeAll,
    showGameErrorPopup = false,
    gameErrorMessage = "",
    closeGameErrorPopup = () => {}
  } = $props<{
    playerState: PlayerState;
    gameVars?: Record<string, unknown>;
    playerNames?: string[];
    sendAction: (action: string, selectedCardId: number | null) => void;
    restartGame: () => void;
    goHomeAll: () => void;
    showGameErrorPopup?: boolean;
    gameErrorMessage?: string;
    closeGameErrorPopup?: () => void;
  }>();

  let winnerIndex = $derived(Number(gameVars["$winner"] ?? -1));
  let winnerName = $derived(playerNames[winnerIndex] ?? `Player ${winnerIndex}`);
  let currentTurnIndex = $derived(Number(gameVars["$turnPlayer"] ?? -1));
  let currentTurnName = $derived(
    playerNames[currentTurnIndex] ?? `Player ${currentTurnIndex}`
  );

  let selected = $state<boolean[]>([]);
  let showGameVars = $state(true);

  $effect(() => {
    selected = playerState?.hand?.length
      ? new Array(playerState.hand.length).fill(false)
      : [];
  });

  const toggleCard = (i: number) => {
    selected = selected.map((_, idx) => idx === i ? !selected[i] : false);
  };

  const playAction = (actionIdx: number) => {
    const action = playerState.actions[actionIdx];
    const selectedCardId = selected.findIndex(Boolean);

    sendAction(action, selectedCardId);
  };
</script>
<div class="w-full h-screen flex relative">
  {#if showGameVars}
    <aside class="bg-[#212529] w-72 h-full p-4 shadow-lg overflow-y-auto shrink-0 z-50 overflow-hidden absolute pt-16">
      <h1 class="text-white">Game Variables</h1>
      <div class="flex flex-col gap-2">
        {#each Object.entries(gameVars) as [key, value]}
          <div class="flex flex-col border-b border-gray-700 pb-2 mb-2 last:border-0">
            <span class="text-blue-400 font-bold text-xs uppercase tracking-wider">{key}</span>
            <span class="text-white text-sm break-words">
              {typeof value === 'boolean' ? (value ? "True" : "False") : value}
            </span>
          </div>
        {/each}
      </div>
    </aside>
  {/if}

  <div class="relative flex-1 h-full p-4 bg-green-500 overflow-hidden">
  <!--  <div class="nes-container with-title absolute top-0 left-0 w-40 h-full is-dark">
      <p class="title">Decks</p>
      <Deck />
    </div>
-->
    <div class="w-12 h-full shrink-0 flex justify-center absolute">
      <button
        type="button"
        class="w-8 h-8 bg-gray-700 text-white rounded shadow flex items-center justify-center hover:bg-gray-600 font-bold z-100"
        onclick={() => (showGameVars = !showGameVars)}
        title={showGameVars ? "Hide vars" : "Show vars"}
      >
        {showGameVars ? "<" : ">"}
      </button>
    </div>
    {#if showGameErrorPopup}
      <div class="absolute inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="nes-container is-dark with-title w-[520px] text-center">
          <p class="title">Game Error</p>

          <p class="mb-6 whitespace-pre-wrap text-left">
            {gameErrorMessage}
          </p>

          <div class="flex justify-center gap-4">
            <button
              type="button"
              class="nes-btn is-error"
              onclick={goHomeAll}
            >
              Home
            </button>
          </div>
        </div>
      </div>
    {/if}
    {#if winnerIndex >= 0}
      <div class="absolute inset-0 bg-black/70 flex items-center justify-center z-50">
        <div class="nes-container is-dark with-title w-[420px] text-center">
          <p class="title">Game Over</p>

          <p class="text-2xl font-bold mb-6">
            {winnerName} wins!
          </p>

          <div class="flex justify-center gap-4">
            <button
              type="button"
              class="nes-btn is-primary"
              onclick={restartGame}
            >
              Restart
            </button>

            <button
              type="button"
              class="nes-btn is-error"
              onclick={goHomeAll}
            >
              Home
            </button>
          </div>
        </div>
      </div>
    {/if}

    <div class="absolute top-4 left-1/2 -translate-x-1/2 flex flex-col items-center gap-4">
      <div class="bg-white text-black px-4 py-2 rounded shadow font-bold">
        Turn: {currentTurnName}
      </div>

      <div class="flex gap-8">
        {#each playerState.opponent_hand ?? [] as opponentCards, opponentIdx}
          <div class="flex flex-col items-center gap-2">
            <p class="bg-white text-black px-2 py-1 rounded text-sm">
              {playerState.opponent_names?.[opponentIdx] ?? `Player ${opponentIdx + 1}`}
            </p>

            <Hand
              cards={opponentCards}
              actions={[]}
              isOpponent={true}
              selected={[]}
            />
          </div>
        {/each}
      </div>
    </div>

    <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex flex-col items-center gap-4">
      <Hand
        actions={[]}
        cards={playerState.hand}
        onCardClick={toggleCard}
        {selected}
      />

      <div class="flex gap-4">
        {#each playerState.actions as action, actionIdx}
          <button
            type="button"
            class="nes-btn is-primary"
            onclick={() => playAction(actionIdx)}
          >
            {action}
          </button>
        {/each}
      </div>
    </div>
  </div>
</div>
