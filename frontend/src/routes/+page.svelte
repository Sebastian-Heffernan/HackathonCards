<script lang="ts">
   import { goto } from "$app/navigation";
   import { tick } from "svelte";

   // svelte-ignore non_reactive_update
   let textarea: HTMLTextAreaElement;

  let rules = $state(
`LABEL SETUP:
    DECK MAKE deck
    DECK SHUFFLE deck
    DECK MAKE discard
    CALL FUNC
    ASSERT DRAW_CARD 0
    ASSERT REMOVE_CARD 0
    GOTO TEST
LABEL TEST:
    END_TURN
LABEL FUNC:
    DRAW deck 0 2
    REVEAL 0
    PRINT playerStates[0].hand
    RETURN
LABEL DRAW_CARD:
    DRAW deck 0 1
    REVEAL 0
    END_TURN
LABEL REMOVE_CARD:
   COMPARE -1 < $selectedCardId
   GOTO REMOVE_CARD_ACTION
   END_TURN
LABEL REMOVE_CARD_ACTION
   MOVE discard 0 $selectedCardId
   END_TURN`);

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
      textarea?.focus();
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
         onclick={() => goto("/docs/getting-started")}
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
         +
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
            class="bg-white rounded-lg shadow-lg w-[90vw] max-w-5xl h-[85vh] p-6 flex flex-col"
         >
            <!-- TITLE -->
            <h2 class="text-xl font-bold mb-4 text-center">Create Lobby</h2>
            <div class="flex-1 flex flex-col">
               <!-- INPUT -->
               <textarea
                  bind:this={textarea}
                  bind:value={rules}
                  placeholder="Enter lobby rules..."
                  class="w-full h-128 border border-gray-300 rounded p-4 text-lg text-left resize-none leading-normal"
               >
               </textarea>
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
