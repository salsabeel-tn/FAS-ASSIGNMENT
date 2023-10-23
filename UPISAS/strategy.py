from abc import ABC, abstractmethod
import requests
import pprint

from UPISAS.exceptions import EndpointNotReachable
from UPISAS.knowledge import Knowledge
from UPISAS import perform_get_request, validate_schema
import logging

pp = pprint.PrettyPrinter(indent=4)


class Strategy(ABC):

    def __init__(self, exemplar):
        self.exemplar = exemplar
        self.knowledge = Knowledge(dict(), dict(), dict(), dict(), dict(), dict(), dict())

    def ping(self):
        ping_res = self._get_schema(self.exemplar.base_endpoint)
        logging.info(f"ping result: {ping_res}")

    def monitor(self, endpoint_suffix="monitor"):
        url = '/'.join([self.exemplar.base_endpoint, endpoint_suffix])
        response, status_code = perform_get_request(url)
        if status_code == 404:
            logging.info("Cannot retrieve data, check that the monitor endpoint exists.")
            return False
        fresh_data = response.json()
        print("[Monitor]\tgot fresh_data: " + str(fresh_data))
        validate_schema(fresh_data, self.knowledge.monitor_schema)
        data = self.knowledge.monitored_data
        for key in list(fresh_data.keys()):
            if key not in data:
                data[key] = []
            data[key].append(fresh_data[key])
        print("[Knowledge]\tdata monitored so far: " + str(self.knowledge.monitored_data))
        return True

    def execute(self, adaptation, endpoint_suffix="execute"):
        validate_schema(adaptation, self.knowledge.execute_schema)
        url = '/'.join([self.exemplar.base_endpoint, endpoint_suffix])
        response = requests.post(url, adaptation)
        print("[Execute]\tposted configuration: " + str(adaptation))
        if response.status_code == 404:
            logging.info("Cannot execute adaptation on remote system, check that the execute endpoint exists.")
            return False
        return True

    def get_adaptation_options(self, endpoint_suffix: "API Endpoint" = "adaptation_options"):
        logging.info("before getting the adaptation_options, we get their schema")
        self.get_adaptation_options_schema()
        self.knowledge.adaptation_options = self._get_schema(endpoint_suffix)
        validate_schema(self.knowledge.adaptation_options, self.knowledge.adaptation_options_schema)
        logging.info("adaptation_options set to: ")
        pp.pprint(self.knowledge.adaptation_options)

    def get_monitor_schema(self, endpoint_suffix = "monitor_schema"):
        '''Queries the API for a schema describing the monitoring info of the particular exemplar'''
        self.knowledge.monitor_schema = self._get_schema(endpoint_suffix)
        logging.info("monitor_schema set to: ")
        pp.pprint(self.knowledge.monitor_schema)

    def get_execute_schema(self, endpoint_suffix = "execute_schema"):
        self.knowledge.execute_schema = self._get_schema(endpoint_suffix)
        logging.info("execute_schema set to: ")
        pp.pprint(self.knowledge.execute_schema)

    def get_adaptation_options_schema(self, endpoint_suffix: "API Endpoint" = "adaptation_options_schema"):
        self.knowledge.adaptation_options_schema = self._get_schema(endpoint_suffix)
        logging.info("adaptation_options_schema set to: ")
        pp.pprint(self.knowledge.adaptation_options_schema)

    def _get_schema(self, endpoint_suffix: "API Endpoint"):
        '''Queries the API for a schema describing the execution info of the particular exemplar'''
        url = '/'.join([self.exemplar.base_endpoint, endpoint_suffix])
        response, status_code = perform_get_request(url)
        if status_code == 404:
            logging.warning("Please check that the endpoint you are trying to reach actually exists.")
            raise EndpointNotReachable()
        return response.json()

    @abstractmethod
    def analyze(self):
        """ ... """
        pass

    @abstractmethod
    def plan(self):
        """ ... """
        pass

