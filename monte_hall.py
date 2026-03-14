import numpy as np
import matplotlib.pyplot as plt

"""
Monte Carlo simulations of the Monte Hall random experiment: 
The Monte Hall experiment goes as follows. The player is presented with three doors, one of which has a prize behind it, the other two which don't. 
The player gets to choose one of the three doors that they believe has the prize behind it. Once the player has selected a door, the host reveals 
one of the two remaining doors that does NOT contain a prize behind it leaving two doors closed - the one that the player chose, and another door that was not revealed. 
The host then asks the player if they would like to change thier choice of door given this new information. 

The Monte Hall problem is as follows: Should the player change their choice given that the host revealed one of the doors that does not have the prize in it. 

The experiments hypothesis are as follows:
- H0 (Null Hypothesis): The probability of that the user wins the prize is not effected by whether they change their choice or not.  
- H1 (Alternative Hypothesis): Switching doors improves the probability of winning the prize.

The aim is test whether the Bayesian probability calcuation matches the empirical results generated from running a 
Monte Carlo simulation of the random experiment.

In honour of Conor.
"""

def monteHall(switch : bool) -> bool:
    """
    Performs one iteration of the Monte Hall random experiment. The function simulates the process of:
    - the prize getting placed behind a door,  
    - the player selecting a door,
    - one of the two remaining doors without the prize behind being revealed,
    - the player either choosing to switch doors or not based on the switch flag. 

    Parameters
    ----------
    switch : bool
    Flag indicating if the player will switch doors or not. True means they will switch, false means they will not

    Returns
    -------
    A flag indicating whether the player won the prize or not.
    """


    """ Select a door with the prize behind it. This is modelled as a discrete uniform distribution
    under the assumption that each door is equally likely to have the prize behinde it. """
    prize_door : int = np.random.randint(0, 3)

    """ The first door selection made by the player. This is modelled as a discrete uniform distribution 
    under the assumption that the player will select any of the given doors with equally probability. """
    selected_door : int = np.random.randint(0, 3)

    """ The door containing no prise that is revealed to the player after their initial choice. This door is one
    of the two remaining door that does not contain the prize. """
    revealed_door : int = getRevealedDoor(prize_door, selected_door)

    """ If the player chooses to switch doors. """
    if switch:
        selected_door = getSwitchedDoor(revealed_door, selected_door)


    return selected_door == prize_door

def getRevealedDoor(prize_door : int, selected_door : int) -> int:
    """
    Determines which door should be revealed to the player. The door must not be the door containing the prize or 
    the door the player has already choosen. This algorithm simply selects the door that is to the right of the prize door 
    (wrapped around), and if that door is the players selected door, then it just chooses the next door to the right.

    Parameters
    ----------
    prize_door : int
    The door containing the prize behind it.

    selected_door: int
    The initial door selection made by the player

    Returns
    -------
    The integer value representing the door that the host would reveal to the contestant given their initial door choice.
    """
    revealed_door : int = (prize_door + 1) % 3
    if (revealed_door == selected_door):
        revealed_door = (selected_door + 1) % 3 
    return revealed_door

def getSwitchedDoor(revealed_door : int, selected_door : int) -> int:
    """ 
    Determines which door the user would switch to given the door that it can't be the door that has already 
    been revealed or the door that the player initially selected.

    Parameters
    ----------
    revealed_door : int
    The door that was revealed to the player after their initial door choice was made.

    selected_door : int
    The door that the player initially selected.

    Returns
    -------
    The remaining door that the user could have switched to.
    """
    new_selection : int = (selected_door + 1) % 3
    if (new_selection == revealed_door):
        new_selection = (revealed_door + 1) % 3

    return new_selection


def runTrials(switch : bool, total_trials : int = 10000) -> float :
    """
    Perform Monte Carlo trials using the MonteHall random experiment. These trails will be run
    for two cases: the player switches their door when the other door is revealed and the player
    remaining with the initial door they selected.

    Parameters
    ----------
    switch : bool
    Flag indicating if the player will switch doors when the door not containing the prize is revealed.
    True if the player will switch, false if the player will remain with their respective door.
    """
    total_wins : int = 0
    for _ in range(total_trials):
        win : bool = monteHall(switch)
        if (win):
            total_wins += 1

    return total_wins / total_trials

