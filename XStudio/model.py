from XStudio.utils import *
import os


class Model():
    def __init__(self) -> None:
        pass


    def exec_tool(self, tool_name, config, params):
        origin_cmd = config['cmd']
        cmd_string = origin_cmd % tuple(params)
        print(cmd_string)
        os.system(cmd_string)