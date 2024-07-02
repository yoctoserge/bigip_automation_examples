class FilterModule(object):
    def filters(self):
        return {
                "create_deployment_array": self.create_deployment_array
        }

    def create_deployment_array(self, data, tree):
        rValue = []
        for key, value in data.items():
            ip_arr = tree.get(key, [])
            deployments = []
            for ip in ip_arr:
                deployments.append({
                    "target": {
                        "address": ip
                    }
                })
            if len(deployments) > 0:
                rValue.append({
                          "id": key,
                          "body": deployments
                })

        return rValue
