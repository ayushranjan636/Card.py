import random

# Constants for suits and ranks
SUITS = ['S', 'H', 'C', 'D']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Generate a deck of cards
def create_deck():
    return [{'suit': suit, 'rank': rank} for suit in SUITS for rank in RANKS]

# Shuffle the deck
def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

# Deal cards to players
def deal_cards(deck, num_players):
    return [deck[i::num_players] for i in range(num_players)]

# Find the starting player for the first round
def find_starting_player(hands):
    for i, hand in enumerate(hands):
        for card in hand:
            if card['rank'] == 'A' and card['suit'] == 'S':
                return i
    return None  # Should never happen if the deck is correct

# Determine the card value to enforce game rules
def card_value(card):
    return RANKS.index(card['rank'])

def play_round(starting_player, hands, current_suit=None):
    round_cards = []
    for i in range(len(hands)):
        player = (starting_player + i) % len(hands)
        hand = hands[player]

        if current_suit is None or not any(card['suit'] == current_suit for card in hand):
            card_to_play = min(hand, key=card_value)  # Play the smallest card if no matching suit
            current_suit = card_to_play['suit']
        else:
            valid_cards = [card for card in hand if card['suit'] == current_suit]
            if valid_cards:
                card_to_play = min(valid_cards, key=card_value)
            else:
                card_to_play = max(hand, key=card_value)  # Player must play the highest card in another suit

        hand.remove(card_to_play)
        round_cards.append((card_to_play, player))

    # Filter round_cards for those that match the current_suit, handle no matches
    filtered_round_cards = [card for card, player in round_cards if card['suit'] == current_suit]
    if not filtered_round_cards:  # if no cards match the current_suit, revert to original cards played
        filtered_round_cards = round_cards

    winning_card = max(filtered_round_cards, key=card_value)
    winner = next(player for card, player in round_cards if card == winning_card)
    return winner, current_suit, round_cards

def simulate_game(num_players):
    deck = create_deck()
    deck = shuffle_deck(deck)
    hands = deal_cards(deck, num_players)
    starting_player = find_starting_player(hands)
    current_suit = None

    round_count = 0  # to track rounds for clarity in print statements

    # Continue playing until players have cards
    while any(len(hand) > 0 for hand in hands):
        round_count += 1
        print(f"\nRound {round_count}")
        starting_player, current_suit, played_cards = play_round(starting_player, hands, current_suit)
        print(f"Round played: {[(card['suit'] + card['rank'], player) for card, player in played_cards]}. Starting next round: {starting_player}.")

        # Diagnostic print to see how many cards each player has after each round
        for idx, hand in enumerate(hands):
            print(f"Player {idx} has {len(hand)} cards.")

    # Check if all players have zero cards
    if all(len(hand) == 0 for hand in hands):
        print("\nGame over! All players have exhausted their cards simultaneously.")
    else:
        # Find the player with cards left and declare them as the loser
        for i, hand in enumerate(hands):
            if len(hand) > 0:
                print(f"\nGame over! The last player with cards is player {i}, and they are declared the loser.")
                break

# Start the game with 4 players
simulate_game(4)