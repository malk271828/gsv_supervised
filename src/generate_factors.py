import numpy as np

from notears import nonlinear
import notears.utils as ut

if __name__ == "__main__":

    n, d, s0, graph_type, sem_type = 200, 5, 9, 'ER', 'mim'
    B_true = ut.simulate_dag(d, s0, graph_type)
    np.savetxt('W_true.csv', B_true, delimiter=',')

    X = ut.simulate_nonlinear_sem(B_true, n, sem_type)
    np.savetxt('X.csv', X, delimiter=',')
