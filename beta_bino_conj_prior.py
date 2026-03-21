#!/usr/bin/env python3

import numpy as np
from dataclasses import dataclass
import matplotlib.pyplot as plt

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
Beta distribution. It's worth noting that setting the beta(a,b) distribution parameters to a=1, b=1, 
makes the prior beta distribution equal to a uniform distribution defined in the range [0,1] 
"""
@dataclass
class Beta:
    a: int
    b: int

def mean(beta : Beta) -> float:

    a : float = beta.a
    b : float = beta.b

    return a / (a + b)


def variance(beta : Beta) -> float:

    a : float = beta.a
    b : float = beta.b

    return (a * b) / ((a + b)**2 * (a + b + 1))

"""
Total number of iterations of Bayesian inference.
"""
total_trials : int = 1_000

posteriors : list[Beta] = [Beta(a=1, b=1)]
iterations : range = range(1, total_trials + 1)

for n in iterations:
    """ Toss the coin and observe the outcome. We are assigning the value of 1 to heads and 0 to tails.
    Therefore, we can just add up the number of heads."""
    flip : int = tossCoin()

    """ Calculate the posterior beta distribution. """
    prior : Beta = posteriors[-1]

    posteriors.append(Beta(
            a = prior.a + flip,
            b = prior.b + (1 - flip)
        ))

mean_line : list[float] = [mean(beta) for beta in posteriors]
variance_line : list[float] = [variance(beta) for beta in posteriors]
std_dev_line : list[float] = [np.sqrt(variance) for variance in variance_line]
iteration_list : list[float] = [0.] + list(iterations)

"""
NOTE: this assumes the distribution is symmetric. Obsviously the beta distribution
is not always symmetric, however for visualisation purposes this does not matter.
"""
upper_bound_line : list[float] = [x + s for x, s in zip(mean_line, std_dev_line)]
lower_bound_line : list[float] = [x - s for x, s in zip(mean_line, std_dev_line)]


fig, ax = plt.subplots()
fig.suptitle("Convergence of Beta conjugate prior to the true probability of heads for a fair coin.")


ax.grid()

ax.axhline(y=.5, linestyle=":" ,label="True probability.")
ax.plot(mean_line, label="Posterior Mean.")
ax.fill_between(iteration_list, upper_bound_line, lower_bound_line, alpha=0.3, label=r"$\sigma$ bound")

ax.set_xlim(0, total_trials)
ax.set_ylim(0, 1)

ax.set_ylabel("Probability of observing heads after flipping a coin (Posterior Mean).")
ax.set_xlabel("Coin Flips.")

ax.legend()
plt.show()

