import numpy as np
from numpy import mean, cov, linalg
from .sequence_attributes import SequenceAttributes


class PCAAttributes:
    def __init__(self, data):
        self.data = data
        self.patterns = [pattern for pattern in SequenceAttributes.ALL_PATTERNS if
                         pattern not in ["fl", "fp", "ll", "lp"]]

    def __calc_pca(self):
        data = [self.data[pattern] for pattern in self.patterns]
        data = np.vstack(tuple(data)).T

        self.loadings, self.eigenvalues = self.princomp(data)

        return self.loadings

    def attributes(self, size=50):
        self.__calc_pca()
        norms = np.array([np.linalg.norm(x[:size]) for x in self.loadings])
        return sorted([self.patterns[i] for i in np.argsort(norms)[::-1][:size]])

    def princomp(self, A):
        """ performs principal components analysis
            (PCA) on the n-by-p data matrix A
            Rows of A correspond to observations, columns to variables.

        Returns :
         loadings :
           is a p-by-p matrix, each column containing coefficients
           for one principal component.
         latent :
           a vector containing the eigenvalues
           of the covariance matrix of A.
        """
        # computing eigenvalues and eigenvectors of covariance matrix
        M = (A - mean(A.T, axis=1)).T  # subtract the mean (along columns)
        [latent, loadings] = linalg.eig(cov(M))  # attention:not always sorted
        # score = dot(loadings.T, M)  # projection of the data in the new space
        return loadings, latent