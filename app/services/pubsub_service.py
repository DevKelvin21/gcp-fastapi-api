import os
from google.cloud import pubsub_v1

ENV_VAR_MSG = "Specified environment variable is not set."

class PubSubService:
    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = os.environ.get("PUBSUB_TOPIC", ENV_VAR_MSG)

    def publish_message(self, message: str) -> str:
        data = message.encode("utf-8")
        future = self.publisher.publish(self.topic_path, data=data)
        return future.result()
