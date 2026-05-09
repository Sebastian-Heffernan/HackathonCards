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
  };

  let {
    playerState,
    sendAction
  } = $props<{
    playerState: PlayerState;
    sendAction: (action: string, cards: Card[]) => void;
  }>();

  let selected = $state<boolean[]>([]);

  $effect(() => {
    selected = playerState?.hand?.length
      ? new Array(playerState.hand.length).fill(false)
      : [];
  });

  const toggleCard = (i: number) => {
    selected[i] = !selected[i];
  };

  const playAction = (actionIdx: number) => {
    const action = playerState.actions[actionIdx];
    const chosenCards = playerState.hand.filter((_, i) => selected[i]);

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
      actions={playerState.actions}
      cards={playerState.hand}
      onCardClick={toggleCard}
      {selected}
      {playAction}
    />
  </div>
</div>