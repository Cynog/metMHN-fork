from itertools import compress, chain, combinations
import numpy as np


def state_space(n: int) -> list:
    """
    Args:
        n (int): total number of events
    Returns:
         list: complete statespace
    """
    return [f'{i:0b}'.zfill(n)[::-1] for i in range(2**n)]


def trunk_states(dpoint: list) -> list:
    """
    Args:
        dpoint (list): Bitstring, genotype of a single patient
    Returns:
        list: states that the tumor could have visited during progression
    """
    n = len(dpoint)
    inds = np.ones(1)
    for i in range(n):
        if dpoint[i] == 1:
            inds = np.kron(np.array([1, 1]), inds)
        else:
            inds = np.kron(np.array([1, 0]), inds)

    return [state for state in compress(state_space(n), inds)]


def ssr_to_fss(state: np.array) -> np.array:
    """This gives the indices of the rate matrix that are appearing in the
    state space restricted rate matrix.

    Args:
        state (np.array): Binary state vector, representing the current sample's
        Fevents.

    Returns:
        np.array: Indices of the rate matrix.
    """
    res = np.ones(1)
    for s in state:
        res = np.kron(np.array([1, s]), res)
    return res.astype(bool)


def random_theta(n: int, sparsity: float) -> np.array:
    """
    Generates a logarithmic theta with normal distributed entries
    Args:
        n (int): Number of mutations
        sparsity (float): Percentage of zero entries in theta
    returns:
        np.array: theta
    """
    npone = n + 1
    log_theta = np.zeros((npone, npone))
    log_theta += np.diag(np.random.normal(size=npone))
    index = np.argwhere(log_theta == 0)[
        np.random.choice(npone**2-npone, size=int((npone**2-npone)
                         * (1-sparsity)), replace=True)
    ]
    log_theta[index[:, 0], index[:, 1]] = np.random.normal(
        size=int((npone**2-npone)*(1-sparsity)))
    return log_theta


def reachable_states(n: int):

    reachable = np.zeros(2**(2*n + 1))

    for i in chain.from_iterable(combinations(list(range(n)), r) for r in range((n+1))):
        reachable[sum((2**(2*j))*3 for j in i)] = 1

    reachable[2**(2*n):] = 1
    return reachable.astype(bool)

    return theta


def finite_sample(pTh: np.array, k: int) -> np.array:
    """
    Generates k random samples drawn from a probability distribution pTh
    Code taken from https://github.com/spang-lab/LearnMHN/blob/main/mhn/original/UtilityFunctions.py
    Args:
        pTh (np.array): Probability distribution to draw samples from
        k (int): Number of samples to draw
    Returns:
         np.array: Subsampled probability distribution
    """
    n = pTh.size
    return np.bincount(np.random.choice(n, k, replace=True, p=pTh), minlength=n) / k

