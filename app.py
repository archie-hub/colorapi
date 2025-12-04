from flask import Flask, Response
import random
import queue
import threading

app = Flask(__name__)

COLORS = ["red","blue","green","purple","yellow","pink","orange","teal","maroon","navy"]

current_color = "white"
subscribers = []
lock = threading.Lock()


# --------------------------------------------------
# MAIN PAGE — shows the color name text
# --------------------------------------------------
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Color Changer</title>
    <meta charset="UTF-8" />
    <style>
        body {
            margin: 0;
            background: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: Arial, sans-serif;
            color: black;
            font-size: 48px;
            font-weight: bold;
        }
        #colorName {
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
    </style>
</head>
<body>

<div id="colorName">white</div>

<script>
    const colorName = document.getElementById("colorName");
    const events = new EventSource("/color-stream");

    events.onmessage = function(e) {
        const newColor = e.data;
        document.body.style.backgroundColor = newColor;

        // Adjust text color for readability
        const lightColors = ["yellow", "pink", "white"];
        colorName.style.color = lightColors.includes(newColor) ? "black" : "white";

        colorName.textContent = newColor;
        console.log("Color changed to:", newColor);
    };
</script>

</body>
</html>
"""


# --------------------------------------------------
# SIMPLE PAGE (OPTIONAL)
# --------------------------------------------------
@app.route("/v1")
def index_v1():
    return """
<!DOCTYPE html>
<html>
<head><title>Change</title></head>
<body style="margin:0; background:white;">

<script>
    const events = new EventSource("/color-stream");

    events.onmessage = function(e) {
        document.body.style.backgroundColor = e.data;
        console.log("Color changed to:", e.data);
    };
</script>

</body>
</html>
"""


# --------------------------------------------------
# SSE STREAM
# --------------------------------------------------
@app.route("/color-stream")
def color_stream():
    q = queue.Queue()

    with lock:
        subscribers.append(q)

    def stream():
        try:
            while True:
                color = q.get()
                yield f"data: {color}\n\n"
        finally:
            with lock:
                subscribers.remove(q)

    return Response(stream(), mimetype="text/event-stream")


# --------------------------------------------------
# BROADCAST FUNCTION
# --------------------------------------------------
def broadcast(color):
    with lock:
        for q in subscribers:
            q.put(color)


# --------------------------------------------------
# API ENDPOINT TO CHANGE THE COLOR
# --------------------------------------------------
@app.route("/change-color")
def change_color():
    global current_color
    new_color = random.choice([c for c in COLORS if c != current_color])
    current_color = new_color

    broadcast(new_color)

    return {"status": "ok", "color": new_color}


@app.route("/health")
def health():
    return {"status": "healthy"}, 200

# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
