import itertools
import random
import json

    
def play_game():
    def choose_letters(_letters_correct, _letters_wrong, letters_chosen=[], letter_count=1):
        nonlocal letters_english
        if letter_count == 0:
            return letters_chosen
        letter_count = letter_count - 1
        while True:
            letter = input('\nPlease choose a letter: ').upper()    
            if len(letter) > 1:
                print('\nYou can only select one letter at a time.')
                continue
            if letter not in letters_english:
                print('\nPlease only choose one of the following letters, or their lowercase equivalents.\n{}'.format(letters_english))
                continue
            if letter in [*_letters_correct, *_letters_wrong, *letters_chosen]:
                print('\nYou have already chosen this letter. Please select another.')
                continue
            break
        print(letter)
        letters_chosen.append(letter)
        # place letters if it is the right option
        print(f'{letters_chosenzs
        }')
        exit()
        return choose_letters(_letters_correct, _letters_wrong, letters_chosen, letter_count)
    
    def place_letters(letters, _word, _letters_correct, _letters_wrong):
        wrong_current_count = 0
        print(letters)
        for let in letters:
            if let in _word:
                _letters_correct.append(let)                    
            else:
                if not power_up:
                    wrong_current_count = wrong_current_count + 1
                _letters_wrong.append(let)
        return _letters_correct, _letters_wrong, wrong_current_count
    
    def load_words():
        with open('words.json', 'r', encoding='utf-8') as word_file:
            valid_words = json.load(word_file)
            valid_words = [word for word in valid_words['data'] if len(word) > 3 and len(word) < 10]
        return valid_words
        
    def clear_display():
        print('\033c')
    
    def display(_word, _letters_correct, _letters_wrong, _wrong_current, _wrong_max, _total_current, _total_max):
        nonlocal message
        clear_display()
        _word = [x if x in _letters_correct else '_' for x in _word]
        _word = ' '.join(_word)
        print('{}\n\nWrong letters: {}\nCorrect letters: {}\n\n{} out of {} wrong tries.\n{} out of {} total tries.'.format(_word, _letters_wrong, _letters_correct, _wrong_current, _wrong_max, _total_current, _total_max))
        if message:
            print('MESSAGE: {}'.format(message))
            message = ''
    
    words = load_words()
    letters_english = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    
    def choose_letters_reveal_afterwards(_letters_correct, _letters_wrong, choose=5, cost=3):
        letters = choose_letters(_letters_correct, _letters_wrong, [], choose)
        return letters
        
    def choose_letters_reveal_afterwards_counting_cost(_letters_correct, _letters_wrong, choose=5, max_cost=4): # todo
        letters = []
        for i in range(choose):
            letter = choose_letters(_letters_correct, _letters_wrong, letters)
            letters.append(letter)
        return letters
    
    
    wrong_max = 7
    total_max = 99
    rounds_played = 0
    rounds_won = 0
    message = ''
    
    def play_round(choose_word=False):
        nonlocal words, letters_english, wrong_max, total_max, rounds_won, rounds_played, message
        if choose_word:
            word = input('Choose word for other player(s) to guess: ').upper()
            if not set(word).issubset(letters_english):
                print('\nPlease only choose one of the following letters, or their lowercase equivalents.\n{}'.format(letters_english))
                play_round(choose_word=True)
                return
        else:            
            word = random.choice(words).upper()
        total_current = 0
        wrong_current = 0
        letters_correct = []
        letters_wrong = []
        while wrong_current < wrong_max:
            display(word, letters_correct, letters_wrong, wrong_current, wrong_max, total_current, total_max)
            power_up = input('Would you like to use a power-up? yes: ')
            if power_up == 'yes':
                power_up = input('Which power-up would you like to use?: ')
                if power_up == '1':
                    if wrong_current + 3 >= wrong_max:
                        message = 'You may not choose this power-up as you don\'t have enough wrong tries remaining.'
                        continue
                    letters_input = choose_letters_reveal_afterwards(letters_correct, letters_wrong, choose=5, cost=3)
                    wrong_current = wrong_current + 3
                else:
                    message = 'Please choose a valid power-up.'
                    continue
            else:
                power_up = ''
                letters_input = [choose_letters(letters_correct, letters_wrong)]
            total_current = total_current + len(letters_input)
            letters_correct, letters_wrong = place_letters(letters_input, word, letters_correct, letters_wrong)                
            if set(word).issubset(letters_correct):
                display(word, letters_correct, letters_wrong, wrong_current, wrong_max, total_current, total_max)
                print('\nCongrats! You win!')
                rounds_won = rounds_won + 1
                break
        if not set(word).issubset(letters_correct):
            print('\nSorry! You\'ve lost! The word was {}'.format(word))
        rounds_played = rounds_played + 1
    
    while True:
        print('\nYou\'ve won {} out of {} games played!'.format(rounds_won, rounds_played))
        while True:
            play_again = input('\nWould you like to play? y/n/2: ')
            if play_again.lower() == 'y':
                play_round()
                break
            elif play_again.lower() == 'n':
                print('\nOkay! Thank you for playing!')
                exit()
            elif play_again == '2':
                play_round(choose_word=True)
                break
            else:
                print('\nPlease only enter \'y\' or \'n\'.')

play_game()

