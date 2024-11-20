import pprint, time
from UPISAS.exemplar import Exemplar
import logging

pp = pprint.PrettyPrinter(indent=4)
logging.getLogger().setLevel(logging.INFO)

class RAMSES(Exemplar):
    """
    A class which encapsulates the RAMSES exemplar run in a docker container.
    """
    _container_name = ""
    
    def __init__(self, auto_start: "Whether to immediately start the container after creation" = False, container_name="ramses-knowledge"):
        '''Create an instance of the RAMSES exemplar'''
        ramses_docker_kwargs = {
            "name": container_name,
            "image": "giamburrasca/ramses-knowledge:${ARCH}",
            "ports": {32841: 58005},  # Adjust if necessary
            "network": "ramses-sas-net",
        }

        super().__init__("http://localhost:32841", ramses_docker_kwargs, auto_start)

    def start_run(self):
        logging.info("RAMSES exemplar started.")
