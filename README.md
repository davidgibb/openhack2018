# Commands for Kubectl

Get list of pods:
`kubectl get pods`

Connect to main pod
`kubectl exec -it task3-0 bash`

Or for the monitoring pod
`kubectl exec -it task3-0 mcstatus bash`

Get IP address of minecraft
`kubectl get services`
