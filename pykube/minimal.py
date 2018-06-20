import pykube
                                         
try:                            
    api = pykube.KubeConfig.from_service_account()                       
except FileNotFoundError:                                                                           
    print('Cannot get from in cluster file, trying home dir')                                       
    api = pykube.HTTPClient(pykube.KubeConfig.from_file("~/.kube/config"))

print(api.config.namespace)
