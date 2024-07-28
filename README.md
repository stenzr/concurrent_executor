# Spawn Parallel Instances

Spawn Parallel Instances is a Python package that allows you to run parrallel instances of the same script. It supports loading environment variables from a YAML file and allows specifying the Python interpreter to use.

## Features

- Run multiple instances of a script concurrently.
- Load environment variables from a YAML file.
- Specify the Python interpreter to use.
- Log output for each process with unique identifiers.

## Installation

You can install the package using pip:

```sh
pip install spawn_parallel_instances
```

## Alternate Installation

You can install it from source

```sh
git clone https://github.com/stenzr/spawn_parallel_instances

cd spawn_parallel_instances

python -m pip install .

```

## Usage

To use the concurrent executor, run the following command:

```sh
spawn_parallel_instances <script_name> --processes <num_processes> --env_file <env_file> --python_interpreter <interpreter>
```

### Arguments

- <script_name>: The Python script to run (positional argument).
- --processes: Number of processes to spawn (default: 1).
- --env_file: YAML file containing environment variables (default: env_variables.yml).
- --python_interpreter: Python interpreter to use (default: python3.11).


### Example
Assuming you have a script called [`tests/sample/test_script.py`](tests/sample/test_script.py) and an environment file [`tests/sample/config.yml`](tests/sample/config.yml), you can run:

```sh
spawn_parallel_instances tests/sample/test_script.py --processes 3 --env_file tests/sample/config.yml --python_interpreter python3.9
```

### Environment Variables

Environment variables should be defined in a YAML file. For example:

```yaml
FOO: bar
BAZ: qux
```

The above YAML file can be used with the --env_file argument to set environment variables for the script.

### Logging
Each process will log its output to a file with a unique identifier. The log files are named based on the script name, process number, and a unique UUID.

## Development
To set up a development environment:

### Clone the repository:

```sh
git clone https://github.com/stenzr/spawn_parallel_instances
cd spawn_parallel_instances
```

### Create a virtual environment and activate it:

```sh
Copy code
python3.9 -m venv venv
source venv/bin/activate
```

### Install the package in editable mode with development dependencies:

```sh
Copy code
pip install -e .[test]
```

## Contributing
Contributions are welcome! Please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes.
- Write tests for your changes.
- Ensure all tests pass.
- Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


