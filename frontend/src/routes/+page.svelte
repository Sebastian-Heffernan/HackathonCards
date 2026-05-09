<script lang="ts">
   import { tick } from "svelte";
   let textarea: HTMLTextAreaElement;
async function openModal() {
	showCreateLobbyModal = true;
	await tick();
	textarea?.focus();
}
   let rules: string = $state("");
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

   let showCreateLobbyModal: boolean = $state(false);
</script>

<!-- Page Wrapped -->
<div class="min-h-screen bg-gray-100 flex flex-col">
   <!-- Header -->
   <header class="flex items-center justify-center p-4 bg-white shadow">
      <!-- Title - Cardssembly -->
      <h1 class="text-2xl font-bold text-center">Cardssembly</h1>

      <!-- Create Lobby Button -->
      <button  
         class="absolute right-4 text-3xl font-bold px-3 py-1 bg-blue-500 text-white rounded"
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
                     <div
                        class="grid grid-cols-[3fr_1fr] divide-x divide-black items-stretch border-t p-3 hover:bg-gray-50 cursor-pointer
                     {i === lobbies.length - 1
                           ? 'border-b-2 border-black'
                           : ''}"
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
   </main>
   {#if showCreateLobbyModal}
      <!-- BACKDROP -->
      <div
         class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      >
         <!-- MODAL -->
         <div class="bg-white rounded-lg shadow-lg w-[90vw] max-w-5xl h-[85vh] p-6 flex flex-col">
            <!-- TITLE -->
            <h2 class="text-xl font-bold mb-4 text-center">Create Lobby</h2>
            <div class="flex-1 flex flex-col">
            <!-- INPUT -->
            <textarea
               bind:this={textarea}
               bind:value={rules}
               placeholder="Enter lobby rules..."
               class="w-full h-128 border border-gray-300 rounded p-4 text-lg text-left resize-none leading-normal">
               </textarea>
               </div>

            <!-- BUTTONS -->
            <div class="flex justify-center gap-2">
               <button
                  class="px-4 py-2 bg-gray-300 rounded"
                  onclick={() => (showCreateLobbyModal = false)}
               >
                  Cancel
               </button>

               <button class="px-4 py-2 bg-blue-500 text-white rounded">
                  Create
               </button>
            </div>
         </div>
      </div>
   {/if}
</div>
