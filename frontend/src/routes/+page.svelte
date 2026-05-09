<script lang="ts">
   import RuleEditor from "$lib/components/RuleEditor.svelte";
   import { goto } from "$app/navigation";
   import { tick } from "svelte";
   let editorRef: any;

   // svelte-ignore non_reactive_update
   let textarea: HTMLTextAreaElement;

  let rules = $state(`
LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck
    DECK MAKE discard
    DECK CLEAR discard

    VARG SET P0_SCORE 0
    VARG SET P1_SCORE 0
    VARG SET P0_STOOD 0
    VARG SET P1_STOOD 0
    VARG SET status "Blackjack started"

    DRAW deck 0 1
    DRAW deck 1 1
    DRAW deck 0 1
    DRAW deck 1 1

    REVEAL 0
    REVEAL 1

    CALL SCORE_P0
    CALL SCORE_P1

    ASSERT HIT 0
    ASSERT STAND 0
    ASSERT HIT 1
    ASSERT STAND 1

    END_TURN 0

LABEL HIT:
    COMPARE $turnPlayer == 0
    GOTO HIT_P0
    GOTO HIT_P1

LABEL HIT_P0:
    DRAW deck 0 1
    REVEAL 0
    CALL SCORE_P0
    COMPARE P0_SCORE > 21
    GOTO P0_BUST
    END_TURN 0

LABEL HIT_P1:
    DRAW deck 1 1
    REVEAL 1
    CALL SCORE_P1
    COMPARE P1_SCORE > 21
    GOTO P1_BUST
    END_TURN 1

LABEL STAND:
    COMPARE $turnPlayer == 0
    GOTO STAND_P0
    GOTO STAND_P1

LABEL STAND_P0:
    VARG SET P0_STOOD 1
    END_TURN 1

LABEL STAND_P1:
    VARG SET P1_STOOD 1
    GOTO FINAL_SCORE

LABEL P0_BUST:
    VARG SET status "Player_0_busts._Player_1_wins."
    END_TURN

LABEL P1_BUST:
    VARG SET status "Player_1_busts._Player_0_wins."
    END_TURN

LABEL FINAL_SCORE:
    COMPARE P0_SCORE > P1_SCORE
    GOTO P0_WIN

    COMPARE P1_SCORE > P0_SCORE
    GOTO P1_WIN

    GOTO PUSH

LABEL P0_WIN:
    VARG SET status "Player_0_wins."
    END_TURN

LABEL P1_WIN:
    VARG SET status "Player_1_wins."
    END_TURN

LABEL PUSH:
    VARG SET status "Push."
    END_TURN

LABEL SCORE_P0:
    VARG SET P0_SCORE 0
    VARG SET cardIdx 0
    HANDLEN handLen 0
    GOTO SCORE_P0_LOOP

LABEL SCORE_P0_LOOP:
    COMPARE cardIdx < handLen
    GOTO SCORE_P0_CARD
    RETURN

LABEL SCORE_P0_CARD:
    VALUE cardValue 0 cardIdx
    CALL ADD_TO_P0
    MATH cardIdx + 1
    GOTO SCORE_P0_LOOP

LABEL ADD_TO_P0:
    COMPARE cardValue == "A"
    GOTO P0_ADD_ACE

    COMPARE cardValue == "K"
    GOTO P0_ADD_FACE

    COMPARE cardValue == "Q"
    GOTO P0_ADD_FACE

    COMPARE cardValue == "J"
    GOTO P0_ADD_FACE

    GOTO P0_ADD_NUMBER

LABEL P0_ADD_ACE:
    MATH P0_SCORE + 11
    RETURN

LABEL P0_ADD_FACE:
    MATH P0_SCORE + 10
    RETURN

LABEL P0_ADD_NUMBER:
    MATH P0_SCORE + cardValue
    RETURN

LABEL SCORE_P1:
    VARG SET P1_SCORE 0
    VARG SET cardIdx 0
    HANDLEN handLen 1
    GOTO SCORE_P1_LOOP

LABEL SCORE_P1_LOOP:
    COMPARE cardIdx < handLen
    GOTO SCORE_P1_CARD
    RETURN

LABEL SCORE_P1_CARD:
    VALUE cardValue 1 cardIdx
    CALL ADD_TO_P1
    MATH cardIdx + 1
    GOTO SCORE_P1_LOOP

LABEL ADD_TO_P1:
    COMPARE cardValue == "A"
    GOTO P1_ADD_ACE

    COMPARE cardValue == "K"
    GOTO P1_ADD_FACE

    COMPARE cardValue == "Q"
    GOTO P1_ADD_FACE

    COMPARE cardValue == "J"
    GOTO P1_ADD_FACE

    GOTO P1_ADD_NUMBER

LABEL P1_ADD_ACE:
    MATH P1_SCORE + 11
    RETURN

LABEL P1_ADD_FACE:
    MATH P1_SCORE + 10
    RETURN

LABEL P1_ADD_NUMBER:
    MATH P1_SCORE + cardValue
    RETURN
`);

   let userName = $state("username");
   let joinLobbyCode = $state("");
   let showCreateLobbyModal = $state(false);

   type Lobby = {
      id: string;
      name: string;
      playerCount: number;
   };

   let lobbies: Lobby[] = [
      { id: "1", name: "ABC123", playerCount: 2 },
      { id: "2", name: "XYZ789", playerCount: 3 },
      { id: "3", name: "LMN456", playerCount: 1 },
   ];

   async function openModal() {
      showCreateLobbyModal = true;
      await tick();
   }

   async function sendRules() {
      const response = await fetch("/api/rules", {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            source: rules,
         }),
      });

      const data = await response.json();
      return data.ruleId;
   }

   async function createLobby() {
      const ruleId = await sendRules();

      const response = await fetch("/api/lobbies", {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            rule_id: ruleId,
            host_name: userName,
         }),
      });

      const data = await response.json();

      sessionStorage.setItem("gameId", data.gameId);
      sessionStorage.setItem("playerId", data.playerId);
      sessionStorage.setItem("lobbyCode", data.lobbyCode);

      goto(`/lobby/${data.lobbyCode}`);
   }

   async function joinLobby(lobbyCode: string) {
      const response = await fetch(`/api/lobbies/${lobbyCode}/join`, {
         method: "POST",
         headers: {
            "Content-Type": "application/json",
         },
         body: JSON.stringify({
            name: userName,
         }),
      });

      const data = await response.json();

      sessionStorage.setItem("gameId", data.gameId);
      sessionStorage.setItem("playerId", data.playerId);
      sessionStorage.setItem("lobbyCode", data.lobbyCode);

      goto(`/lobby/${data.lobbyCode}`);
   }
