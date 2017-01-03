def get_credentials():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = 'http://10.11.50.26:5000/v2.0'
    d['tenant_name'] = os.environ['OS_PROJECT_NAME']
    return d

def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_PROJECT_ID']
    d['project_name']= os.environ['OS_PROJECT_NAME']
    d['domain_name']= os.environ['OS_USER_DOMAIN_NAME']
    return d

def get_session_credentials():
    d = {}
    d['auth_version'] = '3'
    d['user'] = os.environ['OS_USERNAME']
    d['key'] = os.environ['OS_PASSWORD']
    d['authurl'] = os.environ['OS_AUTH_URL']
    d['os_options'] = {'user_domain_id': 'Default','project_domain_id': 'Default','project_name': os.environ['OS_PROJECT_NAME']}
    return d


def get_nova_credentials():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_PROJECT_NAME']
    return d
