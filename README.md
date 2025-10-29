> This project is an independent effort and is neither affiliated with nor endorsed by the Python Software Foundation, CRIU, or React Flow.
> CRIU is licensed under GPLv2.

## Install (Ubuntu/Debian)

```bash
# mkdir ./trace-python/ && cd ./trace-python/
git clone https://github.com/herheliuk/trace-python . --depth 1
source env.sh
git clone https://github.com/herheliuk/criu-python-api ./criu-python-api/ --depth 1
source ./criu-python-api/install.sh
```

## Usage

```bash
source env.sh

sudo $(which python) -E settrace.py test.py
```
