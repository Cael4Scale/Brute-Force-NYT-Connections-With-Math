import numpy as np

aPool = ['00001111', '00010111', '00011011', '00011101', '00011110', '00100111', '00101011', '00101101', '00101110', '00110011', '00110101', '00110110', '00111001', '00111010', '00111100', '01000111', '01001011', '01001101', '01001110', '01010011', '01010101', '01010110', '01011001', '01011010', '01011100', '01100011', '01100101', '01100110', '01101001', '01101010', '01101100', '01110001', '01110010', '01110100', '01111000']

FirstTry = 0
SecondTry = 0
ThirdTry = 0
FourthTry = 0
Fail = 0

def how_many_away(answer, guess):
    return bin(int(answer, 2)^int(guess, 2)).count('1') / 2

for Answer in aPool:
    Guess1 = '00001111'

    if Guess1 == Answer:
        FirstTry += 1
    elif how_many_away(Answer, Guess1) == 2:
        Guess2 = '00110011'

        if Guess2 == Answer:
            SecondTry += 1
        elif how_many_away(Answer, Guess2) == 2:
            Guess3 = '01010101'

            if Guess3 == Answer:
                ThirdTry += 1
            elif how_many_away(Answer, Guess3) == 2:
                Guess4 = '00111100'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
            else:
                Guess4 = '01010110'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
        else:
            Guess3 = '00110101'

            if Guess3 == Answer:
                ThirdTry += 1
            elif how_many_away(Answer, Guess3) == 2:
                Guess4 = '01010011'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
            else:
                Guess4 = '00110110'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
    else:
        Guess2 = '00010111'

        if Guess2 == Answer:
            SecondTry += 1
        elif how_many_away(Answer, Guess2) == 2:
            Guess3 = '00101011'

            if Guess3 == Answer:
                ThirdTry += 1
            elif how_many_away(Answer, Guess3) == 2:
                Guess4 = '01001101'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
            else:
                Guess4 = '00101101'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
        else:
            Guess3 = '00011011'

            if Guess3 == Answer:
                ThirdTry += 1
            elif how_many_away(Answer, Guess3) == 2:
                Guess4 = '00100111'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1
            else:
                Guess4 = '00011101'

                if Guess4 == Answer:
                    FourthTry += 1
                else:
                    Fail += 1

print(FirstTry)
print(SecondTry)
print(ThirdTry)
print(FourthTry)
print(Fail)
SuccessChance = (FirstTry + SecondTry + ThirdTry + FourthTry)/(FirstTry + SecondTry + ThirdTry + FourthTry + Fail)*100
print(f"Chance of Success: '{SuccessChance}'%")
