<script>
  let { suit, value, selected = false } = $props();
  let img = value === "UNKNOWN" ? "card_back.png" : `card_${suit}_${value}.png`;
</script>

<div class="relative transition-transform duration-200 ease-in-out hover:-translate-y-6 
            {selected ? '-translate-y-6' : ''} 
            first:ml-0 -ml-16">
  <img src={`/cards/${img}`} alt={`${value} of ${suit}`} class="w-32 min-w-[6rem] rounded-lg"/>
</div>
