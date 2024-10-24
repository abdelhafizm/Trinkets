from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr


def calculate_correlation(X, Y, nodes):
    """
    Filters a given dataset, then finds Pearson correlation between first principal component of filtered dataset and target variable.

    :param X: Full, unfiltered dataset, as a pandas DataFrame.
    :param Y: Target variable.
    :param nodes: Indices of columns in full dataset to consider.
    :return: (correlation, p-value)
    """
    filt_X = X.iloc[:, nodes]

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(filt_X)

    pca = PCA(n_components=1)
    pc1 = [i for i in pca.fit_transform(scaled_X)]

    corr, p_val = pearsonr(pc1, Y)

    return corr, p_val
