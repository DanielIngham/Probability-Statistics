import matplotlib.pylab as plt
import numpy as np
from numpy.typing import NDArray

"""
This data structure specifes the moments of the proposal distribution.
"""
proposal_moments = {
    "mean": 4,
    "sigma": 1
}


def true_distribution(val : float) -> float:
    """ 
    Probablity Mass Function (PMF) of the underlying true distribution. 

    This function returns the probability of observing a specific outcome `val` 
    from the underlying random process. 

    Parameters
    ----------
    val : float 
    outcome of a random process.

    Returns
    -------
    float
    Probability of observing `val` under the underlying distribution. 
    """
    if (val < 2):
        return 0
    if (val < 4):
         return 0.25
    if (val < 5):
        return 0.1 
    if (val < 6):
        return  0.4
    return 0

def proposal_distribution(val : float) -> float:
    """
    The proposal distribution is a Gaussian distribution.

    Parameters
    ----------
    val : float
    outcome of a random process.

    Returns
    -------
    float
    Probability of observing `val` under the proposal distribution. 
    """

    return np.exp((-1 / 2) * ((val - proposal_moments["mean"]) / proposal_moments["sigma"])**2) / np.sqrt(2 * np.pi * proposal_moments["sigma"]**2)



def importance_sampling(sample : float) -> float:
    """
    Performs importance sampling on a sample drawn from the 
    proposal distribution.

    Parameters
    ---------
    sample : float

    Returns
    -------
    float
    Weight of the sample.
    """
    p = true_distribution(sample)
    q = proposal_distribution(sample)

    # NOTE: Clamp q to prevent numeric instability during division.
    q = max(q, 1e-8)

    return p/q


# Range of x values in the plot 
x_plt_range : NDArray = np.linspace(0, 8, 1000)

# Number of samples to be drawn from the proposal distribution.
total_samples : int = 1_000_000
# Draw samples from the proposal distribution.
samples : NDArray  = np.random.normal(loc=proposal_moments["mean"], 
                           scale=proposal_moments["sigma"], 
                           size=total_samples)
# Assigns weights using importance sampling
weights : NDArray  = np.array([importance_sampling(v) for v in samples])
normalised_weights : NDArray  = weights / np.sum(weights)

# Bin the weighted samples creating a probability mass function (PMF) that 
# approximates the true posterior.
plt.hist(samples, \
        bins=total_samples//100, \
        weights=normalised_weights, \
        density=True, \
        alpha=0.6, \
        label="Importance sampling estimate")

# Plot the true posterior distribution
y_true : NDArray  = np.array([true_distribution(v) for v in x_plt_range])
plt.plot(x_plt_range, y_true, label="True underlying distribution")
plt.grid(True)

# Plot the proposal distribution
y_proposal : NDArray  = np.array([proposal_distribution(v) for v in x_plt_range])
plt.plot(x_plt_range, y_proposal, label="Proposal distribution")

plt.xlabel('Outcome of a random process')
plt.ylabel('Probability Density')
plt.legend()
plt.show()
