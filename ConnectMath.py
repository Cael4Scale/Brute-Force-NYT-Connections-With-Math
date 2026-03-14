# Source - https://stackoverflow.com/a
# Posted by hughdbrown, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-24, License - CC BY-SA 3.0

#from itertools import permutations

#def unique_perms(series):
#    return {"".join(p) for p in permutations(series)}

#print(sorted(unique_perms('11110000')))

#print(bin(y)[2:].zfill(len(h)))
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

## All 35 permuations of 8 choose 4 options. This would be 70, but since every permutation has 2 answers, I can divide by two. I did this by removing all permutations starting with 1 in the first digit
a = ['00001111', '00010111', '00011011', '00011101', '00011110', '00100111', '00101011', '00101101', '00101110', '00110011', '00110101', '00110110', '00111001', '00111010', '00111100', '01000111', '01001011', '01001101', '01001110', '01010011', '01010101', '01010110', '01011001', '01011010', '01011100', '01100011', '01100101', '01100110', '01101001', '01101010', '01101100', '01110001', '01110010', '01110100', '01111000']

guesses = ['00001111', '00011110', '00011101']  # This was to test that the answer_bin function would work
#print("Guesses: ")
#print(guesses)


## Given a certain amount of guesses, calculate which options are 1 or 2 away from the correct answer
def answer_bin(guesses, options, record, bin_amount):
    # Guesses: the 3 guesses allocated (can handle any number of guesses actually)
    # Options: Pool of permutations to compare the guesses to
    # Record: Records which guesses were 1 away or 2 away and combines them into a label for each bin
    # Bin_amount: Array that displays both an ID for each bin and how many objects are in that bin
    away1 = []
    away2 = []
    away0 = []

    # Double check all the guesses answered are valid guesses
    #for g in guesses:
    #    if ''.join(sorted(g)) != '00001111':
    #        print(g)
    #        print("invalid guess")
    #        return
    #print("Guess it must have worked")

    for h in options:
        y = int(h, 2)^int(guesses[0],2) # XOR the Guess with the option. This reveals which digits are different and which are the same
        if h == guesses[0]:  # But first we gotta check if the guess is the exact the same as the option that is being checked. That means its a correct answer
            away0.append(h)
        elif ''.join(sorted(bin(y)[2:].zfill(len(h)))) != '00001111': # Checks if the option is NOT two away from the guess
            away1.append(h)
        else:                                                         # If it aint two away and it aint 0 away, its gotta be one away
            away2.append(h)
    if len(guesses) > 0:                    # If there are any guesses left, remove the first one from the list so this recursively checks each guess
        new_guesses = guesses[1:]
    else:
        new_guesses = []
    
    if len(new_guesses) == 0:               # If we ran out of guesses, perform some last functions before exiting this part of the recursion
        #print(record + '1')
        #print(away1)
        bin_amount.append(record + '1')     # jot down the final 1-away record for the last recursion, indicating the official ID for the bin
        bin_amount.append(len(away1))       # jot down the correspondind amount of things in that bin

        #print(record + '2')
        #print(away2)
        bin_amount.append(record + '2')     # jot down the final 1-away record for the last recursion, indicating the official ID for the bin
        bin_amount.append(len(away2))       # jot down the correspondind amount of things in that bin
    else:
        answer_bin(new_guesses, away1, record + '1', bin_amount)        # If you still have guesses to make, recurse with the now smaller pool of answers per bin
        answer_bin(new_guesses, away2, record + '2', bin_amount)        # Pass along the record of each bin label. This is designed so it can be infinitely recursive for any number of guesses and any size of options

    return(bin_amount)                      # Exit the loop, also pass along the array that indicates how many items are in each bin

bin_amount = (answer_bin(guesses, a, '', []))
G = []
X = []
Y = []
Z = []

print(answer_bin(guesses, a, '', []))

G_setFilter = []


## Go through every possible combination of guesses
## No repeats or duplicates in the combination

# Go through the index of every guess, and pair it with a range of indexes for every other guess

for x in range(len(a)):
    for y in range(x+1, len(a)):
        for z in range(y+1, len(a)):
            #print(a[x], a[y], a[z])
            #print(x, y, z)
            
            bin_amount = (answer_bin([a[x], a[y], a[z]], a, '', []))            # Return the amount inside each bin for calcs later
            #bin_amount = []
            E = 0                                               # E represents the average options left after a given distribution of possible answers in the bins
            for i in range(len(bin_amount)):
                if i%2 == 1:                                    # Skip every other item in this array because that corresponds to the name of the bin
                    E = E + (pow(bin_amount[i], 2))/32          # Weighted average worked out on paper to the Sum of (n_i)^2 / N
            #E = E + 3/35 # Technically it would be like 3.09/35 due to the 1/35 + 1/34 + 1/33
            #print(E)
            Vfilter = 3.91429
            if round(E, 5) != 0:
                G.append(round(E, 5))

                X.append(x)                         # Add the index of the first guess to an array so i can plot it later
                Y.append(y)                         # Add the index of the first guess to an array so i can plot it later
                Z.append(z)                         # Add the index of the first guess to an array so i can plot it later
                #print(a[x], a[y], a[z])
                #print(bin_amount)
            G_setFilter.append(round(E, 5))

G_setFilter = set(G_setFilter)         #Determines how many unique strategies scores there are. They are listed below
#print(G_setFilter)                     #{3.74286, 3.91429, 4.31429, 7.4}

## Generate the 3D plot of all the points
#print(set(G))

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')

ax.scatter3D(X, Y, Z, c = G, cmap='viridis', marker='o')

ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')
ax.set_zlabel('Z Axis')
ax.set_title('Best Connections Combo')
#print(X, Y, Z, G)
#plt.show()