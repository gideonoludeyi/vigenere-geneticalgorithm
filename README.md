# Breaking Vigenère Ciphers /w Genetic Algorithm
Implementation of a genetic algorithm to break Vigenère ciphers

### Generated Data
See `data/` directory

### Build
1. Activate virtual environment
```sh
$ python -m venv .venv
$ source ./.venv/bin/activate
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
$ geneticalgorithm 8 -f attachments/sample.txt -s 3
```

#### Run experiment
```sh
$ experiment sample.json -o csv
$ experiment sample.json -v     # display all outputs (including decrypted text)
$ experiment sample.json -o tbl # requires tabulate package to be installed
```

#### Reproducing `data/data1.csv` and `data/data2.csv`
```sh
$ experiment data1.json -o csv > data/data1.csv
$ experiment data2.json -o csv > data/data2.csv
```

#### Changing Parameters (geneticalgorithm)
To get the list of parameters that can be changed, use:
```sh
$ geneticalgorithm --help
```

For example, to change the crossover algorithm to Order Crossover (OX):
```sh
$ geneticalgorithm 8 -f attachments/sample.txt -s 3 --crossover-alg=ox
```

Or the crossover and mutation rates:
```sh
$ geneticalgorithm 8 -f attachments/sample.txt -s 3 -c 0.8 -m 0.05
```

#### Changing Parameters (experiment)
To change the experiment configurations, edit one of `data1.json`, `data2.json`, or `sample.json`.
A sample configuration file looks like the following:
```json
{
  "pop_size": 50,
  "max_gen": 20,
  "elites": 2,
  "seeds": [2, 3],
  "runs": [
    {
      "file": "attachments/sample.txt",
      "key_length": 8,
      "crossover_algorithms": ["ux", "ox"],
      "mutation_algorithms": ["rx", "rc"],
      "selection_algorithms": ["tour3"],
      "rates": [
        {"crossover": 1.0, "mutation": 0.0},
        {"crossover": 0.9, "mutation": 0.1}
      ]
    }
  ]
}
```

You can run the experiment with this configuration via:
```sh
$ experiment /path/to/config.json
```

For the sample configuration above, this will run the GA for every combination of random seeds, crossover algorithms, mutation algorithms, selection algorithms, and crossover rates.
