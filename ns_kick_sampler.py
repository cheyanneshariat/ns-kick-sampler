"""Sample scalar neutron-star natal-kick speeds."""

import operator

import numpy as np


_F_LOW = 0.126
_LOW = (1.87, 0.55)
_HIGH = (5.62, 0.71)
_V_MIN, _V_MAX = 0.05, 1000.0


def sample_kick_speeds(n, seed=None):
    """Return ``n`` natal-kick speeds in km/s from the fixed global model."""
    if isinstance(n, (bool, np.bool_)):
        raise TypeError("n must be a non-negative integer")
    try:
        n = operator.index(n)
    except TypeError:
        raise TypeError("n must be a non-negative integer") from None
    if n < 0:
        raise ValueError("n must be non-negative")

    rng = np.random.default_rng(seed)
    is_low = rng.random(n) < _F_LOW
    speeds = np.empty(n)

    for mask, (mu, sigma) in ((is_low, _LOW), (~is_low, _HIGH)):
        remaining = np.flatnonzero(mask)
        while remaining.size:
            draws = np.exp(rng.normal(mu, sigma, remaining.size))
            accepted = (draws > _V_MIN) & (draws < _V_MAX)
            speeds[remaining[accepted]] = draws[accepted]
            remaining = remaining[~accepted]

    return speeds
