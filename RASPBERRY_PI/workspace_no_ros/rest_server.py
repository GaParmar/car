import falcon
import json
import os


class LogPath(object):
    def __init__(self): 

        dirs = os.listdir(os.environ['HOME'] + "/LOG/")
        maximum = 0
        for f in dirs:
            if(f.startswith("data")):
                try:
                    maximum = max(maximum, int(f[4:]))
                except:
                    pass

        self.update_log_path(os.environ['HOME'] + "/LOG/data" + str(maximum + 1))

        
    def update_log_path(self, log_path):
        self.log_path = log_path
        with open('config.json', 'w') as outfile:
            json.dump({"log_path": self.log_path}, outfile)


    def on_post(self, req, resp):
        query = falcon.uri.decode(req.query_string)
        queries = query.split("&")

        for each in queries:
            name, data = each.split("=")
            if(name == "log_path"):
                self.update_log_path(data)
        
        resp.status = falcon.HTTP_200


    def on_get(self, req, resp):

        resp.status = falcon.HTTP_200
        resp.body = self.log_path



app = falcon.API()
log_path = LogPath()
app.add_route('/log_path', log_path)

