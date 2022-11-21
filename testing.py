import numpy as np
import random

def random_x():
    return random.randint(0,100)

def random_y():
    return random.randint(0,100)

applesx = np.empty(15, dtype=int)
applesy = np.empty(15, dtype=int)



for i in range(15):
    applesx[i]= random_x()
    applesy[i]= random_y()


print(applesx[7])

