import subprocess
import os

def call_cupp(args):
    cupp_path = os.path.abspath("./assets/bin/cupp/cupp_master/cupp.py")
    subprocess.run([cupp_path] + args, check=True)

if __name__ == "__main__":
    call_cupp(["-i"])  # Example usage: call_cupp(["-i"])
