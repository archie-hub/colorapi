Kube/Openshift playing with builds

# How I'm building for OC
```commandline
apiVersion: image.openshift.io/v1
kind: ImageStream
metadata:
  annotations:
    openshift.io/image.dockerRepositoryCheck: "2025-12-04T17:53:07Z"
  creationTimestamp: "2025-12-04T17:41:14Z"
  generation: 4
  name: python39
spec:
  lookupPolicy:
    local: false
  tags:
  - annotations: null
    from:
      kind: DockerImage
      name: registry.access.redhat.com/ubi8/python-39
    generation: 4
    importPolicy:
      importMode: Legacy
    name: latest
    referencePolicy:
      type: Source
```

I need the ubi image referenced above for oc.

```commandline
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: colorapi-build
spec:
  failedBuildsHistoryLimit: 5
  nodeSelector: null
  output:
    to:
      kind: ImageStreamTag
      name: colorapi:latest
  runPolicy: Serial
  source:
    git:
      ref: main
      uri: https://github.com/archie-hub/colorapi.git
    type: Git
  strategy:
    sourceStrategy:
      from:
        kind: ImageStreamTag
        name: python39:latest
    type: Source
  successfulBuildsHistoryLimit: 5
```

# Podman build for testing.

```podman build -t colorapi:v5 .```

```podman run -p8080:8080 colorapi:v5```

```
archie@windows ~ % while true; do curl http://127.0.0.1:9000/change-color; sleep 0.1; done 
{"color":"blue","status":"ok"}
{"color":"green","status":"ok"}
{"color":"pink","status":"ok"}
{"color":"navy","status":"ok"}
{"color":"purple","status":"ok"}
{"color":"yellow","status":"ok"}
{"color":"maroon","status":"ok"}
{"color":"purple","status":"ok"}
{"color":"maroon","status":"ok"}
{"color":"green","status":"ok"}
{"color":"red","status":"ok"}
{"color":"navy","status":"ok"}
{"color":"red","status":"ok"}
{"color":"navy","status":"ok"}
{"color":"maroon","status":"ok"}
{"color":"blue","status":"ok"}
{"color":"yellow","status":"ok"}
```

### Notes

Webapge on http://127.0.0.1:8080/ changes color when I hit endpoint at

http://127.0.0.1:8080/change-color

