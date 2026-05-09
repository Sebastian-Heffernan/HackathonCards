<!-- 

This is a demo of blackjack

-->
<script lang="ts">
import Hand from "./Hand.svelte";
import Deck from "./Deck.svelte";
import { Suits } from "$lib/suit.ts";

import { writable } from 'svelte/store';

const gameState = {
  actions: ["Hit", "Stand"],
  masked_cards: [[{
    "suit": Suits.SPADES, 
    "value": "UNKNOWN"
  }, {
      "suit": Suits.SPADES, 
      "value": "UNKNOWN"
    }, {
      "suit": Suits.SPADES, 
      "value": "UNKNOWN"
    }, {
      "suit": Suits.SPADES, 
      "value": "UNKNOWN"
    }, {
      "suit": Suits.SPADES, 
      "value": "UNKNOWN"
    }]],
  cards: [{
    "suit": Suits.SPADES, 
    "value": "A"
  }, {
      "suit": Suits.SPADES, 
      "value": "02"
    }, {
      "suit": Suits.SPADES, 
      "value": "02"
    }, {
      "suit": Suits.SPADES, 
      "value": "02"
    }, {
      "suit": Suits.SPADES, 
      "value": "02"
    }]
};

// Use a reactive state for the selection array
let selected = $state(
  gameState?.cards?.length 
    ? new Array(gameState.cards.length).fill(false) 
    : []
);
const toggleCard = (i: number) => {
  console.log("HIHIHI");
  selected[i] = !selected[i]; // This will now trigger UI updates
};

const isCardSelected = (i: number) => {
  return selected[i];
};

const playAction = (actionIdx: number) => {
  // Filter cards to find which ones are currently true
  const chosenCards = gameState.cards.filter((_, i) => selected[i]);
  console.log("Playing action with:", chosenCards);
};

</script>

<div class="relative w-screen h-screen p-4 bg-green-500">
  <!--  -->
  <div class="nes-container with-title absolute t-0 l-0 w-40 h-full is-dark">
    <p class="title">Decks</p>
    <Deck />
  </div>

  <!-- Your Hand -->
  <div class="absolute bottom-4 left-1/2 -translate-x-1/2">
    <Hand actions={gameState.actions} cards={gameState.cards} onCardClick={toggleCard} {selected} {playAction} />
  </div>

  <!-- Opponent Hand -->
  {#each gameState.masked_cards as opponent_cards}
     <!-- content here -->
    <div class="absolute top-4 left-1/2 -translate-x-1/2">
      <Hand actions={[]} cards={opponent_cards} isOpponent={true} selected={[]} />
    </div>
  {/each}
  
</div>
