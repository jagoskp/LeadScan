from kombu import Exchange, Queue

# Define main direct exchange for task routing
leadscan_exchange = Exchange("leadscan", type="direct")

# Define dead letter exchange for isolating failed tasks
dlq_exchange = Exchange("leadscan_dlq", type="direct")

# Task Queues configuration definitions
task_queues = [
    Queue("default", leadscan_exchange, routing_key="default"),
    Queue("ocr", leadscan_exchange, routing_key="ocr"),
    Queue("ai", leadscan_exchange, routing_key="ai"),
    Queue("search", leadscan_exchange, routing_key="search"),
    Queue("report", leadscan_exchange, routing_key="report"),
    Queue("notification", leadscan_exchange, routing_key="notification"),
    Queue("workflow", leadscan_exchange, routing_key="workflow"),
    Queue("maintenance", leadscan_exchange, routing_key="maintenance"),
    Queue(
        "dlq",
        dlq_exchange,
        routing_key="dlq",
        queue_arguments={
            "x-dead-letter-exchange": "leadscan_dlq",
            "x-dead-letter-routing-key": "dlq",
        },
    ),
]
