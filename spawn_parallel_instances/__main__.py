import argparse
from datetime import datetime
import subprocess
import os
import yaml
import traceback
import uuid
import json

class ScriptRunner:
    def __init__(self):
        # Parse command-line arguments
        self.args = self.parse_arguments()
        self.script_name = self.args.script
        self.number_of_processes = self.args.processes
        self.script_type = self.args.script_type
        self.interpreter = self.get_interpreter()
        self.script_args_file = self.args.script_args_file
        self.script_args = self.args.script_args


        # Get the absolute path of the folder containing the script
        self.script_folder = os.path.dirname(os.path.abspath(__file__)) + "/"
        # Append the folder path to the user-provided YAML file name
        self.env_file = os.path.join(self.script_folder, self.args.env_file)
        # Get the log file name based on the script name
        self.log_file = self.get_log_file_name()

        self.child_processes = []
        self.child_process_status_map = {}

    def parse_arguments(self):
        # Define and parse command-line arguments
        parser = argparse.ArgumentParser()

        # Positional argument for the script to run
        parser.add_argument(
            "script",
            help="Script to run (Python or Node.js)",
            type=str
        )

        # Optional argument to specify the number of processes to spawn
        parser.add_argument(
            "--processes",
            help="Number of processes to spawn",
            type=int,
            default=1
        )

        # Optional argument to specify the YAML file containing environment variables
        parser.add_argument(
            "--env-file",
            help="YAML file containing environment variables",
            type=str,
            default="env_variables.yml"
        )

        # Optional argument to specify the script type (python or nodejs)
        parser.add_argument(
            "--script-type",
            help="Script type (python or nodejs)",
            type=str,
            choices=["python", "nodejs", "go"],
            default="python"
        )

        # Optional argument to specify the interpreter to use (Python interpreter or node)
        parser.add_argument(
            "--interpreter",
            help="Interpreter to use (Python interpreter or node)",
            type=str,
            default=""
        )
        
        # Optional argument to specify the JSON file containing script arguments for each process
        parser.add_argument(
            "--script-args-file",
            help="JSON file containing script arguments for each process",
            type=str,
            default=""
        )

        # Optional argument to specify arguments for each process directly
        parser.add_argument(
            "--script-args",
            help="Arguments to pass to each script instance, comma-separated for each instance",
            type=str,
            default=""
        )

        return parser.parse_args()
    
    def get_interpreter(self):
        if self.args.interpreter:
            return self.args.interpreter
        if self.script_type == "python":
            return "python3.11"
        elif self.script_type == "nodejs":
            return "node"
        elif self.script_type == "go":
            return "go run"
        else:
            raise ValueError(f"Unsupported script type: {self.script_type}")

    def get_log_file_name(self):
        # Extract the log file name from the script name
        log_file = os.path.basename(self.script_name).split('.')[0]
        return log_file

    def read_env_variables(self):
        if not os.path.isfile(self.env_file):
            print(f"Environment file {self.env_file} does not exist.")
            return {}  # Return an empty dictionary if the file does not exist

        try:
            # Read environment variables from the YAML file
            with open(self.env_file, 'r') as f:
                env_variables = yaml.safe_load(f) or {}
            print("env_variables", env_variables)
            return env_variables
        except Exception as e:
            print("Error reading environment variables:", e)
            traceback.print_tb(e.__traceback__)
            return {}  # Return an empty dictionary in case of an error
        
    def is_interpreter_available(self):
        try:
            # Attempt to run the interpreter with the `--version` flag to check its availability
            result = subprocess.run(self.interpreter.split() + ['--version'], capture_output=True, text=True, check=True)
            print(f"{self.interpreter} is available.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error checking interpreter: {e}")
            return False
        except FileNotFoundError:
            print(f"Interpreter {self.interpreter} not found.")
            return False
        
    def read_script_args(self):
        if self.script_args_file:
            if not os.path.isfile(self.script_args_file):
                print(f"Script arguments file {self.script_args_file} does not exist.")
                return [""] * self.number_of_processes

            try:
                with open(self.script_args_file, 'r') as f:
                    script_args = json.load(f)
                    
                if not isinstance(script_args, list):
                    raise ValueError("Script arguments file must contain a list of arguments.")
                
                if len(script_args) != self.number_of_processes:
                    raise ValueError("The number of argument sets in the JSON file must match the number of processes.")
                
                return script_args
            
            except Exception as e:
                print(f"Error reading script arguments file: {e}")
                traceback.print_tb(e.__traceback__)
                
                return [""] * self.number_of_processes
            
        elif self.script_args:
            script_args = self.script_args.split(",")
            return [script_args] * self.number_of_processes
        
        else:
            return [""] * self.number_of_processes

    def construct_command(self, env_list, instance_number, script_args):
        # Check if the interpreter is available
        if not self.is_interpreter_available():
            raise RuntimeError(f"Interpreter {self.interpreter} is not available.")
        
        # Construct the command to be executed for each process
        if self.script_type == "python":
            base_command = f'{self.interpreter} -u {self.script_name}'
        elif self.script_type in ["nodejs", "go"]:
            base_command = f'{self.interpreter} {self.script_name}'
        else:
            raise ValueError(f"Unsupported script type: {self.script_type}")

        # Add script arguments
        if script_args:
            base_command += ' ' + ' '.join(script_args)

        command = f'{env_list} {base_command} >> {self.log_file}_{instance_number}_{uuid.uuid4().hex[:6]}.log 2>&1'
        return command
        
    def run_processes(self, env_list, script_args_list):
        chk_point1 = datetime.now()
        try:
            # Spawn the specified number of processes
            for instance_number in range(self.number_of_processes):
                script_args = script_args_list[instance_number]
                command = self.construct_command(env_list, instance_number, script_args)
                try:
                    print("executing-command", instance_number, command, datetime.now())
                    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    self.child_processes.append(process)
                    self.child_process_status_map[str(instance_number)] = False
                except Exception as e:
                    print("failure-while-executing-command", instance_number, command, str(e), datetime.now())
                    continue
        except Exception as e:
            print("Error:", e)
            traceback.print_tb(e.__traceback__)
            exit(1)
        chk_point2 = datetime.now()
        print("initiated-child-processes", "time-taken", (chk_point2 - chk_point1).total_seconds(), datetime.now())
        self.wait_for_processes(chk_point2)

    def wait_for_processes(self, chk_point2):
        # Wait for all child processes to finish
        print("waiting-for-child-processes-to-finish", len(self.child_processes), datetime.now())
        while not all(self.child_process_status_map.values()):
            for index, cp in enumerate(self.child_processes):
                if not self.child_process_status_map.get(str(index)):
                    try:
                        cp.wait(timeout=10)
                        chk_point4 = datetime.now()
                        self.child_process_status_map[str(index)] = True
                        print("execution-completed", cp.args, "finished-after", (chk_point4 - chk_point2).total_seconds(), datetime.now())
                    except Exception as e:
                        continue
        chk_point5 = datetime.now()
        print("all-child-processes-finished", "time-taken", (chk_point5 - chk_point2).total_seconds(), datetime.now())
    
    def run(self):
        print("script folder", self.script_folder)
        print("script", self.script_name, "processes", self.number_of_processes)
        
        # Read and print environment variables
        env_variables = self.read_env_variables()
        env_list = " ".join([f"{key.upper()}={value}" if isinstance(value, str) else f"{key.upper()}={str(value)}" for key, value in env_variables.items()])
        print("env_list", env_list)

        # Read script arguments
        script_args_list = self.read_script_args()
        print("script_args_list", script_args_list)
        
        # Run the processes with the constructed environment variable list and script arguments
        self.run_processes(env_list, script_args_list)

def main():
    ScriptRunner().run()

    
if __name__ == '__main__':
    main()
