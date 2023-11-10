# COSC 3P71 - A2
Genetic algorithm assignment

### attachments/sample.txt

```
xbwdesmhihslwhkktefvktkktcwfpiibihwmosfilojvooegvefwnochsuuspsureifakbnlalzsrsroiejwzgfpjczldokrceoahzshpbdwpcjstacgbarfwifwohylckafckzwwomlalghrtafchfetcgfpfrgxclwzocdctmjebx
```

Key: `password`

### Building
1. Activate virtual environment
```sh
$ python -m venv .venv
$ source .venv/bin/activate
```

2. Build project
```sh
$ pip install build
$ python -m build
```

3. Install project
```sh
$ pip install dist/geneticalgorithm-0.1.0-py3-none-any.whl
$ pip install tqdm tabulate # (optional) for progress bar and formatting output
```

### Usage
#### Run Genetic Algorithm
```sh
$ .venv/bin/geneticalgorithm --help
$ .venv/bin/geneticalgorithm 8 -f attachments/sample.txt -s 3
Best Solution: pqsswkqp
Best Fitness: 0.30067272727272726
```

#### Run experiment
```sh
$ .venv/bin/experiment --help
$ .venv/bin/experiment sample.json -o csv
$ .venv/bin/experiment sample.json -v     # display all outputs (including decrypted text)
$ .venv/bin/experiment sample.json -o tbl # requires tabulate package to be installed
```
