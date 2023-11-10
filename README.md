# COSC 3P71 - A2
Genetic algorithm assignment

### Generated Data
See `data/` directory

### Build
1. Activate virtual environment
```sh
$ python -m venv .venv
```

2. Build project
```sh
$ .venv/bin/pip install build
$ .venv/bin/python -m build
```

3. Install project
```sh
$ .venv/bin/pip install dist/geneticalgorithm-0.1.0-py3-none-any.whl
$ .venv/bin/pip install tqdm tabulate # (optional) for progress bar and formatting output
```

### Usage
#### Run Genetic Algorithm
```sh
$ .venv/bin/geneticalgorithm 8 -f attachments/sample.txt -s 3
```

#### Run experiment
```sh
$ .venv/bin/experiment sample.json -o csv
$ .venv/bin/experiment sample.json -v     # display all outputs (including decrypted text)
$ .venv/bin/experiment sample.json -o tbl # requires tabulate package to be installed
```

#### Reproducing data1.csv and data2.csv
```sh
$ .venv/bin/experiment data1.json -o csv > data1.csv
$ .venv/bin/experiment data2.json -o csv > data2.csv
```

#### Changing Parameters (geneticalgorithm)
To get the list of parameters that can be changed, use:
```sh
$ .venv/bin/geneticalgorithm --help
```

For example, to change the crossover algorithm to Order Crossover (OX):
```sh
$ .venv/bin/geneticalgorithm 8 -f attachments/sample.txt -s 3 --crossover-alg=ox
```

Or the crossover and mutation rates:
```sh
$ .venv/bin/geneticalgorithm 8 -f attachments/sample.txt -s 3 -c 0.8 -m 0.05
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
$ .venv/bin/experiment /path/to/config.json
```

For the sample configuration above, this will run the GA for every combination of random seeds, crossover algorithms, mutation algorithms, selection algorithms, and crossover rates.
