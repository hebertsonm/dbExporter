import subprocess
import os
import ntpath

# execute system command
def popen_command(command):
    get_output_aux =  subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout
    get_output =  get_output_aux.read()

    # return the command output
    return get_output.decode()

def call_command(command):
    return subprocess.call(command, shell=True, stdout=subprocess.PIPE)

def basename(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)