import json

from backend.engine.classes.states import PlayerState
from backend.engine.engine import GameEngine
from backend.routers.models.ClientSide import ClientSide, ClientSideBuilder

FACE_DOWN_CARD = {"suit": "", "value": "UNKNOWN"}


class ClientSideGenerator:
    @staticmethod
    def generate_client_sides(engine: GameEngine) -> list[ClientSide]:
        return [
            ClientSideGenerator.build_client_side(pIdx, engine)
            for pIdx in range(len(engine.playerStates))
        ]

    @staticmethod
    def build_client_side(client_idx: int, engine: GameEngine) -> ClientSide:
        client_side_builder: ClientSideBuilder = ClientSideBuilder()
        client_side_builder.set_actions(engine.playerStates[client_idx].actions)

        for p_idx, p_state in enumerate(engine.playerStates):
            if client_idx == p_idx:  # this is client's hand
                client_side_builder.set_hand(p_state.hand)
                continue

            client_side_builder.create_new_opp_hand()

            for card_idx, revealed in enumerate(
                engine.gameState.global_revealed[p_idx]
            ):
                card = (
                    engine.playerStates[p_idx].hand[card_idx]
                    if revealed
                    else FACE_DOWN_CARD
                )
                client_side_builder.append_opp_card(card)

        return client_side_builder.build()


if __name__ == "__main__":

    class MockEngine:
        def __init__(self):
            self.playerStates = []
            self.gameState = type("obj", (object,), {"global_revealed": []})

    engine = MockEngine()

    # 2. Create Player 1 (The perspective we will check)
    p1 = PlayerState(uuid="user_88")
    p1.hand = [{"suit": "Hearts", "value": "A"}, {"suit": "Spades", "value": "10"}]
    p1.actions = ["ATTACK", "END_TURN"]

    # 3. Create Player 2 (The Opponent)
    p2 = PlayerState(uuid="user_99")
    p2.hand = [{"suit": "Clubs", "value": "2"}, {"suit": "Diamonds", "value": "K"}]
    p2.actions = ["WAIT"]

    engine.playerStates = [p1, p2]

    # 4. Define Visibility (Fog of War)
    # Player 1's cards: [Hidden, Hidden] (to others)
    # Player 2's cards: [Revealed, Hidden] (to others)
    engine.gameState.global_revealed = [[False, False], [True, False]]

    # 5. Run Generator
    print("--- Generating Client Sides ---")
    results = ClientSideGenerator.generate_client_sides(engine)

    # 6. Verify Player 1's Perspective
    # They should see their own full hand, but only 1 of Player 2's cards.
    p1_view = results[0]

    output = {
        "player_1_own_hand": p1_view.hand,
        "player_1_sees_actions": p1_view.actions,
        "player_1_sees_opponents": p1_view.opponent_hand,
    }

    print(json.dumps(output, indent=4))

    # Simple Assertions to verify logic
    assert len(p1_view.hand) == 2, "Should see both own cards"
    assert p1_view.opponent_hand[0][0]["value"] == "2", "Should see revealed card"
    assert (
        p1_view.opponent_hand[0][1]["value"] == "UNKNOWN"
    ), "Should NOT see hidden card"
    print("\n✅ Test Passed: Fog of War logic is working!")
