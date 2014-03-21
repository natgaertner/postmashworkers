import boto.swf.layer2 as swf
from boto.dynamodb2.table import Table
import json
from uuid import uuid4
import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('/var/log/postmash/postmash_worker.log')
handler.setLevel(logging.DEBUG)
logger = logging.getLogger("postmash_worker")
logger.addHandler(handler)
history = Table('history')

DOMAIN = 'PostMashDomain'
VERSION = '1.0'
TASKLIST = 'PostMashTasks'

class PostMashWorker(swf.ActivityWorker):

    domain = DOMAIN
    version = VERSION
    task_list = TASKLIST

    def run(self):
	try:
            activity_task = self.poll()
	except Exception as e:
	    logger.warning(e)
	    raise e
        if 'activityId' in activity_task:
	    try:
		data = json.loads(activity_task['input'])
		data.update({'uuid':uuid4().hex})
		history.put_item(data=data)
		logger.info('inserted {data}'.format(json.dumps(data)))
		self.complete()
	    except Exception as e:
		logger.warning(e)
            return True

if __name__ == '__main__':
    while True: PostMashWorker().run()
