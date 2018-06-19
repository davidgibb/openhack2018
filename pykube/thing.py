import operator
import pykube
import pprint as pp
import yaml

api = pykube.HTTPClient(pykube.KubeConfig.from_file("/home/matthew/.kube/config"))


# takes in a tenant id
# returns a tuple
# (statefulset,service)
# where those objects are pykube objects
def getObjs(tenantid):
    statefulset_fname = './statefulset.yaml'
    service_fname = './service.yaml'
    with open(statefulset_fname,'r') as f:
        statefulset_yaml = f.read().replace('{{TENANT}}',tenantid)
    statefulset_dict = yaml.load(statefulset_yaml)

    with open(service_fname,'r') as f:
        service_yaml = f.read().replace('{{TENANT}}',tenantid)
    service_dict = yaml.load(service_yaml)

    ss_obj = pykube.StatefulSet(api,statefulset_dict)
    service_obj = pykube.Service(api,service_dict)
    return((ss_obj,service_obj))

def createTenant(tenantid):
    print('creating tenant for %s' % tenandid)
    (ss,service) = getObjs(tenantid)

    ss.create()
    service.create()

def getTenantStatus(tenantid):


    (ss,service) = getObjs(tenantid)
    print('Creating statefulset and service for tenant %s...' % tenantid)

    # wait for stateful set to be ready
    watch = ss.watch()
    print('Watching for statefulset creation') 
    # watch is a generator:
    for watch_event in watch:
        if watch_event.type == 'ADDED':
           print('Statefulset added')
           break
        print(watch_event.type) # 'ADDED', 'DELETED', 'MODIFIED'
        print(watch_event.object) # pykube.Job object
    print('stateful 1et created?')

    print('Watching for service creation')
    # Wait for service to be ready

    watch = service.watch()
  
    # watch is a generator:
    for watch_event in watch:
        print(watch_event.type) # 'ADDED', 'DELETED', 'MODIFIED'
        print(watch_event.object) # pykube.Job object

    print('done')

def deleteTenant(tenantid):

    print('deleting statefulset and service for tenant %s' % tenantid)
    (service,statefulset) = getObjs(tenantid)

    service.delete()
    statefulset.delete()


#deleteTenant('tenant1')
createTenant('tenant2')


