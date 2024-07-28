# Spawn Parallel Instances

[![PyPI](https://img.shields.io/pypi/v/spawn-parallel-instances)](https://pypi.org/project/spawn-parallel-instances/)

Spawn Parallel Instances is a versatile tool designed to facilitate running multiple instances of various types of scripts with customizable environment variables and arguments. By leveraging its command-line options, you can efficiently manage and execute scripts in parallel, making it an essential tool for developers and system administrators.

## Features

- Run multiple instances of a script concurrently.
- Load environment variables from a YAML file.
- Pass arguments to each process via a json file
- Specify the interpreter to use.
- Log output for each process with unique identifiers.

## Installation

You can install the package using pip:

```sh
pip install spawn_parallel_instances
```

## Usage

To use the concurrent executor, run the following command:

```sh
spawn_parallel_instances <script_name> --processes <num_processes> --env_file <env_file> --interpreter <interpreter> --script-type <script_type>
```

## Arguments

### Command-Line Arguments

The `ScriptRunner` accepts the following command-line arguments:

1. **script** (positional, required):
   - **Description:** The script to run.
   - **Type:** `str`
   - **Example:** `my_script.py` or `my_script.js`

2. **--processes** (optional):
   - **Description:** Number of processes to spawn.
   - **Type:** `int`
   - **Default:** `1`
   - **Example:** `--processes 4`

3. **--env-file** (optional):
   - **Description:** YAML file containing environment variables.
   - **Type:** `str`
   - **Default:** `env_variables.yml`
   - **Example:** `--env-file config.yml`

4. **--script-type** (optional):
   - **Description:** Script type (either `python`, `nodejs`, `go`).
   - **Type:** `str`
   - **Choices:** `["python", "nodejs", "go"]`
   - **Default:** `python`
   - **Example:** `--script-type nodejs`

5. **--interpreter** (optional):
   - **Description:** Interpreter to use (Python interpreter or node).
   - **Type:** `str`
   - **Default:** If not specified, defaults to `python3.11` for Python scripts or `node` for Node.js scripts or `go run` for go.
   - **Example:** `--interpreter python3.8` or `--interpreter node`

6. **--script-args-file** (optional):
   - **Description:** JSON file containing script arguments for each process.
   - **Type:** `str`
   - **Default:** `""`
   - **Example:** `--script-args-file args.json`

7. **--script-args** (optional):
   - **Description:** Arguments to pass to each script instance, comma-separated for each instance.
   - **Type:** `str`
   - **Default:** `""`
   - **Example:** `--script-args "arg1,arg2,arg3"`

### Environment Variables

Environment variables should be defined in a YAML file. For example:

```yaml
FOO: bar
BAZ: qux
```

The above YAML file can be used with the --env_file argument to set environment variables for the script.

### Arguments

The JSON file specified with `--script-args-file` should contain a list of argument sets, one for each process instance. The number of argument sets in the JSON file must match the number of processes specified.

#### Json file format

```json
[
    ["arg1", "arg2", "arg3"],
    ["arg4", "arg5", "arg6"],
    ["arg7", "arg8", "arg9"]
]
```

### Logging
Each process will log its output to a file with a unique identifier. The log files are named based on the script name, process number, and a unique UUID.

### Example
Assuming you have a script called [`tests/sample/test_script.py`](tests/sample/test_script.py) and an environment file [`tests/sample/config.yml`](tests/sample/config.yml), you can run:

```sh
spawn_parallel_instances tests/sample/test_script.py --processes 3 --env_file tests/sample/config.yml --script-type python --interpreter python3.9
```
## Use Cases

### Running a Python Script with Default Settings:

```bash
spawn_parallel_instances my_script.py
```

### Running a Node.js Script with 4 Processes:

```bash
spawn_parallel_instances my_script.js --script-type nodejs --processes 4
```

### Running a Go Script with Environment Variables:

```bash
spawn_parallel_instances my_script.go --script-type go --env-file my_env.yml
```

### Running a Python Script with Specific Interpreter and Arguments:

```bash
spawn_parallel_instances my_script.py --interpreter python3.9 --script-args-file args.json
```
### Running a Python Script with Direct Arguments:

```bash
spawn_parallel_instances my_script.py --script-args "arg1,arg2,arg3,arg4"
```

## Troubleshooting

If you encounter issues while running ScriptRunner, consider the following tips:

### Interpreter Not Found:

Ensure that the interpreter specified in --interpreter or derived from --script-type is correctly installed and available in your PATH.

### Incorrect JSON Format:

Verify that the JSON file used for --script-args-file is correctly formatted as a list of lists. Each inner list should correspond to the arguments for one process instance.

### Environment Variables Not Loaded:

Check if the YAML file specified with --env-file exists and is correctly formatted. Ensure it contains valid key-value pairs.

### Script Execution Errors:

Review the log files generated for each process to identify any specific errors related to script execution.


## Contributing
Contributions are welcome! Please follow these steps:

- Fork the repository.
- Create a new branch for your feature or bug fix.
- Make your changes.
- Write tests for your changes.
- Ensure all tests pass.
- Submit a pull request.

### Development
To set up a development environment:

#### Clone the repository:

```sh
git clone https://github.com/stenzr/spawn_parallel_instances
cd spawn_parallel_instances
```

#### Create a virtual environment and activate it:

```sh
Copy code
python3.9 -m venv venv
source venv/bin/activate
```

#### Install the package in editable mode with development dependencies:

```sh
Copy code
pip install -e .[test]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


