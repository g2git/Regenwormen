import math
from collections import Counter
from functools import cache

def results_dict(string):
    # Count the occurrences of each element
    counter = Counter(string)
    # Convert the counter to a dictionary
    return dict(counter)


def results_list(string):
    # Count the occurrences of each element
    counter = Counter(string)
    # Convert the counter to a list of tuples
    return sorted(list(counter.items()))


# Rolling a nmber at least k times out of n dices using p-sided dices
def combo(n, p, k):
    res = sum(((1/p)**(x)) * (((p-1)/p)**(n-x)) * math.comb(n, x) for x in range(k, n+1))
    return res


# Create a list of all possible rolls
@cache
def posibilities(hand):
    if hand == "":
        return [""]

    return [
        x + y 
        for x in ("12345R" if hand[0] == "o" else hand[0])
        for y in posibilities(hand[1:])
    ]


# Probability of rolling desired_number at least min_times with number_dices
def probability_of_rolling(number_dices, desired_number , min_times):
    t = 0
    # Create a list of all possibe rolls with number_dices
    p = posibilities(number_dices*"o")
    for i in p:
        # Count all rolls with at least min_times the desired number
        if i.count(str(desired_number)) >= min_times:
            t += 1
    return t / len(p)
    

# Dictionary of dice result and corresponding integer value 
ogen = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "R": 5
}

# Calculate the current score
def score(di):
    tot = 0
    if isinstance(di, dict):
        for k, v in di.items():
            tot += ogen[k] * v
        return tot
    else:
        for k, v in di:
            tot += ogen[k] * v
        return tot
    
regw = {"5": 4, "4": 1}

# Total number of events
n = 0
# Total number of successes
suc = 0

# Play all possibilities until no more dices left
def calc(reg, pts = 34):
    # Check if the number of dices is valid
    if sum(list(reg.values())) > 8:
        print("Invalid combintaion entered")
        return 0
    global n
    global suc
    # Calculate remaining dices
    dices = 8 - sum(list(reg.values()))
    
    # If no more dices left return 1 for the event and 1 if the event was a success otherwise 0
    if dices == 0:
        n += 1
        if score(reg) >= pts and "R" in reg:
            suc += 1
        return True
    # Analyze all possible outcomes of dice rolls
    for pos in posibilities(dices*"o"):
        # Skip to next pos if all dice numbers are already taken
        if all(x in reg for x in pos):
            n += 1
            continue
        
        # Create a dictionary for each dice number(key) and the count of their occurrences(value)
        ps = results_dict(pos)
        for p, v in ps.items():
            # Skip to next dice number if the current dice number was already taken
            if p in reg:
                continue
            # Create a copy of the dictionary to analyze
            new_reg = reg.copy()
            # Add cuurent choice
            new_reg[p] = v
            calc(new_reg)
    return True


# Play all possibilities until no more dices left
@cache
def calc_2(reg, pts = 28):
    # Check if the number of dices is valid
    if sum([row[1] for row in reg]) > 8:
        print("Invalid combintaion entered")
        return 0
    
    # Total number of events
    n = 0
    # Total number of successes
    su = 0
    # Calculate remaining dices
    dices = 8 - sum([row[1] for row in reg])
    
    # If no more dices left return 1 for the event and 1 if the event was a success otherwise 0
    if dices == 0:
        if score(reg) >= pts and any("R" in r[0] for r in reg):
            su += 1
        return (1, su)
    
    # Analyze all possible outcomes of dice rolls
    for pos in posibilities(dices*"o"):
        # Skip to next pos if all dice numbers are already taken
        if all(any(x in r[0] for r in reg) for x in pos):
            n += 1
            continue
        # Create a tuples list for each dice number and the count of their occurrences
        ps = results_list(pos)
        for p, v in ps:
            # Skip to next dice number if the current dice number was already taken
            if any(p in r[0] for r in reg):
                continue
            # Create a new tuple of the dices taken plus the chosen dice numbers
            new_reg = reg + ((p,v),)
            # Determine the number of events and successes after playing the current combination
            n, su = (x + y for x, y in zip((n, su), calc_2(new_reg)))
    
    # Return the total number of events and successes
    return n, su


# Play and stop when points reached
@cache
def calc_w_stop(reg, pts = 28):
    # Check if the number of dices is valid
    if sum([row[1] for row in reg]) > 8:
        print("Invalid combintaion entered")
        return 0
    
    # Total number of events
    n = 0
    # Total number of successes
    su = 0
    # Calculate remaining dices
    dices = 8 - sum([row[1] for row in reg])
    
    # If no more dices left or points reached return 1 for the event and 1 if the event was a success otherwise 0
    if dices == 0 or (score(reg) >= pts and any("R" in r[0] for r in reg)):
        if score(reg) >= pts and any("R" in r[0] for r in reg):
            su += 1
        return (1, su)
    
    # Analyze all possible outcomes of dice rolls
    for pos in posibilities(dices*"o"):
        # Skip to next pos if all dice numbers are already taken
        if all(any(x in r[0] for r in reg) for x in pos):
            n += 1
            continue
        
        # Create a tuples list for each dice number and the count of their occurrences
        ps = results_list(pos)
        # See if one of the dice choices gives the desired points
        for p, v in ps:
            # Skip to next dice number if the current dice number was already taken
            if any(p in r[0] for r in reg):
                continue
            # If desired points reached go to next pos, else analyze calc_w_stop for each option
            if score(reg) + ogen[p]*v >= pts and any("R" in r[0] for r in reg):
                n += 1
                su += 1
                break
        else:
            for p, v in ps:
                # Skip to next dice number if the current dice number was already taken
                if any(p in r[0] for r in reg):
                    continue
                # Create a new tuple of the dices taken plus the chosen dice numbers
                new_reg = reg + ((p,v),)
                # Determine the number of events and successes after playing the current combination
                n, su = (x + y for x, y in zip((n, su), calc_w_stop(new_reg)))
    
    # Return the total number of events and successes
    return n, su

# Dices taken
regw_2 = (("R", 4),)

n_2, su = calc_2(regw_2)
if n_2:
    print(f"calc_2: Gebeurtenissen = {n_2}, success = {su}, kans = {su/n_2}")
    
n_2, su = calc_w_stop(regw_2)
if n_2:
    print(f"calc_w_stop: Gebeurtenissen = {n_2}, success = {su}, kans = {su/n_2}")

print(f'Rolling probability: {probability_of_rolling(8, "R", 4)}')
print(f'Combo probability: {combo(8, 6, 4)}')