#!/usr/bin/bash
rm -rf /tmp/migration/*.sst
../../build/cluster-balance --port=40001
rm -rf /tmp/migration/*.sst
