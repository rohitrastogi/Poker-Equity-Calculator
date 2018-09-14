import sys, os

abs_path = os.path.abspath(os.path.dirname(__file__))
to_add = os.path.join(abs_path, "../src")
sys.path.append(to_add)