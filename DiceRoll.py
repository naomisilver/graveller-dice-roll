import random
import time
from itertools import repeat
from multiprocessing import Pool, cpu_count

# roll a 4 sided dice 231 times, in hopes of achieving 177 of one face. 

def diceRoll(maximumRolls):
    numbers = [0,0,0,0] 
    items = [1,2,3,4] # your use of random.choice was the most optimal given a bunch of testing :)

    highestRoll = 0

    for i in range (maximumRolls):
        numbers = [0,0,0,0]
        notSoftlockedPog = False # not softlocked pog face

        for i in repeat(None, 231): # same as your use of repeat, compared to randint this implementation shaved off 15 seconds in a non-parralelised run of 1 million simulations
            roll = random.choice(items)
            numbers[roll-1] += 1
        
            if numbers[roll-1] == 177:
                notSoftlockedPog = True # break out of the loop if one of the faces hits 177
                break

            currentMax = max(numbers)
            if currentMax > highestRoll: #calculate the max seen this simulation and compare to the max of the former simulations
                highestRoll = currentMax

        if notSoftlockedPog:
            break

    return highestRoll

def main():
    maximumRolls = 1000000 # pick your roll count here 
    numProcesses = cpu_count() # use as many cores as are available, this WILL use 100% of your cpu so yeah
    rollsPerProcess = maximumRolls // numProcesses

    st = time.time() # start time is current time, source: https://stackoverflow.com/questions/6786990/find-out-time-it-took-for-a-python-script-to-complete-execution

    with Pool(processes=numProcesses) as pool:
        results = pool.map(diceRoll, [rollsPerProcess] * numProcesses)

    highestRoll = max(results)

    print(f"run time: {time.time() - st:.2f} seconds")
    print(f"highest roll: {highestRoll}") # browsed the docs for all the multiprocessing implenetation: https://docs.python.org/3/library/multiprocessing.html

if __name__ == "__main__":  
    main()