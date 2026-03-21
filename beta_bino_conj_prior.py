#!/usr/bin/env python3

import numpy as np

def tossCoin() -> int:
    """
    Simulated coin toss. We are assuming that the coin is fair and that there are only two possible outcomes.

    Returns
    -------
    Integer representing the outcome of the coin flip. Returns 1 coin landed on heads, 0 if it landed on tails. 
    """

    """ Drawing from a discrete uniform distribution: either 0 or 1 with equal probability. Assigns 1 to heads and 0 to tails. """
    return np.random.randint(0,2)


"""
Total number of iterations of Bayesian inference.
"""
total_trials : int = 1_000

"""
Prior beta distribution. It's worth noting that setting the beta(a,b) distribution parameters to a=1, b=1, 
makes the prior beta distribution equal to a uniform distribution defined in the range [0,1] 
"""
beta : dict = {
        'a' : 1,
        'b' : 1,
        }

for n in range(1, total_trials + 1):
    """ Toss the coin and observe the outcome. We are assigning the value of 1 to heads and 0 to tails.
    Therefore, we can just add up the number of heads."""
    flip : int = tossCoin()

    """ Calculate the posterior beta distribution. """
    beta['a'] += flip
    beta['b'] += 1 - flip

a : float = beta['a']
b : float = beta['b']

posterior_mean = a / (a + b)
posterior_var = (a * b) / ((a + b)**2 * (a + b + 1))

print(posterior_mean)
print(posterior_var)

