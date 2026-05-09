<script lang="ts">
  import Card from "$lib/components/Card.svelte";

  type CardData = {
    suit: string;
    value: string;
  };

  let {
    cards,
    actions = [],
    isOpponent = false,
    onCardClick = () => {},
    selected = [],
    playAction = () => {}
  } = $props<{
    cards: CardData[];
    actions?: string[];
    isOpponent?: boolean;
    onCardClick?: (cardIdx: number) => void;
    selected?: boolean[];
    playAction?: (actionIdx: number) => void;
  }>();
</script>

<div class="w-full h-full flex flex-col items-center">
  <div class="flex">
    {#each cards as card, cardIdx}
      <button
        class="focus:outline-none outline-none border-none focus-visible:outline-none"
        onclick={() => onCardClick(cardIdx)}
        disabled={isOpponent}
      >
        <Card
          suit={card.suit}
          value={card.value}
          isOpponent={isOpponent}
          selected={selected[cardIdx] ?? false}
        />
      </button>
    {/each}
  </div>

  {#if !isOpponent}
    <div class="flex gap-4">
      {#each actions as action, actionIdx}
        <button onclick={() => { playAction(actionIdx) }} type="button" class="nes-btn is-primary">
          {action}
        </button>
      {/each}
    </div>
  {/if}
</div>