import operator
import pykube
import pprint as pp
import yaml
from flask import Flask
from flask import jsonify
from flask import Response
from flask.json import dumps
import os
app = Flask(__name__)

home_fname = '/home/matthew/.kube/config'
secret_fname = '/data/kubeconfig/config'
if os.path.isfile(secret_fname):
    kubeconfig_fname = secret_fname
else:
    assert(os.path.isfile(home_fname))
    kubeconfig_fname = home_fname
print('Using file %s as kubeconfig' % kubeconfig_fname)
api = pykube.HTTPClient(pykube.KubeConfig.from_file(kubeconfig_fname))



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

@app.route('/<tenantid>',methods=['POST'])
def createTenant(tenantid):
    print('creating tenant for %s' % tenantid)
    (ss,service) = getObjs(tenantid)

    if ss.exists() or service.exists():
        ret = "Tenant already exists"
        return(Response(dumps({"error":"Tenant already exists"}), status=404, mimetype='application/json'))
        return(Response(ret,status=404, mimetype='application/json'))
    else:
        ss.create()
        service.create()

        return(Response(status=202, mimetype='application/json'))


@app.route('/',methods=['GET'])
def listTenants():
    service_objs = pykube.Service.objects(api).filter(selector={"app":"minecraft"})
    services = []
    for s in service_objs:
        health = True
        if not s.name.lower().startswith('mc-'):
            break
        tenantid = s.name[3:]
        data = {
                "name":tenantid,
        }
        try:
            extIp = s.obj['status']['loadBalancer']['ingress'][0]['ip']
            mainPort = [p['port'] for p in s.obj['spec']['ports'] if p['name'].lower() == 'main'][0]
            rconPort = [p['port'] for p in s.obj['spec']['ports'] if p['name'].lower() == 'rcon'][0]
            data['endpoints'] = {
                    "minecraft": extIp + ":" + str(mainPort),
                    "rcon":extIp + ":" + str(rconPort)
            }
        except KeyError:
            data['endpoints'] = {
                    "minecraft":"pending",
                    "rcon": "pending"
            }
            health = False

        if health:
            health = podStatus(tenantid)

        data['ready'] = health
        services.append(data)
    pp.pprint(services)
    print('list function returning')
    return(dumps(services))

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


@app.route('/<tenantid>',methods=['DELETE'])
def deleteTenant(tenantid):

    print('deleting statefulset and service for tenant %s' % tenantid)
    (service,statefulset) = getObjs(tenantid)

    if (service.exists() or statefulset.exists()):

        service.delete()
        statefulset.delete()
        return(Response("", status=202, mimetype='application/json'))
    else:
        return(Response(dumps({"error":"Tenant does not exist"}), status=404, mimetype='application/json'))

# returns True iff there are pods for this tenant, and all those pods are ready
# TODO: deal with status which is not Pending and not Running
def podStatus(tenantid):
    pods = pykube.objects.Pod.objects(api).filter(
                selector={
                    "tenant":tenantid,
                    "app":"minecraft"},
                field_selector={"status.phase": "Running"}
          )
    num_running = len([p for p in pods])
    return(num_running > 0)

#deleteTenant('tenantb')
# tenantid='tenant7'
#createTenant(tenantid)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
