def environment_var(name):
    import os
    import sys
    if (name in os.environ.keys()):
      return os.environ[name]
    else:
      sys.stderr.write("Environment variable not set: {}\n".format(name))
      exit(1)
