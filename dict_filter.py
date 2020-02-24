letter = 'z'

with open('filtered_dict.txt', 'r') as infile:
    with open('letter_dict.txt', 'w') as outfile:
        for line in infile:
            if line[0] == letter:
                outfile.write(line)
