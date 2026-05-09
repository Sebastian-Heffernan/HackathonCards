<!-- This is a demo of blackjack -->

<script lang="ts">
  import Hand from "./Hand.svelte";
  import Deck from "./Deck.svelte";

  type Card = {
    suit: string;
    value: string;
  };

  type GameState = {
    actions: string[];
    masked_cards: Card[][];
    cards: Card[];
  };

  let {
    gameState,
    sendAction
  } = $props<{
    gameState: GameState;
    sendAction: (action: string, cards: Card[]) => void;
  }>();

  let selected = $state<boolean[]>([]);

  $effect(() => {
    selected = gameState?.cards?.length
      ? new Array(gameState.cards.length).fill(false)
      : [];
  });

  const toggleCard = (i: number) => {
    selected[i] = !selected[i];
  };

  const playAction = (actionIdx: number) => {
    const action = gameState.actions[actionIdx];
    const chosenCards = gameState.cards.filter((_, i) => selected[i]);

    sendAction(action, chosenCards);
  };
</script>

<div class="relative w-screen h-screen p-4 bg-green-500">
  <div class="nes-container with-title absolute t-0 l-0 w-40 h-full is-dark">
    <p class="title">Decks</p>
    <Deck />
  </div>

  <div class="absolute bottom-4 left-1/2 -translate-x-1/2">
    <Hand
      actions={gameState.actions}
      cards={gameState.cards}
      onCardClick={toggleCard}
      {selected}
      {playAction}
    />
  </div>

  {#each gameState.masked_cards as opponent_cards}
    <div class="absolute top-4 left-1/2 -translate-x-1/2">
      <Hand
        actions={[]}
        cards={opponent_cards}
        isOpponent={true}
        selected={[]}
      />
    </div>
  {/each}
</div>