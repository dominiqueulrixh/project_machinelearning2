# RAG-week1

## TL;DR

- Install pyenv (see [Setup](### Setup))
- Install Python 3.11.4 with pyenv `pyenv install 3.11.4`
- Switch your local Python version to 3.11.4 with `pyenv local 3.11.4`
- Create a virtual environment with `python -m venv venv`
- Activate the virtual environment with `source venv/bin/activate` on macOS and Linux or `venv\Scripts\activate` on Windows
- Install the required packages with `pip install -r requirements.txt`

Start with your first RAG project by following the instructions in the [Jupyter Notebook](./rag-week1.ipynb).

## Add-on: Managing multiple Python versions with pyenv

![Python environment (https://xkcd.com/1987/)](.doc/image.png)

### Problem

Some libraries are only compatible with specific Python versions. You may have to work with multiple Python versions on the same machine. You may also want to test your code with different Python versions.

### Solution and why now?

We have to find a way to manage multiple Python versions on the same machine. We also have to find a way to switch between these versions easily. This is especially important if you work with different projects that require different Python versions. For this course it is not guarantueed that we will work with the latest Python version. We will use Python 3.10 for this course, but it is not guaranteed that all libraries we use are compatible with this version. We may have to switch to a different version for other projects.

We suggest to use `pyenv` for this purpose. It is a simple and lightweight solution to manage multiple Python versions on the same machine.

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

| Command | Description |
|---------|-------------|
| commands | List all available pyenv commands |
| local | Set or show the local application-specific Python version |
| global | Set or show the global Python version |
| shell | Set or show the shell-specific Python version |
| install | Install 1 or more versions of Python |
| uninstall | Uninstall 1 or more versions of Python |
| update | Update the cached version DB |
| rehash | Rehash pyenv shims (run this after switching Python versions) |
| vname | Show the current Python version |
| version | Show the current Python version and its origin |
| version-name | Show the current Python version |
| versions | List all Python versions available to pyenv |

## Add-on Virtual Environments

### Problem

Python is not great with dependacy management. Simply using `pip install` is going to place and replace all packages in your base python installation. This leads to:

- For macOS and Linux this leads to pollution of your operating system's global Python installation. It can have unexpected side-effects on crucial tasks of your operating system.
- Vice-versa: if you update your operating system, the packages you have installed might be removed or up-/downgraded
- Different projects might require different versions of an external library or even a different Python version.
- Reproducibility is more difficult. Which packages are truly necessary to run a specific project? Which ones are not?
- You may not even have the rights to install packages on the host Python version.

### Solution and why now?

Virtual Environments can mitigate above-mentioned issues. It may seem like an overhead to begin with, but it saves a lot of grief in the future.

We are going to work with bleeding-edge technologies in this course. Machine Learning libraries are still novel, developing rapidly, and often lack backwards compatbility.

The tutorial that we have prepared today will work with the pinned Python versions and dependencies, it may work with the latest version and it will likely not work with prior versions of langchain and its dependencies.

Keeping up with the latest development in a framework or package in the course of project can create new overhead and may not always be necessary. Exceptions: Bug fix of required functionality, fixes of security issues, new feature that you have been waiting for...

## Structure of a Python Virtal Environment

You may not be convinced yet that you want to work with Python virtual environments, but let's assume you are =)

Generally speaking, a Python environment is simply a folder structure that contains everything you need to run an isolated, lightweight Python environment.

When you use the built-in `venv` module, Python creates a new folder structure with copies or symbolic links of the python executable files into this folder structure.

> Let's create a virtual environment for this notebook now. Run `python -m venv venv` and make sure you are in the folder in which you inspect this project.

Inspect the folder you have just created.

- **bin/** is the folder that cointains the exectuble files of your Python environment. Typically Python itself, Pip, and the related symbolic links. You also find the activation script for your virtual environment. The type of the activation script depends on the type of shell you use.
- **include/** will be empty for now and may contain C header files later for packages that depend on C extensions (common for libraries that try to be performant)
- **lib/** is the folder that will eventualy contain the most files. In `site-packages` you will install all the external packages you need for your application. The only pre-installed packages are pip and setuptools.
- **lib64/** exists in Linux-bases systems for compatibility reasons. On Linux some packages will be either installed in `lib` or `lib64`.
- **pyvenv.cfg** is the configuration file for your virtual environment. It contains key-value pairs that define which Python interpreter and which site-packages directory the current Python session will use.

## How does it work then?

We have now a copy of the structure of the system wide Python installation. The Python interpreter always checks for a `pyvenv.cfg`. If it finds one, it will use the configuration defined in this file. If it does not find one, it will use the system wide Python installation.

To make sure that virtual environments are a lightweight solution, the Python interpreter does not copy the whole Python installation. It has pointers to the system wide Python installation on which you based your virtual environment. This means that you can have multiple virtual environments with different Python versions on the same machine without having to store the whole Python installation multiple times.

The virtual environment also modifies the PYTHONPATH environment variable. This is the variable that the Python interpreter uses to find the packages you import in your code. The virtual environment will add its `site-packages` directory to the PYTHONPATH.

> Lets try it out.

```python
>>> import sys
>>> from pprint import pp
>>> pp(sys.path)
['',
 '/usr/local/lib/python310.zip',
 '/usr/local/lib/python3.10',
 '/usr/local/lib/python3.10/lib-dynload',
 '/usr/local/lib/python3.10/site-packages']
```

> Activate now the virtual environment by running `source venv/bin/activate` on macOS and Linux or `venv\Scripts\activate` on Windows. Check again.

```python
>>> import sys
>>> from pprint import pp
>>> pp(sys.path)
['',
 '/usr/local/lib/python310.zip',
 '/usr/local/lib/python3.10',
 '/usr/local/lib/python3.10/lib-dynload',
 '/home/name/path/to/venv/lib/python3.10/site-packages']
```

Furthermore, it changes your shell PATH variable on activation. This means that the Python interpreter and the pip executable in your virtual environment will be used instead of the system wide ones.

Theoretically, you can also use the virtual environment without activating by using the full path to the Python interpreter or pip executable. While you mostly will activate it in practice, the knowing that you can use the absolute path can help if you run a virtual environemt in a Docker container for example.

### Some icing on the cake

You can also create a virtual environment that shows a more telling name in the terminal by adding a `--prompt` flag to the `python -m venv` command. This is especially useful if you work with multiple virtual environments at the same time.

Example: `python -m venv venv --prompt=rag-week1`

Further and more in-depth reading: [Python Virtual Environments: A Primer](https://realpython.com/python-virtual-environments-a-primer/)




npm install -g http-server (zusätzlich zu requirements.txt - achtung mit sudo)
start backend: uvicorn app:app --reload (wait until INFO:     Application startup complete.)
Frontend server starten: cd frontend dann http-server -p 8001

