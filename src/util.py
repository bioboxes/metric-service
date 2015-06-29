def environment_var(name):
    import os
    import sys
    if (name in os.environ.keys()):
      return os.environ[name]
    else:
      sys.stderr.write("Environment variable not set: {}\n".format(name))
      exit(1)

def sdb_domain():
    import boto.sdb
    conn = boto.sdb.connect_to_region('us-west-1',
      aws_access_key_id     = environment_var('AWS_ACCESS_KEY'),
      aws_secret_access_key = environment_var('AWS_SECRET_KEY'))
    return conn.get_domain(environment_var('AWS_SIMPLEDB_NAME'))

def fetch_all_metrics():
    return sdb_domain().select(
        'select * from `{}`'.format(environment_var('AWS_SIMPLEDB_NAME')))
