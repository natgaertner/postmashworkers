#!/bin/bash
(python /var/postmashworkers/log_record_stream_handler.py &)
for i in `seq 1 2` ; do
    (python /var/postmashworkers/postmash_decider.py &)
done
for i in `seq 1 5` ; do
    (python /var/postmashworkers/postmash_worker.py &)
done
