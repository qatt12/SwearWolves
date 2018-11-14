
import events
from events import event_maker

event_maker.make_entry('trace', 'test1', 'DEBUG', 'scratch', False, True, 'DEBUG', "test1")
event_maker.make_entry('trace', 'test2', 'DEBUG', 'scratch', False, True, 'DEBUG', "test2")
event_maker.make_entry('trace', 'test2', 'DEBUG', 'scratch', False, True, 'waffle', "test2")
print("first flush")
event_maker.flush_trace_buffer(True)
print("second flush, should block waffle")
event_maker.flush_trace_buffer(True, block_terms=['waffle'])
print("third flush, should only allow test2")
event_maker.flush_trace_buffer(True, allow_terms=['test2'])

event_maker.make_entry('log', 'test log', 'should be visible in log.txt', 'scratch')
