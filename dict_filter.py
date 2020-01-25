with open('words_alpha.txt', 'r') as infile:
    with open('filtered_dict.txt', 'w') as outfile:
        for line in infile:
            word = line[0:-1]
            unique_letters = []
            for letter in word:
                if letter not in unique_letters:
                    unique_letters.append(letter)
            if len(word) >= 5 and len(unique_letters) <= 7:
                outfile.write(line)
