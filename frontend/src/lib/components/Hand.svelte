<script lang="ts">

  import Card from "$lib/components/Card.svelte";

  let { cards, actions, isOpponent = false, onCardClick, selected, playAction } = $props();

</script>

<div class="w-full h-full flex flex-col items-center">
  <!-- Cards -->
  <div class="flex">
    {#each cards as card, cardIdx}
      <button class="focus:outline-none outline-none border-none focus-visible:outline-none" onclick={() => {onCardClick(cardIdx)}}>
        <Card suit={card.suit} value={card.value} isOpponent={isOpponent} selected={selected[cardIdx]} />
      </button>
    {/each}
  </div>

  <!-- Actions -->
  {#if !isOpponent}
     <!-- content here -->
    <div class="flex gap-4">
      {#each actions as action, actionIdx}
        <button onclick={() => { playAction(actionIdx) }} type="button" class="nes-btn is-primary">{action}</button>
      {/each}
    </div>
  {/if}
  


</div>



