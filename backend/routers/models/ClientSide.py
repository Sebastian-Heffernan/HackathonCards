class ClientSide:
    def __init__(self, actions, hand, opp_hand):
        self.actions: list[str] = actions
        self.hand: list[dict] = hand
        self.opponent_hand: list[list[dict]] = opp_hand


class ClientSideBuilder:
    def __init__(self):
        self.actions: list[str] = []
        self.hand: list[dict] = []
        self.opponent_hand: list[dict] = []

    def set_actions(self, actions: list[str]):
        self.actions = actions

    def create_new_opp_hand(self):
        self.opponent_hand.append([])

    def append_opp_card(self, card: dict):
        self.opponent_hand[-1].append(card)

    def set_hand(self, hand: list[dict]):
        self.hand = hand

    def set_opponent_hand(self, opp_hand: list[dict]):
        self.opponent_hand = opp_hand

    def build(self) -> ClientSide:
        return ClientSide(self.actions, self.hand, self.opponent_hand)
