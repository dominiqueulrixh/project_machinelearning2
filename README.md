# RAG-week1

## TL;DR

- Install pyenv (see [Setup](### Setup))
- Install Python 3.11.4 with pyenv `pyenv install 3.11.4`
- Switch your local Python version to 3.11.4 with `pyenv local 3.11.4`
- Create a virtual environment with `python -m venv venv`
- Activate the virtual environment with `source venv/bin/activate` on macOS and Linux or `venv\Scripts\activate` on Windows
- Install the required packages with `pip install -r requirements.txt`

### Setup

Install pyenv on **macOS**:

```bash
brew update
brew install pyenv
```

Now add the following line towards the bottom of your `.bash`, .`bash_profile` or `.zshrc` file (it depends on which you use):

```bash
eval "$(pyenv init -)"
```

Then load the file with `source ~/.bash_profile` or `source ~/.zshrc` or `source ~/.bashrc`.

Install pyenv on **Windows**:

Open powershell and run:

```bash
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```

For **everyone**: Check now whether pyenv is installed correctly by running `pyenv --version`. If you see a version number, you are good to go.

## activate Virtual Environments
> Activate now the virtual environment by running `source venv/bin/activate` on macOS and Linux or `venv\Scripts\activate` on Windows. Check again.

## Dominique
npm install -g http-server (zusätzlich zu requirements.txt - achtung mit sudo)
start backend: uvicorn app:app --reload (wait until INFO:     Application startup complete.)
Frontend server starten: cd frontend dann http-server -p 8001

