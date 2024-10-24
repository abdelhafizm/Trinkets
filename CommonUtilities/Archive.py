from pickle import dump, load
from pathlib import Path
from datetime import datetime
from CommonUtilities.Notify import send_notification


def pickle_save(variable, filename, directory=None, notify=True, timestamp=False):
    directory = Path(directory) if directory is not None else Path()
    directory.mkdir(parents=True, exist_ok=True)

    filename = Path.with_suffix(Path(Path(filename).stem + '_' + datetime.now().strftime('%H-%M-%S')),
                                '.pkl') if timestamp else Path.with_suffix(Path(filename), '.pkl')

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
