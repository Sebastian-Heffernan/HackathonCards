// src/lib/docsData.js
export const docsData = {
  "overview": {
    title: "Overview",
    content: "An introduction to the language syntax. How to read the notation",
  },
  "commenting": {
    title: "Commenting",
    content: "An introduction to commmenting.",
    items: {
      "Getting Started": {
        name: "Getting Started",
        description: "To do comments, use '#' to comment out.\nIt should be noted that commenting in cardssembly should be done on a separate line.\n",
        example: "# Commenting line\nASSERT label\n\nEND_TURN # This is a bad comment because it leaks into the END_TURN args"
      }
    },  
  },
  "examples" : {
    title: "Working examples",
    content: "These are working examples made by the team that can be inserted into a lobby",
    items: {
      "Loops": {
        name: "Fun with Loops",
        description: "A showcase of how Cardssembly has built-in loop functionality.",
        example: 'LABEL SETUP:\n DECK MAKE deck\n VARG SET i 0\n CALL LOOP\n END_TURN\n LABEL LOOP:\n DRAW deck 0 1\n REVEAL 0\n MATH i + 1\n COMPARE i < 10\n GOTO LOOP\n RETURN\n'
      },
      "Card Drawing": {
        name: "Card Drawing",
        description: "Simple Code which allows for players to draw and remove cards on their turn, and finally end turn\n",
        example: 'LABEL SETUP:\n    DECK MAKE deck\n    DECK SHUFFLE deck\n    DECK MAKE discard\n    ASSERT DRAW_CARD\n    ASSERT REMOVE_CARD\n    ASSERT TURN_FINISH\n    END_TURN\nLABEL DRAW_CARD:\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    END_TURN\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    MOVE discard 0 $selectedCardId\n    END_TURN\nLABEL TURN_FINISH:\n    END_TURN $turnPlayer + 1\n'
      },
      "Showdown": {
        name: "Showdown",
        description: "A tense, single-card elimination game for n players.\nPlayers take turns pressing the 'Showdown' button to flip their card.\nWhoever has the largest card value wins.",
        example: 'LABEL SETUP:\n DECK MAKE deck\n DECK SHUFFLE deck\n \n VARG SET $winner -1\n VARG SET status "highest_card_waiting"\n VARG SET bestValue -1\n VARG SET bestPlayer -1\n VARG SET drawnCount 0\n \n SHOW_VAR status\n SHOW_VAR $winner\n SHOW_VAR bestValue\n SHOW_VAR bestPlayer\n SHOW_VAR drawnCount\n \n ASSERT SHOWDOWN\n END_TURN 0\n \n LABEL SHOWDOWN:\n DRAW deck $turnPlayer 1\n REVEAL $turnPlayer\n \n MATH drawnCount + 1\n \n COMPARE drawnCount < $playerCount\n GOTO NEXT_PLAYER\n GOTO SCORE_START\n \n LABEL NEXT_PLAYER:\n END_TURN $turnPlayer + 1\n \n LABEL SCORE_START:\n VARG SET i 0\n VARG SET bestValue -1\n VARG SET bestPlayer -1\n VARG SET status "scoring"\n GOTO SCORE_ALL\n \n LABEL SCORE_ALL:\n VALUE cardValue i 0\n CALL CARD_TO_VALUE\n \n COMPARE cardScore > bestValue\n GOTO NEW_BEST\n GOTO NEXT_SCORE\n \n LABEL NEW_BEST:\n VARG SET bestValue cardScore\n VARG SET bestPlayer i\n GOTO NEXT_SCORE\n \n LABEL NEXT_SCORE:\n MATH i + 1\n COMPARE i < $playerCount\n GOTO SCORE_ALL\n GOTO FINISH_GAME\n \n LABEL FINISH_GAME:\n VARG SET $winner bestPlayer\n VARG SET status "highest_card_winner"\n END_TURN\n \n LABEL CARD_TO_VALUE:\n COMPARE cardValue == "A"\n GOTO CARD_A\n \n COMPARE cardValue == "K"\n GOTO CARD_K\n \n COMPARE cardValue == "Q"\n GOTO CARD_Q\n \n COMPARE cardValue == "J"\n GOTO CARD_J\n \n GOTO CARD_NUMBER\n \n LABEL CARD_A:\n VARG SET cardScore 14\n RETURN\n \n LABEL CARD_K:\n VARG SET cardScore 13\n RETURN\n \n LABEL CARD_Q:\n VARG SET cardScore 12\n RETURN\n \n LABEL CARD_J:\n VARG SET cardScore 11\n RETURN\n \n LABEL CARD_NUMBER:\n VARG SET cardScore cardValue\n RETURN\n'
      },
      "2 Player Blackjack": {
        name: "2 Player Blackjack",
        description: "This Version of Blackjack will treat the host as the player, whereas the client (2nd player) is the dealer.\n",
        example: 'LABEL SETUP:\n DECK MAKE deck\n DECK SHUFFLE deck\n DECK MAKE discard\n DECK CLEAR discard\n \n VARG SET P0_SCORE 0\n VARG SET P1_SCORE 0\n VARG SET P0_STOOD 0\n VARG SET P1_STOOD 0\n VARG SET status "game_playing"\n SHOW_VAR status\n \n DRAW deck 0 1\n REVEAL 0\n DRAW deck 1 1\n DRAW deck 0 1\n DRAW deck 1 1\n \n REVEAL 0\n REVEAL 1\n \n CALL SCORE_P0\n CALL SCORE_P1\n \n ASSERT HIT\n ASSERT STAND\n \n END_TURN 0\n \n LABEL HIT:\n COMPARE $turnPlayer == 0\n GOTO HIT_P0\n GOTO HIT_P1\n \n LABEL HIT_P0:\n DRAW deck 0 1\n REVEAL 0\n CALL SCORE_P0\n COMPARE P0_SCORE > 21\n GOTO P0_BUST\n END_TURN 0\n \n LABEL HIT_P1:\n DRAW deck 1 1\n REVEAL 1\n CALL SCORE_P1\n COMPARE P1_SCORE > 21\n GOTO P1_BUST\n END_TURN 1\n \n LABEL STAND:\n COMPARE $turnPlayer == 0\n GOTO STAND_P0\n GOTO STAND_P1\n \n LABEL STAND_P0:\n VARG SET P0_STOOD 1\n END_TURN 1\n \n LABEL STAND_P1:\n VARG SET P1_STOOD 1\n GOTO FINAL_SCORE\n \n LABEL P0_BUST:\n VARG SET status "Player_0_busts._Player_1_wins."\n VARG SET $winner 1\n END_TURN\n \n LABEL P1_BUST:\n VARG SET status "Player_1_busts._Player_0_wins."\n VARG SET $winner 0\n END_TURN\n \n LABEL FINAL_SCORE:\n COMPARE P0_SCORE > P1_SCORE\n GOTO P0_WIN\n \n COMPARE P1_SCORE > P0_SCORE\n GOTO P1_WIN\n \n GOTO PUSH\n \n LABEL P0_WIN:\n VARG SET status "Player_0_wins."\n VARG SET $winner 0\n END_TURN\n \n LABEL P1_WIN:\n VARG SET status "Player_1_wins."\n VARG SET $winner 1\n END_TURN\n \n LABEL PUSH:\n VARG SET status "Push."\n END_TURN\n \n LABEL SCORE_P0:\n VARG SET P0_SCORE 0\n VARG SET cardIdx 0\n HANDLEN handLen 0\n GOTO SCORE_P0_LOOP\n \n LABEL SCORE_P0_LOOP:\n COMPARE cardIdx < handLen\n GOTO SCORE_P0_CARD\n RETURN\n \n LABEL SCORE_P0_CARD:\n VALUE cardValue 0 cardIdx\n CALL ADD_TO_P0\n MATH cardIdx + 1\n GOTO SCORE_P0_LOOP\n \n LABEL ADD_TO_P0:\n COMPARE cardValue == "A"\n GOTO P0_ADD_ACE\n \n COMPARE cardValue == "K"\n GOTO P0_ADD_FACE\n \n COMPARE cardValue == "Q"\n GOTO P0_ADD_FACE\n \n COMPARE cardValue == "J"\n GOTO P0_ADD_FACE\n \n GOTO P0_ADD_NUMBER\n \n LABEL P0_ADD_ACE:\n MATH P0_SCORE + 11\n RETURN\n \n LABEL P0_ADD_FACE:\n MATH P0_SCORE + 10\n RETURN\n \n LABEL P0_ADD_NUMBER:\n MATH P0_SCORE + cardValue\n RETURN\n \n LABEL SCORE_P1:\n VARG SET P1_SCORE 0\n VARG SET cardIdx 0\n HANDLEN handLen 1\n GOTO SCORE_P1_LOOP\n \n LABEL SCORE_P1_LOOP:\n COMPARE cardIdx < handLen\n GOTO SCORE_P1_CARD\n RETURN\n \n LABEL SCORE_P1_CARD:\n VALUE cardValue 1 cardIdx\n CALL ADD_TO_P1\n MATH cardIdx + 1\n GOTO SCORE_P1_LOOP\n \n LABEL ADD_TO_P1:\n COMPARE cardValue == "A"\n GOTO P1_ADD_ACE\n \n COMPARE cardValue == "K"\n GOTO P1_ADD_FACE\n \n COMPARE cardValue == "Q"\n GOTO P1_ADD_FACE\n \n COMPARE cardValue == "J"\n GOTO P1_ADD_FACE\n \n GOTO P1_ADD_NUMBER\n \n LABEL P1_ADD_ACE:\n MATH P1_SCORE + 11\n RETURN\n \n LABEL P1_ADD_FACE:\n MATH P1_SCORE + 10\n RETURN\n \n LABEL P1_ADD_NUMBER:\n MATH P1_SCORE + cardValue\n RETURN\n'
      },
      
    }

  },
  "instructions": {
    title: "Instruction Set",
    content: "A complete list of available opcodes.",
    // Nested dictionary for specific instructions
    items: {
      "ASSERT": {
        name: "ASSERT",
        description: "Makes a button with the provided label parameters.\n Additional arguments can be left empty in order to call assert for all players.",
        usage: "ASSERT [label: str] | [label: str][player: int]",
        example: "LABEL SETUP:\n  # Create a button called END_GAME\n  ASSERT END_GAME\nLABEL END_GAME:\n  VARG SET $winner 0\n  END_TURN\n",
      },
      "CALL": {
        name: "CALL",
        description: "Jumps to a specific label and process, while retaining where it left off.\n Requires calling RETURN in order to return back to where it left off.\n",
        usage: "CALL [label: str]",
        example: 'LABEL SETUP:\n  DECK MAKE deck\n  VARG SET i 0\n  # Use CALL to go to LOOP\n  CALL LOOP\n  END_TURN\nLABEL LOOP:\n  DRAW deck 0 1\n  REVEAL 0\n  MATH i + 1\n  COMPARE i < 10\n  GOTO LOOP\n  # Make sure to call RETURN at the end of the label you called!\n  RETURN\n',
      }, 
      "COMPARE": {
        name: "COMPARE",
        description: "Sets x = x + y for COMPARE x + y.\nOn true executes n+1. On false, n+2.\n Operators Include '==', '!=', '>', '<', '>=', '<='. \nLexiographical comparison is performed when x and y are strings, whereas normal comparison is done for integers.",
        usage: "COMPARE [x: int | str][operator: '==' | '!=' | '>' | '<' | '>=' | '<=' ][y: int | str]",
        example: "VARG SET x 0\nVARG SET y 0\n# Call compare to check if x equals to y numerically. In this case it does.\nCOMPARE x == y",
         warning: {
          about: "Ensure the same types (x = int, y = int, vice versa) are called",
          code: "# Good Case:\nCOMPARE 1 > 2\n# Bad Case:\nCOMPARE 1 > 'hello'",
        }
      },
      "DECK": {
        name: "DECK", 
        description: "Controls a specified deck by name through an action specified.",
        usage: "DECK [('MAKE' | 'SHUFFLE' | 'CLEAR' | 'RESET'): str][name: str]",
         example: 'LABEL SETUP:\n    # Call DECK MAKE to make an initial deck \n    DECK MAKE deck\n    # Call DECK SHUFFLE to shuffle the given deck\n    DECK SHUFFLE deck\n    # Call Deck MAKE discard to make a discard pile\n    DECK MAKE discard\n    ASSERT DRAW_CARD\n    ASSERT REMOVE_CARD\n    ASSERT TURN_FINISH\n    END_TURN\nLABEL DRAW_CARD:\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    END_TURN\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    MOVE discard 0 $selectedCardId\n    END_TURN\nLABEL TURN_FINISH:\n    END_TURN $turnPlayer + 1\n'
      }, 
      "DRAW": {
        name: "DRAW",
        description: "Takes a card from deck name to a players hand by a given number of times.",
        usage: "DRAW [deck_name: str][player_id: int][times: int]",
        example: 'LABEL SETUP:\n    DECK MAKE deck\n    DECK SHUFFLE deck\n    DECK MAKE discard\n    ASSERT DRAW_CARD\n    ASSERT REMOVE_CARD\n    ASSERT TURN_FINISH\n    END_TURN\nLABEL DRAW_CARD:\n    # Draw from the deck one card to the current player.\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    END_TURN\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    MOVE discard 0 $selectedCardId\n    END_TURN\nLABEL TURN_FINISH:\n    END_TURN $turnPlayer + 1\n'
      },
      "END_TURN": {
        name: "END_TURN",
        description: "Finishes the player's turn through finishing a label execution initiated by an action. Can break a loop",
        usage: "END_TURN [] | [next_index: int] | [VAR1][+ | -][VAR2 | i: int]",
        example: "LABEL SETUP:\n    DECK MAKE deck\n    DECK SHUFFLE deck\n    DECK MAKE discard\n    ASSERT DRAW_CARD\n    ASSERT REMOVE_CARD\n    ASSERT TURN_FINISH\n    END_TURN\nLABEL DRAW_CARD:\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    # Call END_TURN here once card is drawn.\n    END_TURN\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    MOVE discard 0 $selectedCardId\n    # Only End Turn here if no card is found.\n    END_TURN\nLABEL TURN_FINISH:\n    # End Turn of the current player, go to the next player\n    END_TURN $turnPlayer + 1\n"
      },
      "PASS": {
        name: "PASS",
        description: "Skips to n + 1 line, where n is the current line pointer.",
        usage: "PASS []",
        example: "COMPARE a > b \nPASS \nGOTO LABEL \n# Equivalent to if a > b, do nothing, else go to the label",
      },
      "GOTO": {
        name: "GOTO",
        description: "Jumps process to a given label, and begins processing its data.\n Does not retain its previous location during execution.\nSee CALL for more deatils.",
        usage: "GOTO [LABEL]",
        example: "LABEL TEST:\n   END_TURN\nLABEL SETUP:\n    # Call test label\n    GOTO TEST\n"
      },
      "HANDLEN": {
        name: "HANDLEN",
        description: "Stores the hand length of player, 'p' in VAR",
        usage: "HANDLEN [VAR][player_id: int][card_id: int]",
        example: "DECK MAKE deck\nDECK SHUFFLE\nDRAW deck 0\n# Calling hand length here would be a value of 1 stored in memory.\nHANDLEN p0length 0 0",
      },
      "MATH": {
        name: "MATH",
        description: "Performs mathematical operations between two labels, such as \n addition, subtraction, multiplication, division and modulus",
        usage: "MATH [x: str][enum: '+' | '-' | '*' | '/' | '%' ][y: str]",
        example: "LABEL SETUP:\n   DECK MAKE deck\n   VARG SET i 0\n   CALL LOOP\n   END_TURN\nLABEL LOOP:\n   DRAW deck 0 1\n   REVEAL 0\n   # Increment i by 1\n   MATH i + 1\n   COMPARE i < 10\n   GOTO LOOP\n   RETURN"
      },
      "MOVE": {
        name: "MOVE",
        description: "Moves a card from a player's hand and then move it to a specified deck",
        usage: "MOVE [DECK][player_idx: int][card_idx: int]",
        example: 'LABEL SETUP:\n    DECK MAKE deck\n    DECK SHUFFLE deck\n    DECK MAKE discard\n    ASSERT DRAW_CARD\n    ASSERT REMOVE_CARD\n    ASSERT TURN_FINISH\n    END_TURN\nLABEL DRAW_CARD:\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    END_TURN\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    # Move the selected card to the discard pile\n    MOVE discard 0 $selectedCardId\n    END_TURN\nLABEL TURN_FINISH:\n    END_TURN $turnPlayer + 1\n'
      },
      "REVEAL": {
        name: "REVEAL",
        description: "Specify a player's most recently drawn card (Lastmost Index).\n Sets its global visibility flag to TRUE for everybody.",
        usage: "REVEAL [player_idx: int]",
        example: "REVEAL 2"
      },
      "SUIT": {
        name: "SUIT",
        description: "Stores the suit of the card of player [p], in their hand at [c] into [VAR]",
        usage: "SUIT [VAR][player_idx: int][card_idx: int]",
        example: "DECK MAKE deck\nDECK SHUFFLE\nDRAW deck 0\n# Store the Suit of Player 1 (ID 0) of Card 1 (ID 0)\nSUIT varsuit 0 0"
      },
      "VALUE": {
        name: "VALUE",
        description: "Stores the value of the card at VAR",
        usage: "VALUE [VAR][player_idx: int][card_idx: int]",
        example: "DECK MAKE deck\nDECK SHUFFLE\nDRAW deck 0\n# Store the Value of Player 1 (ID 0) of Card 1 (ID 0)\nVALUE varvalue 0 0"
      },
      "VARG": {
        name: "VARG",
        description: "Declares a 'Game State' Variable. Server-Sided/Global Variable",
        usage: "VARG [SET][VAR][insert_value: str | int]",
        example: "# Initialise a A Global Variable, TOTAL of 5\nVARG TOTAL 5"
      },
      "SHOWVAR": {
        name: "SHOWVAR",
        description: "Adds a variable to showVars array, to then be shown to every client",
        usage: "SHOWVAR [NAME]",
        example: "VARG HELLO 0\n# Showvar Call Should be 0\nSHOWVAR VARG",
        warning: {
          about: "SHOWVAR should not be declared before a VARG declaration",
          code: "# This would work however it is not good practice.\nSHOWVAR variable\nVARG variable 1",
        }
      },
      "RETURN": {
        name: "RETURN",
        description: "Returns back to the last CALL on the stack trace.\n Works in Unison with CALL command.",
        usage: "RETURN []",
         example: 'LABEL SETUP:\n DECK MAKE deck\n VARG SET i 0\n # Use CALL to go to LOOP\n CALL LOOP\n END_TURN\nLABEL LOOP:\n DRAW deck 0 1\n REVEAL 0\n MATH i + 1\n COMPARE i < 10\n GOTO LOOP\n # Make sure to call RETURN at the end of the label you called!\n RETURN\n',
        warning: {
          about: "Don't use RETURN without having CALLed first",
          code: "# Bad Practice; Works however not good readability-wise.\nRETURN\nCALL label1",
        }
      },
    }
  },
  "registry": {
    title: "Registeries",
    content: "The regisiters in the game engine",
    items: {
      "$turnPlayer": {
        name: "Turn Player Register",
        description: "Tracks the current player's turn. \n Starts with a value of 0 for the first player",
        example: '# Draw Card for the current player via $turnPlayer \nLABEL DRAW_CARD:\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    END_TURN\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    # Move the selected card to the discard pile\n    MOVE discard 0 $selectedCardId\n    END_TURN\nLABEL TURN_FINISH:\n    END_TURN $turnPlayer + 1\n'
      },
      "$selectedCardId": {
        name: "Selected Card Register",
        description: "Tracks the currently selected card index.\n On Default, value is -1 if nothing is selected",
        example: '# Removed Card Label Compares against existing selecting card IDs\nLABEL REMOVE_CARD:\n    COMPARE -1 < $selectedCardId\n    GOTO REMOVE_CARD_ACTION\n    END_TURN\nLABEL REMOVE_CARD_ACTION\n    # Move the selected card to the discard pile\n    MOVE discard 0 $selectedCardId\n    END_TURN\nLABEL TURN_FINISH:\n    END_TURN $turnPlayer + 1\n'
      },
      "$playerCount": {
        name: "Player Count Register",
        description: "Tracks how many players are in the current game session.\n Checks game state.",
        example: "# Show Score for the Next Player\n LABEL NEXT_SCORE:\n MATH i + 1\n COMPARE i < $playerCount\n GOTO SCORE_ALL\n GOTO FINISH_GAME\n"
      },
      "$turnCount": {
        name: "Turn Count Register",
        description: "Tracks the count of turns performed by every player each game.\n Initially Starts off at 0 turns for the first turn.",
        example: "# Increment Turns each time a card is drawn.\n LABEL DRAW_CARD:\n    DRAW deck $turnPlayer 1\n    REVEAL 0\n    # Increment i by 1\n    MATH $turnCount + 1\n    END_TURN\n "
      },
      "$winner": {
        name: "Winner Flag Register",
        description: "Simple Flag which checks if there is a Winner.\n Initially starts off at -1 to declare that there are no winners.\n Set $winner to the winning players index",
        example: "LABEL SETUP:\n  ASSERT END_GAME\nLABEL END_GAME:\n   # Set winner flag to 0, where Player 1 is the winner.\n  VARG SET $winner 0\n  END_TURN\n"
      }
    }
  }
};
