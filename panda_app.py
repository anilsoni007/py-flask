from flask import Flask, render_template_string, request
import socket
import requests
import os
import psutil

app = Flask(__name__)

# Global list to store user data
user_data = []

def get_node_info():
    if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount'):
        try:
            pod_name = open('/etc/hostname').read().strip()
            return f"Pod Name: {pod_name}"
        except Exception as e:
            return f"Error fetching pod info: {str(e)}"

    try:
        metadata_url = "http://169.254.169.254/latest/meta-data/public-ipv4"
        response = requests.get(metadata_url, timeout=2)
        if response.status_code == 200:
            return f"EC2 Instance IP: {response.text}"
    except requests.exceptions.RequestException:
        pass

    return f"Local Machine: {socket.gethostname()}"

def check_memory_usage():
    memory = psutil.virtual_memory()
    used_memory_percentage = memory.percent
    return used_memory_percentage

@app.route('/', methods=['GET', 'POST'])
def hello_docker():
    node_info = get_node_info()
    hosting_resource = "Unknown Resource"
    if "Pod Name" in node_info:
        hosting_resource = "Kubernetes Pod"
    elif "EC2 Instance IP" in node_info:
        hosting_resource = "EC2 Instance"
    else:
        hosting_resource = "Local Machine"

    memory_usage = check_memory_usage()
    memory_status = "Healthy" if memory_usage <= 80 else "Unhealthy"

    global user_data

    if request.method == 'POST':
        user_name = request.form.get('name', '').strip()
        if user_name:
            # Add new user to the user_data list
            user_data.append({"serial": len(user_data) + 1, "name": user_name})

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask App</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #ff7eb3, #ff758c, #ff637b);
                height: 100vh;
                overflow: hidden;
                color: #fff;
            }
            .container {
                text-align: center;
                padding: 20px;
            }
            h1 {
                font-size: 2.5rem;
                color: #ffd700;
            }
            p {
                font-size: 1.2rem;
            }
            .host-info {
                margin-top: 20px;
                padding: 10px;
                background: black;
                color: green;
            }
            form {
                margin-top: 20px;
            }
            table {
                margin: 20px auto;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid white;
            }
            th, td {
                padding: 10px;
                text-align: left;
            }
            .panda {
                position: absolute;
                animation: roll 5s infinite linear;
                font-size: 2rem;
            }
            @keyframes roll {
                from { transform: translate(-50px, 0) rotate(0deg); }
                to { transform: translate(100vw, 100vh) rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>This is Anil Soni's Test App!!!!</h1>
            <p>This is my test app using Python Flask!</p>
            <p>{{ node_info }}</p>
            <div class="host-info">
                This app is hosted on: {{ hosting_resource }}<br>
                Memory Status: <span style="color: {{ 'red' if memory_status == 'Unhealthy' else 'green' }}">{{ memory_status }}</span><br>
                Memory Usage: {{ memory_usage }}%
            </div>
            <form method="POST">
                <label for="name">Enter your name:</label>
                <input type="text" id="name" name="name" required>
                <button type="submit">Submit</button>
            </form>
            {% if user_data %}
                <h2>User Table</h2>
                <table>
                    <tr>
                        <th>Serial No</th>
                        <th>Name</th>
                    </tr>
                    {% for row in user_data %}
                    <tr>
                        <td>{{ row.serial }}</td>
                        <td>{{ row.name }}</td>
                    </tr>
                    {% endfor %}
                </table>
            {% endif %}
        </div>
        <script>
            for (let i = 0; i < 30; i++) {
                const panda = document.createElement('div');
                panda.className = 'panda';
                panda.textContent = '🐼';
                panda.style.top = Math.random() * 100 + 'vh';
                panda.style.left = Math.random() * 100 + 'vw';
                panda.style.animationDuration = Math.random() * 3 + 2 + 's';
                panda.style.animationDelay = Math.random() * 2 + 's';
                document.body.appendChild(panda);
            }
        </script>
    </body>
    </html>
    ''', node_info=node_info, hosting_resource=hosting_resource, memory_status=memory_status,
       memory_usage=memory_usage, user_data=user_data)

@app.route('/health')
def health_check():
    memory_usage = check_memory_usage()
    if memory_usage > 80:
        return f"Health Status: Unhealthy\nMemory usage: {memory_usage}%", 500
    return f"Health Status: Healthy\nMemory usage: {memory_usage}%", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
