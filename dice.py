import random
import time

STARTING_BALANCE = 100
DICE_SIDES = 6


def select_number(sides=DICE_SIDES):
    return random.randint(1, sides)


def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("Por favor ingresa un número válido.")
            continue

        if min_value is not None and value < min_value:
            print(f"El valor debe ser al menos {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"El valor debe ser como máximo {max_value}.")
            continue

        return value


def choose_game_mode():
    print("\nSelecciona un modo de juego:")
    print("1. Comparar dados (mayor gana)")
    print("2. Par o impar")
    print("3. Adivinar número exacto")
    return get_int_input("Ingresa 1, 2 o 3: ", 1, 3)


def play_compare_mode(bet):
    print("\nEl oponente lanza su dado...")
    time.sleep(random.uniform(0.8, 1.5))
    opponent = select_number()
    print("Resultado del oponente:", opponent)

    print("\nAhora es tu turno...")
    time.sleep(random.uniform(0.8, 1.5))
    player = select_number()
    print("Tu resultado es:", player)

    if player > opponent:
        print("¡Ganaste! Obtienes un bono extra.")
        return bet * opponent
    elif player < opponent:
        print("Perdiste. Mejor suerte la próxima vez.")
        return -bet
    else:
        print("Empate. No pierdes ni ganas dinero.")
        return 0


def play_even_odd_mode(bet):
    choice = input("¿Apuestas a 'par' o 'impar'? ").strip().lower()
    while choice not in ("par", "impar"):
        choice = input("Ingresa 'par' o 'impar': ").strip().lower()

    print("\nLanzando tu dado...")
    time.sleep(random.uniform(0.8, 1.5))
    player = select_number()
    print("Tu resultado es:", player)

    result = "par" if player % 2 == 0 else "impar"
    if result == choice:
        print("¡Acertaste! Ganas el doble de tu apuesta.")
        return bet * 2
    else:
        print("No acertaste. Pierdes tu apuesta.")
        return -bet


def play_exact_number_mode(bet):
    guess = get_int_input(f"Adivina el número entre 1 y {DICE_SIDES}: ", 1, DICE_SIDES)
    print("\nLanzando el dado...")
    time.sleep(random.uniform(0.8, 1.5))
    player = select_number()
    print("El resultado es:", player)

    if guess == player:
        print("¡Increíble! Adivinaste el número exacto.")
        return bet * 5
    else:
        print("No fue correcto. Pierdes tu apuesta.")
        return -bet


def print_statistics(rounds, wins, losses, ties, balance):
    print("\n----- Estadísticas de la sesión -----")
    print("Rondas jugadas:", rounds)
    print("Victorias:", wins)
    print("Derrotas:", losses)
    print("Empates:", ties)
    print("Balance final:", balance, "unidades")
    print("------------------------------------")


def main():
    balance = STARTING_BALANCE
    rounds = wins = losses = ties = 0

    print("Bienvenido al simulador de dados!")
    time.sleep(1)

    while balance > 0:
        print(f"\nTu saldo actual es: {balance} unidades.")
        mode = choose_game_mode()
        bet = get_int_input("¿Cuánto deseas apostar? ", 1, balance)

        if mode == 1:
            result = play_compare_mode(bet)
        elif mode == 2:
            result = play_even_odd_mode(bet)
        else:
            result = play_exact_number_mode(bet)

        if result > 0:
            wins += 1
        elif result < 0:
            losses += 1
        else:
            ties += 1

        balance += result
        rounds += 1

        print(f"\nCambio en tu saldo: {result} unidades.")
        print(f"Saldo actual: {balance} unidades.")

        if balance <= 0:
            print("\nTe quedaste sin dinero. Fin del juego.")
            break

        play_again = input("\n¿Quieres jugar otra ronda? (si/no) ").strip().lower()
        if play_again not in ("si", "sí", "s"):
            break

    print_statistics(rounds, wins, losses, ties, balance)
    print("\nGracias por jugar. ¡Hasta pronto!")


if __name__ == "__main__":
    main()
