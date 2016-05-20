from random import choice 
def randFunc():
    alpha = choice('efghijklmnopqrstuvwxyz') 
    numeric = choice([x for x in range(1,10)]) 
    return 'sd' + str(alpha) + str(numeric)


