#!/usr/bin/env python
# -*- coding: utf-8 -*-

""":Mod: fabfile

:Synopsis:
    Fabric script to interact with remote host(s) - see below for an example
    $ fab data_query -I -i /home/<user>/.ssh/id_rsa -H kimberlite.lternet.edu

:Author:
    servilla
  
:Created:
    10/6/16
"""
from __future__ import print_function

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s (%(name)s): %(message)s',
                    datefmt='%Y-%m-%d% H:%M:%S%z')
logging.getLogger('').setLevel(logging.WARN)
logger = logging.getLogger('fabfile')

from fabric.api import *

def data_query():
    print(env.user)
    sql = 'psql -U pasta -d pasta -h localhost -c "copy (select ' \
          'resource_location,package_id,' \
          'entity_id,sha1_checksum,resource_size from ' \
          'datapackagemanager.resource_registry where resource_type=\'data\') to stdout with csv" > /tmp/data_entities.csv'
    run(sql)
    get('/tmp/data_entities.csv')

def main():
    return 0


if __name__ == "__main__":
    main()