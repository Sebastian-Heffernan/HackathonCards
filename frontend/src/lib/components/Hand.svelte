<script>
  let { cards, actions } = $props();

  function press_button(action) {
    
  }
</script>

<div class="w-full h-full flex flex-col">
  <!-- Cards -->
  <div class="flex">
    {#each cards as card}
      <Card suit={card.suit} value={card.value}/>
    {/each}
  </div>

  <!-- Actions -->
  <div>
    {#each actions as action}
      <button onClick={() => { press_button(action) }}></button>
    {/each}
  </div>


</div>



