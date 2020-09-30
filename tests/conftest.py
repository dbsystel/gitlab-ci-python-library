import os
import inspect
import pathlib

import yaml


def check(output: str) -> bool:
    yaml_output = yaml.safe_dump(output, default_flow_style=False, sort_keys=False)
    # inspired by https://stackoverflow.com/a/60297932
    caller_file_path, caller_file_name = os.path.split(os.path.abspath(inspect.stack()[1].filename))
    caller_file_name = os.path.splitext(caller_file_name)[0]
    caller_function_name = inspect.stack()[1].function
    compare_file = f"{caller_file_path}/comparison_files/{caller_file_name}_{caller_function_name}.yml"

    if os.getenv("UPDATE_TEST_OUTPUT", "false").lower() == "true":
        pathlib.Path(os.path.split(compare_file)[0]).mkdir(parents=True, exist_ok=True)
        with open(compare_file, "w") as outfile:
            outfile.write(yaml_output)
    else:
        with open(compare_file, "r") as infile:
            assert yaml_output == infile.read()
