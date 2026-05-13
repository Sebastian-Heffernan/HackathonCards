# Conceptual planning
What each game conseptually requires
## Blackjack
- [ ] Player's hand
- [ ] Opponent's hand
- [ ] Hiding/showing card to specific players/all.
- [ ] Draw/discard decks.
- [ ] Picking/storing a dealer.
Mechanics:
- [ ] Hit
  - [ ] Draw card
  - [ ] Check if sum over 21
  - [ ] Lose/continue
- [ ] Stay
  - [ ] Next turn

## Here to slay
https://cdn.1j1ju.com/medias/2e/32/cd-here-to-slay-rulebook.pdf

Each player's zones:
- [ ] Party leader
- [ ] Slayed monsters
- [ ] Hero cards in play
- [ ] Deck

Central zones:
- [ ] Party leader cards deck (drawn out on start, not accecible during gameplay)
- [ ] Monster cards deck (hidden)
- [ ] Monster cards in play (3, face up, side by side)
- [ ] Main deck (hidden)
- [ ] Discard deck (face up, searchable)

Turn logic:
- [ ] 3 action points to spend on:
  - [ ] 1x Draw card from main deck
  - [ ] 1x Play Hero, Item, Magic from hand. Heroes rolled for immediately.
  - [ ] 1x Roll dice to use effect of prev played hero.
  - [ ] 2x Attack monster.
  - [ ] 3x Discrard whole hand, draw 5 cards.

Hero classes:
- [ ] Fighter
- [ ] Guardian
- [ ] Ranger
- [ ] Thief
- [ ] Wizard
- [ ] Bard
- [ ] Generic (any hero)

Card types:
- [ ] Hero - (class, effect)
  - [ ] Roll requirement - min to play card.
  - [ ] Unlimited number of.
- [ ] Item - (effect)
  - [ ] Attached to Heroes.
  - [ ] Only one to Hero at a time.
  - [ ] If hero destroyed/stolen etc. Item goes with it.
- [ ] Magic - (effect)
  - [ ] Single use, move to disard pile.
- [ ] Modifier
  - [ ] Played instantly from hand when ANYONE rolls dice. Changes roll result.
  - [ ] Allow for choices w cards like (+1, -3)
- [ ] Challenge
  - [ ]  You may CHALLENGE another player by playing a Challenge card on that player’s turn when that player attempts to play a Hero, Item, or Magic card from their hand. Playing a Challenge card does not cost any action points.When you CHALLENGE another player, each of you must roll two dice. If your roll is equal to or higher than the other player’s roll, you successfully prevent that player from playing their Hero, Item, or Magic card. That player must immediately move the card they attempted to play to the discard pile (and that player does not get back an action point). If that player’s roll is higher, they may proceed with playing their card as planned. When modifying a Challenge roll, you may wait until both players have rolled before deciding whether or not to use your Modifier card. Each card can only be challenged once; if another player has already challenged the card being played, you may not CHALLENGE that card a second time