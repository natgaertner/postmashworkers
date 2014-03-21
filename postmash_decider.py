# hello_decider.py
import boto.swf.layer2 as swf
import logging
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler('/var/log/postmash/postmash_decider.log')
handler.setLevel(logging.DEBUG)
logger = logging.getLogger("postmash_decider")
logger.addHandler(handler)

DOMAIN = 'PostMashDomain'
ACTIVITY = 'PostMashInsert'
VERSION = '1.0'
TASKLIST = 'PostMashTasks'

class PostMashDecider(swf.Decider):

    domain = DOMAIN
    task_list = TASKLIST
    version = VERSION

    def run(self):
        history = self.poll()
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
		    logger.warning(e)
            elif last_event['eventType'] == 'ActivityTaskCompleted':
		try:
                    decisions.complete_workflow_execution()
		except Exception as e:
		    logger.warning(e)
            self.complete(decisions=decisions)
	    logger.info("complete")
            return True

if __name__ == '__main__':
    while True: PostMashDecider().run()
