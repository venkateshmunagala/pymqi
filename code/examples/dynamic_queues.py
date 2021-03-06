# See discussion and more examples at http://packages.python.org/pymqi/examples.html
# or in doc/sphinx/examples.rst in the source distribution.

import pymqi

queue_manager = "QM01"
channel = "SVRCONN.1"
host = "192.168.1.135"
port = "1434"
conn_info = "%s(%s)" % (host, port)
message = "Please reply to a dynamic queue, thanks."
dynamic_queue_prefix = "MY.REPLIES.*"
request_queue = "TEST.1"

qmgr = pymqi.connect(queue_manager, channel, conn_info)

# Dynamic queue's object descriptor.
dyn_od = pymqi.OD()
dyn_od.ObjectName = "SYSTEM.DEFAULT.MODEL.QUEUE"
dyn_od.DynamicQName = dynamic_queue_prefix

# Open the dynamic queue.
dyn_input_open_options = pymqi.CMQC.MQOO_INPUT_EXCLUSIVE
dyn_queue = pymqi.Queue(qmgr, dyn_od, dyn_input_open_options)
dyn_queue_name = dyn_od.ObjectName.strip()

# Prepare a Message Descriptor for the request message.
md = pymqi.MD()
md.ReplyToQ = dyn_queue_name

# Send the message.
queue = pymqi.Queue(qmgr, request_queue)
queue.put(message, md)

# Get and process the response here..

dyn_queue.close()
queue.close()
qmgr.disconnect()