</script>

<!-- Page Wrapped -->
<div class="min-h-screen bg-gray-100 flex flex-col">
   <!-- Header -->
   <header class="flex items-center justify-center p-4 bg-white shadow">
      <!-- Left button -->
      <button
         class="absolute left-4 text-sm font-semibold px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-800"
         onclick={() => goto("/docs/overview")}
      >
         How to Play
      </button>
      <!-- Title - Cardssembly -->
      <h1 class="text-2xl font-bold text-center">Cardssembly</h1>

      <!-- Create Lobby Button -->
      <button
         class="absolute right-4 text-3xl font-bold px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-800"
         onclick={openModal}
      >
         +Create Lobby
      </button>
   </header>

   <main class="flex-1 flex flex-col items-center p-6">
      <!-- Welcome message -->
      <p class="text-lg text-gray-600 mb-6 text-center">
         Welcome to Cardssembly! Join or create a lobby to start playing.
      </p>

      <!-- Section title -->
      <h2 class="text-xl text-gray-400 text-center font-semibold mb-4">
         Available Lobbies
      </h2>

      <!-- Lobby Table -->
      <div class="flex justify-center w-full">
         <div
            class="w-full max-w-3xl min-h-[500px] bg-white shadow rounded overflow-hidden flex flex-col"
         >
            <div class="divide-y">
               <!-- Table Headers -->
               <div
                  class="grid grid-cols-[3fr_1fr] divide-x divide-black bg-gray-200 p-3 text-base font-semibold text-center"
               >
                  <div>Lobby Name</div>
                  <div class="text-right text-center">Players</div>
               </div>
               <!-- ROWS -->
               <div class="flex-1">
                  {#each lobbies as lobby, i}
                     <!-- svelte-ignore a11y_click_events_have_key_events -->
                     <!-- svelte-ignore a11y_no_static_element_interactions -->
                     <div
                        class="grid grid-cols-[3fr_1fr] divide-x divide-black items-stretch border-t p-3 hover:bg-gray-50 cursor-pointer
                        {i === lobbies.length - 1
                           ? 'border-b-2 border-black'
                           : ''}"
                        onclick={() => joinLobby(lobby.name)}
                     >
                        <div
                           class="pr-4 font-bold text-gray-900 text-center text-sm"
                        >
                           {lobby.name}
                        </div>

                        <div
                           class="text-right flex items-center justify-end pr-2"
                        >
                           {lobby.playerCount}
                        </div>
                     </div>
                  {/each}
               </div>
            </div>
         </div>
      </div>

      <div class="mt-6 w-full max-w-3xl bg-white shadow rounded p-4">
         <h2 class="text-lg font-bold mb-3 text-center">Join Lobby by Code</h2>

         <div class="flex flex-col md:flex-row gap-3">
            <input
               bind:value={userName}
               placeholder="Username"
               class="border border-gray-300 rounded px-3 py-2 flex-1"
            />

            <input
               bind:value={joinLobbyCode}
               placeholder="Lobby Code"
               class="border border-gray-300 rounded px-3 py-2 flex-1 uppercase"
            />

            <button
               class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-800"
               onclick={() => joinLobby(joinLobbyCode)}
               disabled={!joinLobbyCode || !userName}
            >
               Join Lobby
            </button>
         </div>
      </div>
   </main>
   {#if showCreateLobbyModal}
      <!-- BACKDROP -->
      <div
         class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      >
         <!-- MODAL -->
         <div
            class="bg-white rounded-lg shadow-lg w-[90vw] max-w-5xl h-[85vh] p-6 flex flex-col min-h-0"
         >
            <!-- TITLE -->
            <h2 class="text-xl font-bold mb-4 text-center">Create Lobby</h2>
            <div class="flex-1 flex flex-col min-h-0">
               <!-- INPUT -->
               <RuleEditor bind:value={rules} bind:this={editorRef} />
            </div>

            <!-- BUTTONS -->
            <div class="flex justify-center gap-2">
               <button
                  class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
                  onclick={() => (showCreateLobbyModal = false)}
               >
                  Cancel
               </button>

               <button
                  class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-800"
                  onclick={createLobby}
               >
                  Create
               </button>
            </div>
         </div>
      </div>
   {/if}
</div>
