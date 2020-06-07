name: python_38

on:
  pull_request:
    branches:
      - master
      - release/*

jobs:
  build:
    runs-on: ${{ matrix.os }}
    strategy:
      max-parallel: 4
      matrix:
        python-version: [3.8]
        os: [ubuntu-latest, windows-latest]

    steps:
      - uses: actions/checkout@v1
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v1
        with:
          python-version: ${{ matrix.python-version }}
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Install package
        run: |
          python setup.py install
      - name: Lint with flake8
        run: |
          pip install flake8
          flake8 --version
          # stop the build if there are Python syntax errors or undefined names
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
      - name: Test with pytest
        run: |
          pip install pytest
          pytest
