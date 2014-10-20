import json
import requests

from st2common.models.api import constants
from st2actions import handlers
from st2common import log as logging


LOG = logging.getLogger(__name__)


STATUS_MAP = dict()
STATUS_MAP[constants.ACTIONEXEC_STATUS_SCHEDULED] = 'RUNNING'
STATUS_MAP[constants.ACTIONEXEC_STATUS_RUNNING] = 'RUNNING'
STATUS_MAP[constants.ACTIONEXEC_STATUS_SUCCEEDED] = 'SUCCESS'
STATUS_MAP[constants.ACTIONEXEC_STATUS_FAILED] = 'ERROR'


def get_handler():
    return MistralCallbackHandler


class MistralCallbackHandler(handlers.ActionExecutionCallbackHandler):

    @staticmethod
    def callback(url, context, status, result):
        try:
            method = 'PUT'
            output = json.dumps(result) if isinstance(result, dict) else str(result)
            v1 = 'v1' in url
            data = {'state': STATUS_MAP[status], 'output': output} if v1 else {'result': output}
            headers = {'content-type': 'application/json'}
            response = requests.request(method, url, data=json.dumps(data), headers=headers)
            if response.status_code != 200:
                response.raise_for_status()
        except Exception as e:
            LOG.error(e)
