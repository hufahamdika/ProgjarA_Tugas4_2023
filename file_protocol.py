import json
import logging
import shlex

from file_interface import FileInterface


class FileProtocol:
    def __init__(self):
        self.file = FileInterface()

    def proses_string(self, string_datamasuk=''):
        logging.warning(f"processing string: {string_datamasuk}")
        c = shlex.split(string_datamasuk)
        try:
            c_request = c[0].lower().strip()
            logging.warning(f"processing request: {c_request}")
            params = [x for x in c[1:]]
            cl = getattr(self.file, c_request)(params)
            return json.dumps(cl)
        except Exception:
            return json.dumps(dict(status='ERROR', data='request unknown'))


if __name__ == '__main__':
    fp = FileProtocol()
    print(fp.proses_string("LIST"))
    print(fp.proses_string("GET pokijan.jpg donalbebek.jpg"))