import random

# List of colors
colors = ['Red', 'Blue', 'Green', 'Yellow', 'White', 'Pink']
money = 50  # Starting money in pesos
debt = 0  # Initial debt in pesos

def start_game():
    """Simulan ang laro."""
    global money, debt

    print("\nWelcome to the Color Game!")
    print("Pwede kang tumaya sa kahit ilang kulay!")
    print("Kapag ang kulay na tinayaan mo ay lumabas, dodoble ang iyong taya!")
    print("Kapag mali, mababawasan ka ng halaga ng taya para sa kulay na iyon.")
    print("Pwede kang mangutang kung kailangan, pero hanggang ₱100 lang ang utang.")
    print("Simula ka sa ₱50.\n")

    while True:
        if money <= 0 and debt >= 100:
            print("Bankrupt ka na at malaki ang utang mo! Tapos na ang laro!")
            break

        print("\nPera Mo: ₱", money)
        print("Utang Mo: ₱", debt)

        if debt > 0:
            pay_debt_option = input("\nGusto mo bang magbayad ng utang? (yes/no): ").strip().lower()
            if pay_debt_option == "yes":
                pay_debt()

        play_round = input("\nGusto mo bang maglaro ng isang round? (yes/no): ").strip().lower()

        if play_round == "yes":
            draw_colors()
        elif play_round == "no":
            handle_end_game()
            break
        else:
            print("Mali ang input. Pakisulat lang 'yes' o 'no'.")

def draw_colors():
    """Tatlong tamang kulay ang pipiliin, at hahayaan ang manlalaro na maglagay ng taya."""
    global money, debt

    # Pumili ng 3 tamang kulay mula sa listahan
    correct_colors = random.sample(colors, 3)

    print("\nNarito ang mga kulay na pwede mong tayaan:")
    print(", ".join(colors))
    print("\nTatlong kulay ang pipiliin bilang tama.")

    # Kolektahin ang taya ng manlalaro
    bets = {}
    for color in colors:
        while True:
            try:
                bet = int(input(f"Magkano ang taya mo para sa kulay {color}? (₱): "))
                if bet > money:
                    print(f"Wala kang sapat na pera para tumaya ng ₱{bet}.")
                elif bet < 0:
                    print("Hindi pwedeng negatibo ang taya.")
                else:
                    bets[color] = bet
                    money -= bet
                    break
            except ValueError:
                print("Pakilagay ang tamang halaga ng taya bilang numero.")

    print("\nNagtapos na ang pagtaya. Ang iyong mga taya ay:")
    for color, bet in bets.items():
        print(f"{color}: ₱{bet}")

    print("\nTatlong tamang kulay ay:", ", ".join(correct_colors))

    # Tignan kung nanalo o natalo ang bawat kulay
    winnings = 0
    for color, bet in bets.items():
        if color in correct_colors:
            winnings += bet * 2
            print(f"Nanalo ka sa kulay {color}! Napanalunan: ₱{bet * 2}")
        else:
            print(f"Talo ka sa kulay {color}. Nawalan ka ng ₱{bet}.")

    # Update ang pera
    money += winnings
    print("\nBago mong balanse: ₱", money)

    # Pag-check kung kailangan mangutang
    if money <= 0:
        print("Wala ka nang pera.")
        borrow_option = input("Gusto mo bang mangutang ng ₱50? (yes/no): ").strip().lower()
        if borrow_option == "yes" and debt < 100:
            money += 50
            debt += 50
            print("Nangutang ka ng ₱50. Mag-ingat, lumalaki ang utang mo.")
        elif debt >= 100:
            print("Hindi ka na pwedeng mangutang. Naabot mo na ang limit.")
        else:
            print("Tapos na ang laro! Pinili mong hindi mangutang.")

def pay_debt():
    """Pay debt if the player has money."""
    global money, debt

    if debt > 0:
        print("\nUtang Mo: ₱", debt)
        while True:
            try:
                payment = int(input("Magkano ang gusto mong bayaran? (₱): "))
                if payment > money:
                    print(f"Wala kang sapat na pera para magbayad ng ₱{payment}.")
                elif payment < 0:
                    print("Hindi pwedeng negatibo ang bayad.")
                elif payment > debt:
                    print("Hindi pwedeng mas mataas sa utang ang ibabayad mo.")
                else:
                    money -= payment
                    debt -= payment
                    print(f"Nakapagbayad ka ng ₱{payment}. Natitirang Utang: ₱{debt}. Pera Mo: ₱{money}.")
                    break
            except ValueError:
                print("Pakilagay ang tamang halaga bilang numero.")
    else:
        print("Wala kang utang na kailangang bayaran.")

def handle_end_game():
    """Tanungin kung nais bayaran ang utang bago matapos ang laro."""
    global debt

    print("\nSalamat sa paglalaro!")
    if debt > 0:
        while True:
            pay_now = input("May utang ka pa. Gusto mo bang bayaran ito bago umalis? (yes/no): ").strip().lower()
            if pay_now == "yes":
                pay_debt()
                break
            elif pay_now == "no":
                print("Tandaan, may natitira ka pang utang!")
                break
            else:
                print("Pakisagot lamang ng 'yes' o 'no'.")
    print("Final Pera: ₱", money, "| Utang: ₱", debt)

# Simulan ang laro
start_game()
