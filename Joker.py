import random

real_draws = {1 : 0, 2 : 0, 3 : 0, 4 : 0}
points = {1 : 0, 2 : 0, 3 : 0, 4 : 0}

# ფუნქცია მიიღებს მოთამაშეების სახელებს და შეინახავს ლისტში.
def get_player_names():
    player_names = []
    for i in range(4):
        player = input("Enter your name: ")
        player_names.append(player)
    random.shuffle(player_names)
    return player_names

# ფუნქცია აირჩევს პირველ მოთამაშეს და ბოლო მოთამაშეს
def shuffle_players(a: list):  
    last_player = a[-1]
    first_player = a[0]
    new_a = a[1:]
    new_a.append(a[0])
    print(f'{last_player} is dealing cards.')
    return new_a

# ფუნქცია შექმნის კარტის დასტას
def create_deck():
    deck = []
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    values = ['2', '3', '4', '5',  '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    for suit in suits:
        for value in values:
            deck.append(f'{value} of {suit}')
    deck.append('6 of Hearts')
    deck.append('6 of Diamonds')
    deck.append('Joker')
    deck.append('Joker')
    random.shuffle(deck)
    return deck


# დავურიგებთ მოტამასეებს კარტებს და შევინახავთ დიქტში.
def deal_cards(deck : list, player_names : list):
    cards_for_players = {}
    for player_num in range(4):
        cards = []
        for i in range(9):
            cards.append(deck.pop())
        cards_for_players[player_num + 1] = cards
    return cards_for_players


# პირველი მოთამაშე აირჩევს კოზირს
def get_trump_card(cards_for_players : dict, player_names : list):
    cards = cards_for_players.get(1)
    for i in range(3):
        print(f'{i + 1}. {cards[i]}')
    n = int(input(f"{player_names[0]}, choose the trump card(1, 2, or 3): "))
    card = cards[n - 1]
    trump_card = card.split(' of ')[1]
    print(f"{trump_card} is the trump suit.")
    return trump_card


# ყველა მოთამაშეს ეძლევა სიტყვა
def declare_draws(cards_for_players : dict, player_names : list):
    draws = []
    for i in range(4):
        print()
        cards = cards_for_players.get(i + 1)
        for card in cards:
            print(f"{card}")
        if i == 3:  # ბოლო მოთამაშისთვის
            draws_sum = sum(draws)
            if draws_sum <= 9:
                diff = 9 - draws_sum
                n = int(input(f"{player_names[i]}, declare your draws (except {diff}): "))
                while n == diff:
                    n = int(input(f"You cannot enter {diff} draws. Enter again: "))
            else:
                n = int(input(f"{player_names[i]}, declare your draws (from 0 to 9): "))
        else:    
            n = int(input(f"{player_names[i]}, declare your draws (from 0 to 9): "))
        draws.append(n)
    return draws


# მოთამაშეები ითამაშებენ ერთ გათამაშებას
def play_round(player_names : list, cards_for_players : dict, trump_card):
    discarded_cards = {}
    first_card_suit = ''
    for i in range(4):
        cards = cards_for_players.get(i + 1)
        print(f"\n{player_names[i]}, it is your turn.")
    
        cards_for_round = []
        if i > 0:
            has_playable_card = False
            for card in cards:
                if 'Joker' in card or first_card_suit in card or trump_card in card:
                    cards_for_round.append(card)
                    has_playable_card = True
            
            if not has_playable_card:
                cards_for_round = cards
        else:
            cards_for_round = cards


        for n in range(len(cards_for_round)):
            print(f'{n + 1}. {cards_for_round[n]}')
        n = int(input(f"{player_names[i]}, choose a card to lay down (enter the number): ")) - 1

        
        chosen_card = cards_for_round[n]
        cards.remove(chosen_card)
        discarded_cards[i + 1] = chosen_card
        
        
        if i == 0:
            if ' of ' in chosen_card:
                first_card_suit = chosen_card.split(' of ')[1]
            else:
                first_card_suit = chosen_card

        
        cards_for_players[i + 1] = cards

    
    print("\nDiscarded cards:")
    for i in range(4):
        card = discarded_cards[i + 1]
        print(f"{player_names[i]} discarded: {card}")
    return discarded_cards, first_card_suit, cards_for_players


# გავიგოთ, ვინ წაიღო კარტი ამ ხელზე
def get_card_value(card, first_card_suit, trump_card):
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    if card == 'Joker':
        return float('inf')
    value, suit = card.split(' of ')
    value_index = values.index(value)
    if suit == trump_card:
        return value_index + len(values)
    elif suit == first_card_suit:
        return value_index
    return -1

def get_round_winner(discarded_cards : dict, first_card_suit : str, 
                     trump_card : str, player_names : list):
    winning_player = None
    highest_value = -1

    for player, card in discarded_cards.items():
        card_value = get_card_value(card, first_card_suit, trump_card)
        if card_value > highest_value:
            highest_value = card_value
            winning_player = player
        elif card == 'Joker' and highest_value == float('inf'):
            winning_player = player
    real_draws[winning_player] += 1
    print(f"\n{player_names[winning_player - 1]} wins the round and takes the cards!")
    return real_draws


# დავითვალოთ ქულები
def calculate_points(draws : list, real_draws : dict, player_names : list):
    scoring_table = [
    [50, 10, 20, 30, 40, 50, 60, 70, 80, 90],
    [50, 100, 20, 30, 40, 50, 60, 70, 80, 90],
    [50, 10, 150, 30, 40, 50, 60, 70, 80, 90],
    [50, 10, 20, 200, 40, 50, 60, 70, 80, 90],
    [50, 10, 20, 30, 250, 50, 60, 70, 80, 90],
    [50, 10, 20, 30, 40, 300, 60, 70, 80, 90],
    [50, 10, 20, 30, 40, 50, 350, 70, 80, 90],
    [50, 10, 20, 30, 40, 50, 60, 400, 80, 90],
    [50, 10, 20, 30, 40, 50, 60, 70, 450, 90],
    [50, 10, 20, 30, 40, 50, 60, 70, 80, 900]
    ]

    
    for i in range(4):
        player_id = i + 1
        bid = draws[i]
        actual = real_draws[player_id]
        points[player_id] += scoring_table[bid][actual]

    print("\nPoints:")
    for i in range(4):
        player_id = i + 1
        print(f"{player_names[i]}: {points[player_id]} points")
    return points
        
        
        
def main():
    player_names = get_player_names()
    print()
    
   
    consecutive_correct_draws = {1: 0, 2: 0, 3: 0, 4: 0}
    prime_player_rounds = {1: 0, 2: 0, 3: 0, 4: 0}
    
    for n in range(16):  
        player_names = shuffle_players(player_names)
        deck = create_deck()
        cards_for_players = deal_cards(deck, player_names)
        print()
        trump_card = get_trump_card(cards_for_players, player_names)
        print()
        
        draws = declare_draws(cards_for_players, player_names)
        
        for i in range(9):
            discarded_card, first_card_suit, cards_for_players = play_round(player_names, cards_for_players, trump_card)
            real_draws = get_round_winner(discarded_card, first_card_suit, trump_card, player_names)
        
        points = calculate_points(draws, real_draws, player_names)
        
       
        if (n + 1) % 4 == 0:  
            for player_id in range(1, 5):
                if prime_player_rounds[player_id] == 4:
                    max_points = max(points.values())
                    points[player_id] += max_points
                    print(f"{player_names[player_id - 1]} receives a premia of {max_points} points!")
                    prime_player_rounds[player_id] = 0  
        
        
        for player_id in range(1, 5):
            if real_draws[player_id] == draws[player_id - 1]:
                consecutive_correct_draws[player_id] += 1
                if consecutive_correct_draws[player_id] == 4:
                    prime_player_rounds[player_id] = 4
            else:
                consecutive_correct_draws[player_id] = 0
        
       
        print("\nCurrent Points:")
        for i in range(4):
            player_id = i + 1
            print(f"{player_names[i]}: {points[player_id]} points")
        print()

    
   
if __name__ == "__main__":
    main()