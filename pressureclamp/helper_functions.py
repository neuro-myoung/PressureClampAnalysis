def sigmoid_fit(p, p50, k):
    """
    This function defines a sigmoid curve.

    Arguments: 
    p - the abscissa data.
    p50 - the inflection point of the sigmoid.
    k - the slope at the inflection point of a sigmoid.
    
    Returns:
    The ordinate for a boltzmann sigmoid with the passed parameters.
    """
    return(1 / (1 + np.exp((p50 - p) / k)))


def ngauss_guesses(x, y, nGauss):
    initial_guesses = {"p":[1], "u": [x[np.argmax(y)]], "s": [0.5]}
    for i in list(range(0, nGauss - 1)):
        initial_guesses["p"].append(0.5 * initial_guesses["p"][i])
        initial_guesses["u"].append(-2.2 * (i+1) + initial_guesses["u"][i])
        initial_guesses["s"].append(2 * initial_guesses["s"][i])

    arr = [np.array(initial_guesses['p']), np.array(initial_guesses['u']), np.array(initial_guesses['s'])]

    return(arr)
    
def single_gauss_fit(x, a1, m1, s1):
    gauss = a1 * norm.pdf(x, loc = m1, scale = s1)

    return gauss

def double_gauss_fit(x, a1, a2, m1, m2, s1, s2):
    gauss = a1 * norm.pdf(x, loc = m1, scale = s1)
    gauss += a2 * norm.pdf(x, loc = m2, scale = s2)

    return gauss

def triple_gauss_fit(x, a1, a2, a3, m1, m2, m3, s1, s2, s3):
    gauss = a1 * norm.pdf(x, loc = m1, scale = s1)
    gauss += a2 * norm.pdf(x, loc = m2, scale = s2)
    gauss += a3 * norm.pdf(x, loc = m3, scale = s3)

    return gauss