def Bayesian(switch : bool) -> float: 
    """
    It is worth restating that, in the standard Monty Hall problem:
    - The prize is equally likely to be behind any door.
    - The player initially chooses a door without information.
    - The host follows the same rule regardless of which door is chosen.

    Hence, the game is invariant under relabeling the doors. This means
    that if we fix the players choice, and calculate its probabilities, we do not 
    lose generality.

    With that said, lets assume that the player chooses door 1. We now want to calculate
    the probability that the prize is behind door 1.

    The following definitions will be used:
    - X : Door X that the prize behind.
    - Y : Door Y that the host reveals does not contain the prize. Note that X != Y.

    We are interested in calculating:
    - P(X | Y) : The probability that the door X prize contains the prize given
    that the host revealed door Y does not contain the prize.
    
    To do this we need to utilise Bayes theorem which states:
    - P(X | Y) = (P(Y | X) * P(X)) / P(Y)
    where
    - P(X) : Prior probability that the door that the prize is behind door X.
    - P(Y) : Probability that the host reveals door Y out of the two remaining doors.
    - P(Y | X) : Probability that the host reveals the door Y given that door X has the prize.
    """

    """ The player makes a selection of one of the three doors. In our example, we say door 1.
    The probability of the prize being behind any one of the three doors is assumed to be equal. 
    Therefore, the prior probability that the door selected by the player has the prize is
    calculated as: P(X) = 1/3
    """
    prior : float = 1 / 3
    
    """ The player now selects a door and the host reveals whats inside one of the two remaining doors 
    that does not contain the prize. We now need to compute the likelihood of the host revealing that specific door 
    not containing the prize given that the initial door selected by the player is Door 1. We note that in order to 
    compute the probability of door Y being revealed given that the player selected door 1, we must compute 
    the probability of door Y being revealed given all possible combinations of where the prize is.

    Therefore the likelihood that the host revealed the specific door not containing the prize: P(Y | X) = 1/2.
    """
    likelihood : float = 1 / 2
    
    """ The numerator, defined by the product of the prior and the likelihood, P(Y | X) * P (X), needs to normalised by 
    the probability that door Y gets choosen. Using the law of total probability, the probablity of door Y getting choosen
    can be found by considering the sum of Y getting choosen and all the doors that could contain the prize. Recall
    that the door opened can't the one the player chose or the one with the prize. For example, let's assume the player selected door 1,
    then the probability of door 2 being opened by the host can be calculated as:
        P(Y = 2) = P(Y=2 | X=1) * P(X=1) + P(Y=2 | X=2) * P(X=2) + P(Y=2 | X=3) * P(X=3)
             = 1/2 * 1/3 + 0 * 1/3 + 1 * 1/3
             = 1/6 + 1/3
             = 1/2
    Notice how to P(Y=2 | X=2) = 0, due to the fact that the host can't open a door that contains the prize, and 
    P(Y=2 | X=3) = 1, for the same reason, but also applying the constraint that door 1 can't be picked either,
    since that is the one the player picked, meaning that door 2 is the only option, makings its probability 1.
    """
    normalization : float = 1/2
    
    """ Using Bayes theorem, the probablity that the player selected the correct door given the that the host opened up door
    Y can be calculated as follows. However, not that if we calculate the closed for solution for Bayes theorem in this 
    context, we get:
        P(X | Y) = (1/2 * 1/3) / 1/2
                 = 1/3
    """
    probability : float = (likelihood * prior) / normalization

    """ If the player chooses not to switch, then return the probability that the prize is under the players choice. 
    Note that if the play chooses not to switch, then the probability that their choice contains the prize is equal
    to prior probability that their choice contained the prize. It is effectively as though you ignored the new 
    information.
    """
    if not switch:
        return  probability

    """ If the player switches, the probability that the switched door contains the prize is equal to the complement
    of the prior probability (1 - P(X | Y)), since their are only two doors to choose from (stay or switch), therefore,
    these two outcomes partition the probability space:
    """
    return 1 - probability

total_trials : int = 10000
switch_win_rate = runTrials(switch = True, total_trials=total_trials)
stay_win_rate = runTrials(switch = False, total_trials=total_trials)

fig, ax = plt.subplots(nrows=2, ncols=2)
fig.suptitle("Win-to-loss percentages in the Monty Hall problem")

ax[0,0].set_title("When switching")
ax[0,1].set_title("When staying with original choice")

ax[0,0].set_ylabel("Empirical: " + str(total_trials) + " trials")
ax[1,0].set_ylabel("Theoretical")

ax[0,0].pie([switch_win_rate, 1 - switch_win_rate], labels=["win", "loss"], autopct="%1.1f%%")
ax[0,1].pie([stay_win_rate, 1 - stay_win_rate], labels=["win", "loss"], autopct="%1.1f%%")

switch_win_rate = Bayesian(switch = True)
stay_win_rate = Bayesian(switch = False)

ax[1,0].pie([switch_win_rate, 1 - switch_win_rate], labels=["win", "loss"], autopct="%1.1f%%")
ax[1,1].pie([stay_win_rate, 1 - stay_win_rate], labels=["win", "loss"], autopct="%1.1f%%")
plt.show()
