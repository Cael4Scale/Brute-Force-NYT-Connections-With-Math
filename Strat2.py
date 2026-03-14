import numpy as np

aPool = ['00001111', '00010111', '00011011', '00011101', '00011110', '00100111', '00101011', '00101101', '00101110', '00110011', '00110101', '00110110', '00111001', '00111010', '00111100', '01000111', '01001011', '01001101', '01001110', '01010011', '01010101', '01010110', '01011001', '01011010', '01011100', '01100011', '01100101', '01100110', '01101001', '01101010', '01101100', '01110001', '01110010', '01110100', '01111000']

FirstTry = 0
SecondTry = 0
ThirdTry = 0
FourthTry = 0
Fail = 0

for Answer in aPool:
    for Guess1 in aPool:
        twoAwayFromFirstGuess = False
        if Guess1 == Answer:
            FirstTry += 1
        else:
            compare = int(Answer, 2)^int(Guess1,2)
            if ''.join(sorted(bin(compare)[2:].zfill(len(Answer)))) == '00001111':
                twoAwayFromFirstGuess = True

            for Guess2 in aPool:
                twoAwayFromSecondGuess = False
                if Guess2 == Answer:
                    SecondTry += 1
                elif Guess2 != Guess1:
                    compare = int(Guess1, 2)^int(Guess2,2)
                    if (twoAwayFromFirstGuess == (''.join(sorted(bin(compare)[2:].zfill(len(Answer)))) == '00001111')):
                        compare = int(Answer, 2)^int(Guess2,2)
                        if ''.join(sorted(bin(compare)[2:].zfill(len(Answer)))) == '00001111':
                            twoAwayFromSecondGuess = True

                        for Guess3 in aPool:
                            twoAwayFromThirdGuess = False
                            if Guess3 == Answer:
                                ThirdTry += 1
                            elif (Guess3 != Guess2) and (Guess3 != Guess1):
                                Cell_ID = [Guess1[0]+ Guess2[0]+ Guess3[0], Guess1[1]+ Guess2[1]+ Guess3[1], Guess1[2]+ Guess2[2]+ Guess3[2], Guess1[3]+ Guess2[3]+ Guess3[3], Guess1[4]+ Guess2[4]+ Guess3[4], Guess1[5]+ Guess2[5]+ Guess3[5], Guess1[6]+ Guess2[6]+ Guess3[6], Guess1[7]+ Guess2[7]+ Guess3[7]]
                                if len(set(Cell_ID)) > 4:
                                    compare1 = int(Guess1, 2)^int(Guess3,2)
                                    compare2 = int(Guess2, 2)^int(Guess3,2)
                                    if ((twoAwayFromFirstGuess == (''.join(sorted(bin(compare1)[2:].zfill(len(Answer)))) == '00001111')) and (twoAwayFromSecondGuess == (''.join(sorted(bin(compare2)[2:].zfill(len(Answer)))) == '00001111'))):
                                        compare = int(Answer, 2)^int(Guess3,2)
                                        if ''.join(sorted(bin(compare)[2:].zfill(len(Answer)))) == '00001111':
                                            twoAwayFromThirdGuess = True

                                        for Guess4 in aPool:
                                            if Guess4 == Answer:
                                                FourthTry += 1
                                            elif (Guess4 != Guess3) and (Guess4 != Guess2) and (Guess4 != Guess1):
                                                compare1 = int(Guess1, 2)^int(Guess4,2)
                                                compare2 = int(Guess2, 2)^int(Guess4,2)
                                                compare3 = int(Guess3, 2)^int(Guess4,2)
                                                if ((twoAwayFromFirstGuess == (''.join(sorted(bin(compare1)[2:].zfill(len(Answer)))) == '00001111')) and (twoAwayFromSecondGuess == (''.join(sorted(bin(compare2)[2:].zfill(len(Answer)))) == '00001111')) and (twoAwayFromThirdGuess == (''.join(sorted(bin(compare3)[2:].zfill(len(Answer)))) == '00001111'))):
                                                    Fail += 1
                                                    print(f"'{aPool.index(Answer)}''{aPool.index(Guess1)}''{aPool.index(Guess2)}''{aPool.index(Guess3)}''{aPool.index(Guess4)}'")
print(FirstTry)
print(SecondTry)
print(ThirdTry)
print(FourthTry)
print(Fail)
SuccessChance = (FirstTry + SecondTry + ThirdTry + FourthTry)/(FirstTry + SecondTry + ThirdTry + FourthTry + Fail)*100
print(f"Chance of Success: '{SuccessChance}'%")