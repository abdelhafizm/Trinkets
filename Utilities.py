def calculate_correlation(X, Y, nodes):
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler
    from scipy.stats import pearsonr

    filt_X = X.iloc[:, nodes]

    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(filt_X)

    pca = PCA(n_components=1)
    pc1 = [i for i in pca.fit_transform(scaled_X)]

    corr, p_val = pearsonr(pc1, Y)

    return corr, p_val


def send_notification(message, priority=0, image_path=None):
    import requests
    import keyring

    url = 'https://api.pushover.net/1/messages.json'
    params = {
        'token': keyring.get_password('Pushover', 'token'),
        'user': keyring.get_password('Pushover', 'user'),
        'device': 'mohamediphone',
        'message': message,
        'priority': priority
    }
    files = {
        'attachment': ('img', open(image_path, 'rb'))
    } if image_path else {}

    r = requests.post(url=url, data=params, files=files)

def pickle_save(variable, filename, directory=None, notify=True, timestamp=False):
    from pickle import dump
    from pathlib import Path
    from datetime import datetime

    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(Path(filename).stem + '_' + datetime.now().strftime('%H-%M-%S')), '.pkl') if timestamp else Path.with_suffix(Path(filename), '.pkl')
    
    try:
        with Path(directory, filename).open('wb') as file:
            dump(variable, file)
            
    except Exception as e:
        if notify:
            send_notification(f'Error saving {filename}: {e}')
        return

    if notify:
        send_notification(f'Saved {filename}')

def pickle_load(filename, directory=None, notify=False):
    from pickle import load
    from pathlib import Path

    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(filename), '.pkl')

    if Path(directory, filename).exists():
        try:
            with Path(directory, filename).open('rb') as file:
                variable = load(file)
    
        except Exception as e:
            if notify:
                send_notification(f'Error loading {filename}: {e}')
            return None

        if notify:
            send_notification(f'Loaded {filename}')
        
    else:
        send_notification(f'Unable to read {filename} because it doesn\'t exist.')
        return None

    return variable

def plot_with_metrics(X, Y, title=None, x_label=None, y_label=None, metrics=None, save=True, directory=None, timestamp=True, notify=False):
    import matplotlib.pyplot as plt
    from pathlib import Path
    from datetime import datetime

    plt.figure()
    plt.plot(X, Y)

    if title:
        plt.title(title)
    else:
        title = 'Unnamed Figure'
        timestamp = True

    if x_label:
        plt.xlabel(x_label)

    if y_label:
        plt.ylabel(y_label)

    if metrics:
        label = ''
        for key in metrics:
            label += f'{key}: {metrics[key]}\n'
        
        plt.figtext(0.95, 0.5, label[:-1], bbox=dict(boxstyle="round", fc="0.8"))

    if save:
        directory = Path(directory) if directory is not None else Path()
        directory.mkdir(parents=True, exist_ok=True)

        filename = title
        
        for char in '<>:"/\|?* ':
            filename = filename.replace(char, '_')

        if timestamp:
            filename += '_' + datetime.now().strftime('%H-%M-%S-%f')
        
        filename = Path.with_suffix(Path(filename), '.png')

        plt.savefig(Path(directory, filename), bbox_inches='tight')

    if notify:
        under_size_limit = Path(directory, filename).stat().st_size < 5242880 if save else False
        send_notification(f'Plot saved: {title}', image_path=Path(directory, filename) if save and under_size_limit else None)
