Kube/Openshift playing with builds

Webapge on http://127.0.0.1:9000/ changes color when I hit endpoint at

http://127.0.0.1:9000/change-color

Podman build for testing.

```podman build -t colorapi:v5 .```

```podman run -p9000:9000 colorapi:v5```