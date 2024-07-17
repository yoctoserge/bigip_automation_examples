def find_node(data, className):
    def find_service_http_node(node, parent_key=None):
        if isinstance(node, dict):
            if node.get('class', '').startswith(className):
                return {
                    "name": parent_key,
                    "data": node
                }
            for key, value in node.items():
                result = find_service_http_node(value, key)
                if result:
                    return result
        elif isinstance(node, list):
            for item in node:
                result = find_service_http_node(item, parent_key)
                if result:
                    return result
        return None

    return find_service_http_node(data)


class FilterModule(object):
    def filters(self):
        return {
                "create_deployment_array": self.create_deployment_array
        }

    def create_deployment_array(self, data, as3docs, tree):
        rValue = []
        for key, value in data.items():
            ip_arr = tree.get(key, [])
            deployments = []
            body = {
                "generic_hosts": {
                "added": []
                },
                "deployments": deployments
            }
            for ip in ip_arr:
                as3_pool = find_node(value['as3'], 'Pool')
                as3_virtual = find_node(value['as3'], 'Service_')

                pools = [{
                    "poolName": as3_pool["name"], 
                    "poolMembers": as3_pool["data"]["members"][0]["servers"],
                    "isServicePool": False,
                    "allowNetworks": []
                }]

                virtuals = [{
                    "virtualName": as3_virtual["name"],
                    "virtualAddress": as3_virtual["data"]["virtualAddresses"][0],
                    "enable_allow_networks": False,
                    "allow_networks": [],
                    "ingressVrfs":[],
                    "egressVrf":[]
                }]

                deployment = {
                    "parameters": {
                        "pools": pools,
                        "virtuals": virtuals,
                    },
                    "additional_parameters": {},
                    "target": {
                        "address": ip
                    },
                    "allow_overwrite": True
                }
                deployments.append(deployment)

            rValue.append({
               "id": value["id"],
                "body": body
            })

        return rValue
