import numpy as np


def _circle_rect_pvol(center, radius, corners, samples=10000):
    """
    Monte Carlo estimation of circle/rectangle intersection.

    Parameters
    ----------
    center : length-2 iterable of floats
        Center of the circle (row, column).
    radius : float
        Radius of the circle.
    corners : (4, 2) ndarray of floats
        Corner coordinates, clockwise from upper left.
    samples : int
        Number of random samples; more results in a better estimation.

    Returns
    -------
    intersection : float
        Fraction of rectangle described by `corners` which is
        the intersection of said rectangle and the circle.
    """
    r = np.random.uniform(low=corners[0, 0], high=corners[2, 0], size=samples)
    c = np.random.uniform(low=corners[0, 1], high=corners[1, 1], size=samples)
    levelset = (r - center[0])**2 + (c - center[1])**2 - radius**2 < 0
    return levelset.sum() / samples


def disk(rr, cc, center, radius, precision=0.0001):
    """
    Return a circle with partial volumes calculated.

    Parameters
    ----------
    rr : (M, N) ndarray of floats
        Row point coordinates.
    cc : (M, N) ndarray of floats
        Column point coordinates.
    center : length-2 iterable of floats
        Center of the circle (row, column).
    radius : float
        Radius of the circle.

    Returns
    -------
    disk : (M, N) ndarray of floats
        Circular structuring element with partial volumes, i.e.,
        each point carries a value on the range [0, 1] representing
        the fraction of the rectangular space it occupies which the
        circle intersects.

    Notes
    -----
    All input values should carry consistent units. The partial
    volumes are closely approximated via Monte Carlo simulation.
    """
    stepr = rr[1, 0] - rr[0, 0]
    stepc = cc[0, 1] - cc[0, 0]

    # Padded array of point indices half-between all pixel centers
    rrr = np.pad(rr[:, 0] - stepr/2, (0, 1),
                 mode='constant', constant_values=rr[-1, 0] + stepr/2)
    ccc = np.pad(cc[0, :] - stepc/2, (0, 1),
                 mode='constant', constant_values=cc[0, -1] + stepc/2)

    corners = np.zeros(shape=(4, 2))

    # The partial volume array
    disk = np.zeros_like(rr, dtype=np.float64)

    for i in range(disk.shape[0]):
        for j in range(disk.shape[1]):
            # Corners clockwise from upper left
            corners[:, 0] = [rrr[i], rrr[i], rrr[i + 1], rrr[i + 1]]
            corners[:, 1] = [ccc[j], ccc[j + 1], ccc[j + 1], ccc[j]]

            disk[i, j] = _circle_rect_pvol(center, radius, corners,
                                           samples=int(1 / precision))

    return disk
