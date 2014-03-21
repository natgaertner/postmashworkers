#!/bin/bash
for i in `seq 1 2` ; do
    (python /var/postmash/postmash_decider.py &)
done
for i in `seq 1 5` ; do
    (python /var/postmash/postmash_worker.py &)
done
