<!-- 

This is a demo of blackjack

-->
<script>
import Hand from "./Hand.svelte";
import Deck from "./Deck.svelte";
import { Suits } from "$lib/suit.ts";

const gameState = {

};

const actions = ["Hit", "Stand"];
const opponent_cards = [{
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
}];
const cards = [{
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
</script>

<div class="relative w-screen h-screen p-4 bg-green-500">
  <!--  -->
  <div class="nes-container with-title absolute t-0 l-0 w-40">
    <p class="title">Decks</p>
    <Deck />
  </div>
  <!--  -->
  <div class="absolute t-0 r-0">

  </div>

  <!-- Your Hand -->
  <div class="absolute bottom-4 left-1/2 -translate-x-1/2">
    <Hand actions={actions} cards={cards} />
  </div>

  <!-- Opponent Hand -->
  <div class="absolute top-4 left-1/2 -translate-x-1/2">
    <Hand actions={actions} cards={opponent_cards} isOpponent={true} />
  </div>
</div>
