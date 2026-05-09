<script lang="ts">
    type Player = {
        id: string;
        name: string;
        connected?: boolean;
    };

    let rulesText = $state(`ACTION START BUTTON "Start Game":
    EXIT`);

    let userName = $state("username");

    let ruleId = $state("");
    let gameId = $state("");
    let playerId = $state("");
    let lobbyCode = $state("");

    let players = $state<Player[]>([]);

    let output = $state("");

    let socket = $state<WebSocket | null>(null);
</script>

<main
    class="flex items-center justify-center min-h-screen w-screen bg-gray-200"
>
    <!-- Change 'flex' to 'flex-col' to stack vertically -->
    <div class="flex flex-col items-center">
        <!-- Header at the top -->
        <h1 class="text-4xl font-extrabold mb-6 py-8">Lobby</h1>

        <!-- Main Content Area below -->
        <div class="p-10 bg-white shadow-xl rounded-lg border border-gray-200">
            <p class="font-extrabold text-lg mb-2 text-center">Details</p>
            <p>Lobby Code:</p>
            <p>Player Count:</p>
        </div>

        <div class="py-3">
        <button type="button" class="nes-btn is-primary">Start Game</button>


        <!-- TODO: LOOP THROUGH-->
</div>
        <div class="py-3">
            <h1 class="text-2xl font-extrabold py-3 text-center">Players:</h1>
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                
                
                <p
                    class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors"
                >
                <i class="nes-icon coin is-small"></i>
                    HOST: Player 1
                </p>

                <p
                    class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors"
                >
                    Player 2
                </p>

                <p
                    class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors"
                >
                    Player 3
                </p>

                <p
                    class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors"
                >
                    Player 4
                </p>

                <p
                    class="bg-white border border-gray-200 rounded-lg p-4 shadow-sm text-center font-semibold hover:border-blue-500 transition-colors"
                >
                    Player 5
                </p>
            </div>
        </div>
    </div>
</main>
