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
VERSION = '1.1'
TASKLIST = 'PostMashTasks'

class PostMashWorker(swf.ActivityWorker):

    domain = DOMAIN
    version = VERSION
    task_list = TASKLIST

    def run(self):
	try:
            activity_task = self.poll()
	except Exception as e:
	    logger.exception('exception polling for data')
	    raise e
        if 'activityId' in activity_task:
	    try:
		data = json.loads(activity_task['input'])
		data.update({'uuid':uuid4().hex})
		history.put_item(data=data)
		logger.info('inserted {data}'.format(data=json.dumps(data)))
		self.complete()
	    except Exception as e:
		logger.exception('exception inserting data')
		self.fail()
            return True

if __name__ == '__main__':
    logger.info('starting postmash worker')
    while True: PostMashWorker().run()
