from ansible.module_utils.action_converter import httpHeaderActionConverter
from ansible.module_utils.action_converter import httpSetCookieActionConverter
from ansible.module_utils.action_converter import forwardActionConverter
from ansible.module_utils.condition_converter import httpHostContitionConverter
from ansible.module_utils.condition_converter import httpHeaderContidionConverter
from ansible.module_utils.condition_converter import httpUriContitionConverter

from ansible.module_utils.irule_bo import IRule

def addIfClause(ifClause, currentIfClause):
    if len(currentIfClause.ifs) == 0:
        currentIfClause.ifs.append(ifClause)
    else:
        addIfClause(ifClause, currentIfClause.ifs[0])


class RuleConverterContext:
    def __init__(self):
        self.irule = IRule()

    def appendRequestIf(self, ifClause):
        if len(self.irule.request.ifs) == 0:
            self.irule.request.ifs.append(ifClause)
        else:
            addIfClause(ifClause, self.irule.request.ifs[0])

    def appendResponseIf(self, ifClause):
        if len(self.irule.response.ifs) == 0:
            self.irule.response.ifs.append(ifClause)
        else:
            addIfClause(ifClause, self.irule.response.ifs[0])

class LtmPolicyConverterFactory:
    def __init__(self):
        self.policyConverter = {
            "http": HttpPolicyConverterFactory()
        }

class HttpPolicyConverterFactory:
    def __init__(self):
        self.conditionConverterFactory = {
            "http-host": httpHostContitionConverter,
            "http-header": httpHeaderContidionConverter,
            "http-uri": httpUriContitionConverter
        }
        self.actionConverterFactory = {
            "http-header": httpHeaderActionConverter,
            "http-set-cookie": httpSetCookieActionConverter,
            "forward": forwardActionConverter
        }