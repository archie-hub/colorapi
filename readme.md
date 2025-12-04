Kube/Openshift playing with builds

Webapge on http://127.0.0.1:9000/ changes color when I hit endpoint at

http://127.0.0.1:9000/change-color

# Podman build for testing.

```podman build -t colorapi:v5 .```

```podman run -p9000:9000 colorapi:v5```

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
dsd
