from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import pearsonr


def calculate_correlation(X, Y, nodes):
    filt_X = X.iloc[:, nodes]

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(filt_X)

    pca = PCA(n_components=1)
    pc1 = [i for i in pca.fit_transform(scaled_X)]

    corr, p_val = pearsonr(pc1, Y)

    return corr, p_val
