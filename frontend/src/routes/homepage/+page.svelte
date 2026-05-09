<script lang="ts">
   type Lobby = {
    id: string;
    name: string;
    playerCount: number;
   };

   let lobbies: Lobby[] = [
    { id: '1', name: 'ABC123', playerCount: 2 },
    { id: '2', name: 'XYZ789', playerCount: 3 },
   ];

</script>

<!-- Page Wrapped -->
<div class = "min-h-screen bg-gray-100 flex flex-col">


<!-- Header -->
 <header class="flex items-center justify-center p-4 bg-white shadow ">

    <!-- Title - Cardssembly -->
    <h1 class="text-2xl font-bold text-center"
    >Cardssembly</h1>

     <!-- Create Lobby Button -->
      <button class="absolute right-4 text-3xl font-bold px-3 py-1 bg-blue-500 text-white rounded">
      +
      </button>
    
 </header>

 <main class="flex-1 flex flex-col items-center p-6">

   <!-- Welcome message -->
    <p class="text-lg text-gray-600 mb-6 text-center">
        Welcome to Cardssembly! Join or create a lobby to start playing.
    </p>

    <!-- Section title -->
    <h2 class ="text-xl text-gray-400 text-center font-semibold mb-4">
        Available Lobbies
    </h2>

    <!-- Lobby Table -->
     <div class="flex justify-center w-full">
         <div class="w-full max-w-3xl bg-white shadow rounded overflow-hidden">
      <!-- Table Headers -->
       <div class="grid grid-cols-[3fr_1fr] bg-gray-200 p-3 text-sm font-semibold">
         <div> Lobby Name</div>
         <div class="text-right">Players</div>
       </div>
<!-- ROWS -->
		{#each lobbies as lobby}
			<div class="grid grid-cols-[3fr_1fr] p-3 border-t hover:bg-gray-50 cursor-pointer">

				<!-- LEFT COLUMN (with divider) -->
				<div class="pr-4 border-r border-gray-300 font-bold text-gray-900">
					{lobby.name}
				</div>

				<!-- RIGHT COLUMN -->
				<div class="text-right">
					{lobby.playerCount}
				</div>

			</div>
		{/each}
      </div>
     </div>
 </main>
 </div>