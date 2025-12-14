import string
from combo_generator import generate_combinations

def main():
    """
    Funzione principale dell'applicazione. Si occupa di:
    1. Richiedere all'utente la lunghezza minima e massima.
    2. Richiedere il set di caratteri da utilizzare.
    3. Generare le combinazioni e salvarle su file.
    """
    print("Password Combination Generator")
    print("-----------------------------")
    
    try:
        min_length = int(input("Inserisci la lunghezza minima delle password: "))
        max_length = int(input("Inserisci la lunghezza massima delle password: "))
    except ValueError:
        print("Per favore inserisci un valore numerico.")
        return

    # Controllo di validità sui valori
    if min_length > max_length:
        print("La lunghezza minima non può essere maggiore della lunghezza massima.")
        return
    
    print("\nSeleziona il tipo di caratteri da usare:")
    print("1. Lettere maiuscole")
    print("2. Lettere minuscole")
    print("3. Lettere maiuscole e minuscole")
    print("4. Numeri e lettere (maiuscole e minuscole)")
    print("5. Solo numeri")
    print("6. Caratteri speciali e lettere (maiuscole e minuscole)")
    print("7. Tutti i caratteri (lettere, numeri, caratteri speciali)")
    
    choice = input("Inserisci il numero corrispondente alla tua scelta: ")
    
    # Definizione dei set di caratteri
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation
    
    if choice == '1':
        character_set = uppercase
    elif choice == '2':
        character_set = lowercase
    elif choice == '3':
        character_set = uppercase + lowercase
    elif choice == '4':
        character_set = uppercase + lowercase + digits
    elif choice == '5':
        character_set = digits
    elif choice == '6':
        character_set = uppercase + lowercase + special_characters
    elif choice == '7':
        character_set = uppercase + lowercase + digits + special_characters
    else:
        print("Scelta non valida.")
        return
    
    # Generazione delle combinazioni
    combinations = generate_combinations(min_length, max_length, character_set)
    
    # Scrittura delle combinazioni su file di output (percorso generico, senza informazioni sensibili)
    output_file = "passlist.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            for combination in combinations:
                file.write(combination + '\n')
        print(f"\nCombinazioni generate e salvate in: {output_file}")
    except OSError as e:
        print(f"Errore durante la scrittura del file: {e}")

if __name__ == "__main__":
    main()
