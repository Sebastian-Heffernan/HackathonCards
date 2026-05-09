<script lang="ts">
   import RuleEditor from "$lib/components/RuleEditor.svelte";
   import { goto } from "$app/navigation";
   import { tick } from "svelte";
   let editorRef: any;

   // svelte-ignore non_reactive_update
   let textarea: HTMLTextAreaElement;

   let showCompilationErrorPopup = $state(false);
   let compilationErrorMessage = $state("");

  let rules = $state(`
LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck

    VARG SET $winner -1
    VARG SET status "highest_card_waiting"
    VARG SET bestValue -1
    VARG SET bestPlayer -1
    VARG SET drawnCount 0

    SHOW_VAR status
    SHOW_VAR $winner
    SHOW_VAR bestValue
    SHOW_VAR bestPlayer
    SHOW_VAR drawnCount

    ASSERT SHOWDOWN
    END_TURN 0

LABEL SHOWDOWN:
    DRAW deck $turnPlayer 1
    REVEAL $turnPlayer

    MATH drawnCount + 1

    COMPARE drawnCount < $playerCount
    GOTO NEXT_PLAYER
    GOTO SCORE_START

LABEL NEXT_PLAYER:
    END_TURN $turnPlayer + 1

LABEL SCORE_START:
    VARG SET i 0
    VARG SET bestValue -1
    VARG SET bestPlayer -1
    VARG SET status "scoring"
    GOTO SCORE_ALL

LABEL SCORE_ALL:
    VALUE cardValue i 0
    CALL CARD_TO_VALUE

    COMPARE cardScore > bestValue
    GOTO NEW_BEST
    GOTO NEXT_SCORE

LABEL NEW_BEST:
    VARG SET bestValue cardScore
    VARG SET bestPlayer i
    GOTO NEXT_SCORE

LABEL NEXT_SCORE:
    MATH i + 1
    COMPARE i < $playerCount
    GOTO SCORE_ALL
    GOTO FINISH_GAME

LABEL FINISH_GAME:
    VARG SET $winner bestPlayer
    VARG SET status "highest_card_winner"
    END_TURN

LABEL CARD_TO_VALUE:
    COMPARE cardValue == "A"
    GOTO CARD_A

    COMPARE cardValue == "K"
    GOTO CARD_K

    COMPARE cardValue == "Q"
    GOTO CARD_Q

    COMPARE cardValue == "J"
    GOTO CARD_J

    GOTO CARD_NUMBER

LABEL CARD_A:
    VARG SET cardScore 14
    RETURN

LABEL CARD_K:
    VARG SET cardScore 13
    RETURN

LABEL CARD_Q:
    VARG SET cardScore 12
    RETURN

LABEL CARD_J:
    VARG SET cardScore 11
    RETURN

LABEL CARD_NUMBER:
    VARG SET cardScore cardValue
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

      if (!data.ok) {
         compilationErrorMessage = data.error ?? "Compilation failed";
         showCompilationErrorPopup = true;
         return null;
      }

      return data.ruleId;
   }

   async function createLobby() {
      const ruleId = await sendRules();

      if (!ruleId) {
         return;
      }

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
               <RuleEditor bind:value={rules} editable={true} />
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
   {#if showCompilationErrorPopup}
      <div class="fixed inset-0 bg-black/50 flex items-center justify-center z-[100]">
         <div class="bg-white rounded-lg shadow-lg max-w-lg w-[90vw] p-6">
            <h2 class="text-xl font-bold mb-3 text-red-600">
               Compilation Error
            </h2>

            <p class="mb-6 whitespace-pre-wrap">
               {compilationErrorMessage}
            </p>

            <div class="flex justify-center">
               <button
                  class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-800"
                  onclick={() => (showCompilationErrorPopup = false)}
               >
                  OK
               </button>
            </div>
         </div>
      </div>
   {/if}
</div>
