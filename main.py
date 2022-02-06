# !/usr/bin/env python

import re
import art
import json
import datetime

CMD_LIST = """
+----------------------------------------------+
|                 All Commands                 |
+--------------+-------------------------------+
|  Exit script | 'exit', 'stop', 'e', 's'      |
+--------------+-------------------------------+
| Command List | 'cmds', 'cl', 'c'             |
+--------------+-------------------------------+
| Today's word | 'today', 'wotd', 'tw', 'w'    |
+--------------+-------------------------------+
| Word Guesser | 'guesser', 'guess', 'wg', 'g' |
+--------------+-------------------------------+"""

def todays_word():
    print("The list of 'today's word' is according to Wordle's own source code (https://www.powerlanguage.co.uk/wordle/main.e65ce0a5.js). This program was last updated on February 6th, 2022. Far past this date may result in innacurate word predictions, as the list may have changed.")
    first_day = datetime.date(2021, 6, 19)
    end_day = datetime.date(2027, 10, 21)
    today = datetime.date.today()
    if today<first_day:
        print(f"It seems like the date that your computer has for today ({today.strftime('%d/%m/%Y')}) is earlier than the Wordle's list can go. There is no Wordle for 'today'!")
    if today>end_day:
        print(f"It seems like the date that your computer has for today ({today.strftime('%d/%m/%Y')}) is farther than the Wordle's list goes. There is no Wordle for 'today'!")
    else:
        wordle_num = (today - first_day).days
        with open('answers.json', 'r') as answers_file:
            answers = json.load(answers_file)
        print(f"Today's word is '{answers[wordle_num]}'")

def word_guesser():
    print("Retrieving all possible words...")
    with open('answers.json', 'r') as answers_file:
        answers = json.load(answers_file)
    with open('words.json', 'r') as words_file:
        words = json.load(words_file)
    for answer in answers:
        words.append(answer)
    print("Words retrieved.")
    print("""
W E L C O M E    T O    T H E    W O R D    G U E S S E R

There will be multiple fields that appear in the following order:
Anywhere, first, second, third, fourth, fifth
To enter letters just have them all in a row no commas or spaces. When you have nothing to put, just press enter to skip filling the field. 
An example for the word 'proxy' where you know where 'r' and 'x' go, and you know that 'o' and 'y' are in the word, but you don't know that 'p' is in the word.
Also, you've had 'y' yellow in 3 and 'o' and 'y' in 4, you can add that as well.
Here is how you would fill out the fields:

Letters you know are in the word:
Anywhere: oy
   First: 
  Second: r
   Third: 
  Fourth: x
   Fifth: 

Letters you know are not in the word:
Not anywhere: ubeqz
   Not first: 
  Not second: 
   Not third: y
  Not fourth: oy
   Not fifth: 

All the words that matched with your arguments are: 
 - orixa
 - proxy
""")
    print("Word guesser initiated.")
    while True:
        print("\nLetters you know are in the word:")
        anywhere = input("Anywhere: ").lower().replace(' ', '')
        first = input("   First: ").lower().replace(' ', '')
        second = input("  Second: ").lower().replace(' ', '')
        third = input("   Third: ").lower().replace(' ', '')
        fourth = input("  Fourth: ").lower().replace(' ', '')
        fifth = input("   Fifth: ").lower().replace(' ', '')
        
        if 0>len(anywhere+first+second+third+fourth+fifth)>5:
            print("\nThe total amount of letters you provided is either greater than 5 or lesser than 0, so no word could be found.\n")
            stop = input("(y/n) Would you like to exit the Word Guesser? ").lower()
            if stop in ('yes', 'y'):
                break
            else:
                continue
        
        print("\nLetters you know are not in the word:")
        not_anywhere = input("Not anywhere: ").lower().replace(' ', '')
        not_first = input("   Not first: ").lower().replace(' ', '')
        not_second = input("  Not second: ").lower().replace(' ', '')
        not_third = input("   Not third: ").lower().replace(' ', '')
        not_fourth = input("  Not fourth: ").lower().replace(' ', '')
        not_fifth = input("   Not fifth: ").lower().replace(' ', '')

        match = r""
        for letter in ((first, not_first), (second, not_second), (third, not_third), (fourth, not_fourth), (fifth, not_fifth)):
            if len(letter[0])!=1:
                match+=f"[^{not_anywhere+letter[1] if len(not_anywhere+letter[1])>0 else ' '}]"
            else:
                match+=f"{letter[0]}"
        
        matched_words = []
        for word in words:
            if re.match(match, word.lower()):
                matched_words.append(word)
        matched_words = "\n - "+"\n - ".join(matched_words) if len(matched_words)>0 else ' - No words were matched'
        
        print(f"\nAll the words that matched with your arguments are: {matched_words}\n")
        stop = input("(y/n) Would you like to exit the Word Guesser? ").lower()
        if stop in ('yes', 'y'):
            break

art.tprint("Wordle\nHelper", font="block", chr_ignore=True)
print(CMD_LIST)

while True:
    print()
    cmd = input("Command: ").lower()
    if cmd in ('exit', 'stop', 'e', 's'):
        print("Exiting...")
        break
    elif cmd in ('cmds', 'cl', 'c'):
        print(CMD_LIST)
    elif cmd in ('today', 'wotd', 'tw', 'w'):
        todays_word()
    elif cmd in ('guesser', 'guess', 'wg', 'g'):
        word_guesser()
    else:
        print("Command not recognized. Type 'cmds' for a list of possible commands.", end='\n\n')

print("\nClosed program.")