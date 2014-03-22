#!/bin/bash
source /var/postmashenv/bin/activate
(python /var/postmashenv/postmashworkers/log_record_stream_handler.py &)
for i in `seq 1 2` ; do
    (python /var/postmashenv/postmashworkers/postmash_decider.py &)
done
for i in `seq 1 5` ; do
    (python /var/postmashenv/postmashworkers/postmash_worker.py &)
done
