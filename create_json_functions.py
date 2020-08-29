#!/bin/env python
import json
import sys
import glob

def create_function_header(name, data_vars=None):
    name = name.replace(':', '_')
    name = name.replace('.', '_')
    name = name.replace('mycroft_', '')
    if data_vars != None:
        local_data_vars = data_vars.copy()
        new_args = local_data_vars.pop()
        if len(local_data_vars) != 0:
           new_args = "=None ,".join(local_data_vars) 
        else:
           new_args = f"{new_args}=None"
        function_header = f"def {name}(self, {new_args}):"
    else: 
        function_header = f"def {name}(self):"
    return function_header

def create_data_dict(name, data_vars=None):
    message_block = []
    if data_vars != None:
        message_block.append(" message = \"{'type': '%s','data': {" %(name))
        local_data_vars = data_vars.copy()
        data_strs = [f"                           '{var}':{var}" for var in local_data_vars]
        for var in data_strs:
           message_block.append(f'{var},')
        message_block[-1] = message_block[-1].rstrip(',')
        message_block.append("                           }")
    else:
        message_block.append("message = \"{'type': '%s'\"" %(name))
    return message_block


def create_send_block():
    send_block = ["send_status = self._send(message)", "return send_status"] 
    return send_block

if __name__ == '__main__':
    newlines = []
    json_dir = glob.glob(sys.argv[1])
    for json_file in json_dir:
       if ".json" in json_file:
           with open(json_file, 'r') as fh:
              json_message = json.load(fh)
           name = json_message['type']
           try:
              data_vars = [data_var for data_var in json_message['data']]
           except KeyError:
               data_vars = None
           function_header = create_function_header(name, data_vars)
           data_dict_lines = create_data_dict(name, data_vars)
           send_block_lines = create_send_block()
           newlines.append(f'{function_header}')
           for line in data_dict_lines:
               newlines.append(f'   {line}')
           for line in send_block_lines:
               newlines.append(f'    {line}')
           newlines.append('\n')

    with open("./mycroft_websocket_template.py", 'r') as fh:
       boiler_plate = fh.read()
    with open("./mycroft_websocket.py", 'w') as fh:
       fh.write(boiler_plate)
       fh.write(f'\n### The following was auto generated by {__name__} ###')
       for line in newlines:
          fh.write(f'\n    {line}')

