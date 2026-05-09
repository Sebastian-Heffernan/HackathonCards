<script>
  let { deckSize = 5 } = $props(); // Number of visible layers to show thickness
</script>

<div class="relative w-48">
  {#each Array(deckSize) as _, i}
    <img 
      src="/cards/card_back.png" 
      alt="Card Deck"
      class="absolute w-32 rounded-lg border border-gray-400"
      style="transform: translate({i * -1}px, {i * -2}px); z-index: {i};"
    />
  {/each}
</div>

<style>
  /* Optional: adds a slight 3D perspective */
  div {
    perspective: 1000px;
  }
</style>
