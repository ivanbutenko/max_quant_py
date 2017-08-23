import subprocess
from typing import List, Iterable


def execute(cmd: List[str])->Iterable[str]:
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line.strip()
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def run_maxquant(max_quant_cmd: str, options: List[str])->Iterable[str]:
    args = ['mono', max_quant_cmd] + options
    return execute(args)


def echo_stdout(outs: Iterable[str]):
    for line in outs:
        print(line)
