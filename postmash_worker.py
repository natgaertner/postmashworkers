import boto.swf.layer2 as swf
from boto.dynamodb2.table import Table
import json
from uuid import uuid4
import logging, logging.handlers
rootLogger = logging.getLogger('postmash')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
rootLogger.addHandler(socketHandler)
logger = logging.getLogger('postmash.worker')

history = Table('history')

DOMAIN = 'PostMashDomain'
VERSION = '1.0'
TASKLIST = 'PostMashTasks'

class PostMashWorker(swf.ActivityWorker):

    domain = DOMAIN
    version = VERSION
    task_list = TASKLIST

    def run(self):
	logger.info('starting postmash worker')
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
