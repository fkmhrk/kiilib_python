import kii

class ServerAPI:
    def __init__(self, context):
        self.context = context

    def execute(self, api, params):
        """
        Executes the specified server code. 
        """        
        url = '%s/apps/%s/server-code/versions/current/%s' % (self.context.url, self.context.app_id, api)
        client = self.context.newClient()
        client.method = "POST"
        client.url = url
        client.setContentType('application/json')
        client.setKiiHeaders(self.context, True)
        (code, body) = client.send(params)
        if code != 200:
            raise CloudException(code, body)
        return body










