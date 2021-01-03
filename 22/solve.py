input_file = "input.txt"
with open(input_file) as f:
    player1_data, player2_data = f.read().strip().split("\n\n")

    original_deck1 = [int(line) for line in player1_data.split("\n")[1:]]
    original_deck2 = [int(line) for line in player2_data.split("\n")[1:]]


def compute_score(deck):
    return sum(c * index for index, c in enumerate(reversed(deck), start=1))


deck1 = original_deck1[:]
deck2 = original_deck2[:]
while len(deck1) > 0 and len(deck2) > 0:
    card1, deck1 = deck1[0], deck1[1:]
    card2, deck2 = deck2[0], deck2[1:]

    if card1 > card2:
        deck1 += [card1, card2]
    else:
        deck2 += [card2, card1]


print("Player {} wins non recursive game!".format(1 if len(deck2) == 0 else 2))
print("Score:", compute_score(deck1 if len(deck2) == 0 else deck2))


def play_recursive_combat(deck1, deck2):
    previous_configurations = {1: set(), 2: set()}
    while len(deck1) > 0 and len(deck2) > 0:
        if (tuple(deck1) in previous_configurations[1] or
                tuple(deck2) in previous_configurations[2]):
            return 1, deck1, deck2

        previous_configurations[1].add(tuple(deck1))
        previous_configurations[2].add(tuple(deck2))

        card1, deck1 = deck1[0], deck1[1:]
        card2, deck2 = deck2[0], deck2[1:]

        if len(deck1) < card1 or len(deck2) < card2:
            winner = 1 if card1 > card2 else 2
        else:
            winner, _, __ = play_recursive_combat(deck1[:card1], deck2[:card2])

        if winner == 1:
            deck1 += [card1, card2]
        else:
            deck2 += [card2, card1]

    return (
        1 if len(deck2) == 0 else 2,
        deck1 if len(deck2) == 0 else deck2,
        deck2 if len(deck2) == 0 else deck1,
    )


deck1 = original_deck1[:]
deck2 = original_deck2[:]
winner, winner_deck, loser_deck = play_recursive_combat(deck1, deck2)

if len(loser_deck):
    print("Player 1 wins to avoid infinte loop")
else:
    print("Player {} wins recursive game!".format(winner))
print("Score:", compute_score(winner_deck))
