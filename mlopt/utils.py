import numpy as np
from mlopt.settings import INFEAS_TOL, SUBOPT_TOL
#  import scipy.io as spio
#  import cvxpy as cp
#  import scipy.sparse as spa


def n_features(df):
    """
    Get number of features in dataframe
    where cells contain tuples.

    Parameters
    ----------
    df : pandas DataFrame
        Dataframe.

    Returns
    -------
    int
        Number of features.
    """
    n = 0
    for c in df.columns.values:
        if isinstance(df[c].iloc[0], list):  # If list add length
            n += len(df[c].iloc[0])
        else:  # If number add 1
            n += 1
    return n


def pandas2array(X):
    """
    Unroll dataframe elements to construct 2d array in case of
    cells containing tuples.
    """

    if isinstance(X, np.ndarray):
        # Already numpy array. Return it.
        return X
    else:
        # get number of datapoints
        n_data = len(X)
        # Get dimensions by inspecting first row
        n = n_features(X)

        # Allocate full vector
        X_new = np.empty((0, n))

        # Unroll
        # TODO: Speedup this process
        for i in range(n_data):
            x_temp = np.array([])
            x_data = X.iloc[i, :].values
            for i in x_data:
                if isinstance(i, list):
                    x_temp = np.concatenate((x_temp, np.array(i)))
                else:
                    x_temp = np.append(x_temp, i)
            X_new = np.vstack((X_new, x_temp))

    return X_new


def suboptimality(cost_pred, cost_test):
    """Compute suboptimality"""
    return (cost_pred - cost_test)/(np.abs(cost_test) + 1e-10)


def accuracy(results_pred, results_test):
    """
    Accuracy comparison between predicted and test results.

    Parameters
    ----------
    results_red : dictionary of predict results.
        List of predicted results.
    results_test : dictionary of test results.
        List of test results.

    Returns
    -------
    float:
        Fraction of correct over total strategies compared.
    numpy array:
        Boolean vector indicating which strategy is correct.
    numpy array:
        Boolean vector indicating which strategy is exact.
    """

    # Assert correctness by compariing solution cost and infeasibility
    n_points = len(results_pred)
    assert n_points == len(results_test)

    idx_correct = np.zeros(n_points, dtype=int)
    for i in range(n_points):
        r_pred = results_pred[i]
        r_test = results_test[i]
        # Check if prediction is correct
        if r_pred['strategy'] == r_test['strategy']:
            idx_correct[i] = 1
        else:
            # Check feasibility
            if r_pred['infeasibility'] <= INFEAS_TOL:
                # Check cost function value
                subopt = suboptimality(r_pred['cost'], r_test['cost'])
                if subopt <= SUBOPT_TOL:
                    idx_correct[i] = 1

    return np.sum(idx_correct) / n_points, idx_correct


# TODO: Fix creation from matlab file
#  def read_mat(filepath):
#      # Load file
#      m = spio.loadmat(filepath)
#
#      # Convert matrices
#      c = m['c'].T.flatten().astype(float)
#      Aeq = m['Aeq'].astype(float).tocsc()
#      beq = m['beq'].T.flatten().astype(float)
#      Aineq = m['Aineq'].astype(float).tocsc()
#      bineq = m['bineq'].T.flatten().astype(float)
#      if len(m['int_idx']) > 0:
#          int_idx = m['int_idx'].T.flatten().astype(int)
#      else:
#          int_idx = np.array([], dtype=int)
#
#      # Create cvxpy problem
#      x = cp.Variable(len(c))
#      cost = c * x
#      constraints = []
#
#
#
#      return problem_data(c, l, A, u, int_idx)
