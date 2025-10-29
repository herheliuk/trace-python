#!/usr/bin/env python3

from sys import path, gettrace, settrace, exit as sys_exit
from os import chdir
from contextlib import contextmanager
from pathlib import Path

from utils.interactive_stepper import await_command

@contextmanager
def use_dir(target_dir: Path):
    original_dir = Path.cwd()
    target_dir = str(target_dir)
    if target_dir not in path:
        path.insert(0, target_dir)
        chdir(target_dir)
    try:
        yield
    finally:
        if target_dir in path:
            path.remove(target_dir)
            chdir(original_dir)
    
@contextmanager
def use_trace(trace_function):
    old_trace = gettrace()
    settrace(trace_function)
    try:
        yield
    finally:
        settrace(old_trace)

@contextmanager
def step_io(write_mem, criu, output_file: Path, interactive = None):
    if interactive:
        def print_step(text):
            print(text)
            
        def input_step(text):
            criu.dump(allow_overwrite=True)
            code, return_value = await_command(text)

            match code:
                case 'enter':
                    ...
                case 'backspace':
                    write_mem(str(criu._last_dump_number - 1))
                    sys_exit()
                case 'int':
                    write_mem(str(return_value))
                    sys_exit()
        
        def finalize():
            pass
    else:
        from io import StringIO
        buffer = StringIO()
        
        def print_step(text):
            buffer.write(text + '\n')
            
        def input_step(text):
            buffer.write(text + '\n')
            
        def finalize():
            output_file.write_bytes(buffer.getvalue().encode('utf-8'))
            buffer.close()

    try:
        yield print_step, input_step
    finally:
        finalize()
