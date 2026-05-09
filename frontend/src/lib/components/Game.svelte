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
    sendAction
  } = $props<{
    playerState: PlayerState;
    gameVars?: Record<string, unknown>;
    sendAction: (action: string, selectedCardId: number | null) => void;
  }>();

  let selected = $state<boolean[]>([]);

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
<div class="w-screen h-screen flex">
  <aside class="nes-container with-title is-dark w-72 h-full p-4 shadow-lg overflow-auto shrink-0">
    <p class="title">Game Vars</p>
    <pre class="text-xs whitespace-pre-wrap">{JSON.stringify(gameVars, null, 2)}</pre>
  </aside>


  <div class="relative flex-1 h-full p-4 bg-green-500">
  <!--  <div class="nes-container with-title absolute top-0 left-0 w-40 h-full is-dark">
      <p class="title">Decks</p>
      <Deck />
    </div>
-->

    <div class="absolute top-4 left-1/2 -translate-x-1/2 flex gap-8">
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