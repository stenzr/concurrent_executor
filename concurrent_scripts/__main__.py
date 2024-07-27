import argparse
from datetime import datetime
import subprocess
import os
import yaml
import traceback
import uuid

class ScriptRunner:
    def __init__(self):
        # Parse command-line arguments
        self.args = self.parse_arguments()
        self.script_name = self.args.script
        self.number_of_processes = self.args.processes
        self.python_interpreter = self.args.python_interpreter

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
        parser.add_argument("--processes", help="number of processes to spawn", type=int, default=1)
        parser.add_argument("--script", help="python script to run", type=str, default="")
        parser.add_argument("--env_file", help="YAML file containing environment variables", type=str, default="env_variables.yml")
        parser.add_argument("--python_interpreter", help="Python interpreter to use", type=str, default="python3.11")
        return parser.parse_args()

    def get_log_file_name(self):
        # Extract the log file name from the script name
        log_file = self.script_name.split('/')[-1]
        log_file = log_file.split('.')[0]
        return log_file

    def read_env_variables(self):
        try:
            # Read environment variables from the YAML file
            with open(self.env_file, 'r') as f:
                env_variables = yaml.safe_load(f)
            print("env_variables", env_variables)
            return env_variables
        except Exception as e:
            print("Error reading environment variables:", e)
            traceback.print_tb(e.__traceback__)
            exit(1)

    def construct_command(self, env_list, instance_number):
        # Construct the command to be executed for each process
        base_command = f'{self.python_interpreter} -u {self.script_name}'
        command = f'{env_list} {base_command} >> {self.log_file}_{instance_number}_{uuid.uuid4().hex[:6]}.log 2>&1'
        return command

    def run_processes(self, env_list):
        chk_point1 = datetime.now()
        try:
            # Spawn the specified number of processes
            for instance_number in range(self.number_of_processes):
                command = self.construct_command(env_list, instance_number)
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
        
        # Run the processes with the constructed environment variable list
        self.run_processes(env_list)

if __name__ == '__main__':
    ScriptRunner().run()
