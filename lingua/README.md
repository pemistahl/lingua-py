## How to build Lingua locally?

*Lingua* requires Python >= 3.8.
First [download](https://pypi.org/project/lingua-language-detector/#files)
the correct Python wheel for your platform on PyPI and put it in this directory.
Then go up to this project's root directory, create a virtualenv and install
the Python wheel with `pip`.

```
git clone https://github.com/pemistahl/lingua-py.git
cd lingua-py/lingua

# Put the downloaded wheel file in this directory

cd ../
python3 -m venv .venv
source .venv/bin/activate
pip install --find-links=lingua lingua-language-detector
```
