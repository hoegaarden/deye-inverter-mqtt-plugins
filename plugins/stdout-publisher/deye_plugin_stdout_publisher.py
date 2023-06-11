
import logging
import json
import re
import sys
import typing

from deye_events import DeyeEvent, DeyeEventProcessor, DeyeObservationEvent, DeyeLoggerStatusEvent
from deye_config import DeyeConfig
from deye_observation import Observation
from deye_plugin_loader import DeyePluginContext

class DeyeStdoutPublisher(DeyeEventProcessor):
    """
    Publishes events on STDOUT
    """

    __mqtt_topic_suffix_splitter = r"/|_"
    __source_joiner = "/"

    def __init__(self, config: DeyeConfig, dest: typing.IO = sys.stdout):
        self.__log = logging.getLogger(DeyeStdoutPublisher.__name__)
        self.__config = config
        self.__dest = dest

    def initialize(self):
        pass

    def get_id(self):
        return "stdout_publisher"

    def process(self, events: list[DeyeEvent]):
        data = []

        for event in events:
            if isinstance(event, DeyeObservationEvent):
                data.append(DeyeStdoutPublisher.__handle_observation(event.observation))
            elif isinstance(event, DeyeLoggerStatusEvent):
                data.append({"up": 1 if event.online else 0})
            else:
                self.__log.warn(f"Unsupported event type {event.__class__}")

        print(
            json.dumps(
                {
                    "serial": str(self.__config.logger.serial_number),
                    "address": self.__config.logger.ip_address,
                    "port": self.__config.logger.port,
                    "data": data,
                }
            ),
            flush=True,
            file=self.__dest,
        )

    @staticmethod
    def __handle_observation(observation: Observation) -> dict[str, str | float | int]:
        topic_suffix = observation.sensor.mqtt_topic_suffix
        name, source = DeyeStdoutPublisher.__mqtt_topic_to_identity(topic_suffix)

        data = {
            name: observation.value,
            "name": observation.sensor.name,
            "unit": observation.sensor.unit,
            "groups": ",".join(observation.sensor.groups),
            "sensor": observation.sensor.__class__.__name__,
            "timestamp": int(observation.timestamp.timestamp()),
        }
        if source is not None:
            data["source"] = source

        return data

    @classmethod
    def __mqtt_topic_to_identity(cls, topic_suffix: str) -> tuple[str, str | None]:
        # topic_suffix can be something like 'dc/pv2/total_power'
        # and will be split into "power" and "dc/pv2/total"
        parts = re.split(cls.__mqtt_topic_suffix_splitter, topic_suffix)

        name = parts[-1]
        source = cls.__source_joiner.join(parts[:-1])

        return name, None if source == "" else source


class DeyePlugin:
    def __init__(self, plugin_context: DeyePluginContext):
        self.publisher = DeyeStdoutPublisher(config=plugin_context.config)

    def get_event_processors(self) -> [DeyeEventProcessor]:
        return [self.publisher]
