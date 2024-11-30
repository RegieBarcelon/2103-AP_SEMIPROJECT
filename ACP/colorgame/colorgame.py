import random

# List of colors
colors = ['Red', 'Blue', 'Green', 'Yellow', 'White', 'Pink']
money = 50  # Starting money in pesos
debt = 0  # Initial debt in pesos

def start_game():
    """Simulan ang laro."""
    global money, debt

    print("\nWelcome to the Color Game!")
    print("Hulaan ang tamang kulay para madoble ang iyong taya!")
    print("Kapag mali, mababawasan ka ng halaga ng iyong taya.")
    print("Pwede kang mangutang kung kailangan, pero hanggang ₱100 lang ang utang.")
    print("Simula ka sa ₱50.\n")

    while True:
        if money <= 0 and debt >= 100:
            print("Bankrupt ka na at malaki ang utang mo! Tapos na ang laro!")
            break

        print("\nPera Mo: ₱", money)
        print("Utang Mo: ₱", debt)
        play_round = input("\nGusto mo bang maglaro ng isang round? (yes/no): ").strip().lower()

        if play_round == "yes":
            draw_colors()
        elif play_round == "no":
            print("\nSalamat sa paglalaro! Final Pera: ₱", money, "| Utang: ₱", debt)
            break
        else:
            print("Mali ang input. Pakisulat lang 'yes' o 'no'.")

def draw_colors():
    """Tatlong tamang kulay ang pipiliin, at hahayaan ang manlalaro na hulaan."""
    global money, debt

    # Pumili ng 3 tamang kulay mula sa listahan
    correct_colors = random.sample(colors, 3)

    print("\nNarito ang mga kulay na pwede mong tayaan:")
    print(", ".join(colors))

    # Pagkuha ng taya mula sa user
    while True:
        try:
            bet = int(input("Magkano ang iyong taya? (₱): "))
            if bet > money:
                print("Wala kang sapat na pera para tumaya ng ₱", bet)
            elif bet <= 0:
                print("Ang taya ay dapat mas mataas sa ₱0.")
            else:
                break
        except ValueError:
            print("Pakilagay ang tamang halaga ng taya bilang numero.")

    # Hula ng user
    guess = input("Hulaan ang tamang kulay: ").strip().capitalize()

    if guess not in colors:
        print("Maling input. Pakipili mula sa listahan ng kulay.")
        return

    if guess in correct_colors:
        money += bet  # Nadagdag ang napanalunan
        print(f"Tama! Ang iyong hula ({guess}) ay isa sa tamang kulay: {', '.join(correct_colors)}.")
        print(f"Napanalunan mo ang iyong taya! Bago mong balanse: ₱{money}.")
    else:
        money -= bet  # Nabawas ang taya
        print(f"Mali! Ang tamang mga kulay ay: {', '.join(correct_colors)}.")
        print(f"Nabawasan ka ng iyong taya. Bago mong balanse: ₱{money}.")

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

# Simulan ang laro
start_game()