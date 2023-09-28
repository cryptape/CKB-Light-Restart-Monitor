import json
import requests
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask

NodeFlask = Flask(__name__)
light_client_urls = [
    "http://127.0.0.1:9000"
]


def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)
    except Exception as exp:
        raise exp


class RpcGet(object):

    def __init__(self, url):
        self.url = url

    def get_scripts(self):
        return self.call("get_scripts", [])

    def get_tip_header(self):
        return self.call("get_tip_header", [])

    def get_peers(self):
        return self.call("get_peers", [])

    def get_min_script_height(self):
        min_height = 999999999
        scripts = self.get_scripts()
        if len(scripts) == 0:
            return 0
        for script in scripts:
            min_height = min(min_height, int(script['block_number'], 16))
        return min_height

    def call(self, method, params):

        headers = {'content-type': 'application/json'}
        data = {
            "id": 42,
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        response = requests.post(self.url, data=json.dumps(data), headers=headers).json()
        if 'error' in response.keys():
            error_message = response['error'].get('message', 'Unknown error')
            raise Exception(f"Error: {error_message}")
        return response.get('result', None)


#
@NodeFlask.route("/metrics")
def Node_Get():
    CKB_Light_Chain = CollectorRegistry(auto_describe=False)
    script_min_height_gauge = Gauge("get_script_min_height",
                                    "get script min height",
                                    [],
                                    registry=CKB_Light_Chain)

    script_length_gauge = Gauge("get_script_length",
                                "get script length",
                                [],
                                registry=CKB_Light_Chain)

    tip_header_number_gauge = Gauge("get_tip_header_number",
                                    "Returns the header with the highest block number in the canonical chain",
                                    [], registry=CKB_Light_Chain)

    node_connected_duration_gauge = Gauge('node_connected_duration_seconds', 'Duration of node connection seconds',
                                          ["node_id"],
                                          registry=CKB_Light_Chain)

    node_connected_proved_best_known_header_height_gauge = Gauge('node_connected_proved_best_known_header_height',
                                                                 'node connected proved best known header height ',
                                                                 ["node_id"],
                                                                 registry=CKB_Light_Chain)

    get_result = RpcGet(light_client_urls[0])
    min_height = get_result.get_min_script_height()
    script_min_height_gauge.set(min_height)

    script_length = len(get_result.get_scripts())
    script_length_gauge.set(script_length)

    tip_header_number_gauge.set(int(get_result.get_tip_header()['number'], 16))

    peers = get_result.get_peers()
    for peer in peers:
        node_connected_duration_gauge.labels(node_id=peer['node_id']).set(int(peer["connected_duration"], 16))
        node_connected_proved_best_known_header_height_gauge.labels(node_id=peer['node_id']).set(
            int(peer['sync_state']['proved_best_known_header']['number'], 16))

    return Response(prometheus_client.generate_latest(CKB_Light_Chain), mimetype="text/plain")


if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0", port=8200)
