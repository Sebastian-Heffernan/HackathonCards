<script>

  import Card from "$lib/components/Card.svelte";

  let { cards, actions, isOpponent = false } = $props();

  function press_button(action) {
    
  }
</script>

<div class="w-full h-full flex flex-col items-center">
  <!-- Cards -->
  <div class="flex">
    {#each cards as card}
      <Card suit={card.suit} value={card.value}/>
    {/each}
  </div>

  <!-- Actions -->
  {#if !isOpponent}
     <!-- content here -->
    <div class="flex gap-4">
      {#each actions as action}
        <button onClick={() => { press_button(action) }} type="button" class="nes-btn is-primary">{action}</button>
      {/each}
    </div>
  {/if}
  


</div>



