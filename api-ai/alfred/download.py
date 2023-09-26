import os

import alfred

ROOT_DIR = os.path.realpath(os.path.join(__file__, '..', '..'))
SCRIPTS_PATH = os.path.realpath(os.path.join(ROOT_DIR, 'scripts'))


@alfred.command('download:model:pneumonia', help="download pneumonia model")
def model_pneumonia() -> None:
    python = alfred.sh('python', "python is not installed")
    os.chdir(SCRIPTS_PATH)

    alfred.run(python, ['download_pneumonia_model.py'])

@alfred.command('download:model:alzheimer', help="download alzheimer model")
def model_alzheimer() -> None:
    python = alfred.sh('python', "python is not installed")
    os.chdir(SCRIPTS_PATH)

    alfred.run(python, ['download_alzheimer_model.py'])
