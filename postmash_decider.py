# hello_decider.py
import boto.swf.layer2 as swf
import logging, logging.handlers
rootLogger = logging.getLogger('postmash')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',logging.handlers.DEFAULT_TCP_LOGGING_PORT)
rootLogger.addHandler(socketHandler)
logger = logging.getLogger('postmash.decider')

DOMAIN = 'PostMashDomain'
ACTIVITY = 'PostMashInsert'
VERSION = '1.0'
TASKLIST = 'PostMashTasks'

class PostMashDecider(swf.Decider):

    domain = DOMAIN
    task_list = TASKLIST
    version = VERSION

    def run(self):
	try:
            history = self.poll()
	except Exception as e:
	    logger.exception('exception polling for decider work')
	    raise e
        if 'events' in history:
            # Find workflow events not related to decision scheduling.
            workflow_events = [e for e in history['events']
                if not e['eventType'].startswith('Decision')]
            last_event = workflow_events[-1]

            decisions = swf.Layer1Decisions()
            if last_event['eventType'] == 'WorkflowExecutionStarted':
		try:
                	decisions.schedule_activity_task('insert_post', ACTIVITY, VERSION, task_list=TASKLIST,input = last_event['workflowExecutionStartedEventAttributes']['input'])
		except Exception as e:
		    logger.exception('exception scheduling insert_post activity')
            elif last_event['eventType'] == 'ActivityTaskCompleted':
		try:
                    decisions.complete_workflow_execution()
		except Exception as e:
		    logger.exception('exception closing workflow')
            self.complete(decisions=decisions)
	    logger.info("complete")
            return True

if __name__ == '__main__':
    logger.info('starting postmash decider')
    while True: PostMashDecider().run()
