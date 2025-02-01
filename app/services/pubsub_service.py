import os
import json
from google.cloud import pubsub_v1
from typing import Union
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

ENV_VAR_MSG = "Specified environment variable is not set."

class PubSubService:
    def __init__(self):
        self.project_id = os.getenv("GCP_PROJECT_ID", ENV_VAR_MSG)
        self.topic_id = os.getenv("PUBSUB_TOPIC", ENV_VAR_MSG)

        if not self.project_id:
            raise ValueError("Environment variable 'GCP_PROJECT_ID' is not set.")

        if not self.topic_id:
            raise ValueError("Environment variable 'PUBSUB_TOPIC' is not set.")

        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
    
    def publish_message(self, message: Union[str, dict]) -> str:
        """
        Publishes a message to the configured Pub/Sub topic.
        
        Args:
            message (str | dict): The message to publish. If dict, it will be serialized to JSON.
        
        Returns:
            str: The message ID of the published message.
        """
        if isinstance(message, dict):
            try:
                message = json.dumps(message)
            except (TypeError, ValueError) as e:
                raise ValueError(f"Failed to serialize message to JSON: {e}")
        
        if not isinstance(message, str):
            raise TypeError("Message must be a string or a dictionary.")
        
        try:
            data = message.encode("utf-8")
            future = self.publisher.publish(self.topic_path, data=data)
            message_id = future.result()
            logger.info(f"Published message ID: {message_id}")
            return message_id
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    