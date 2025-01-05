from flask import Flask
import socket
import requests
import os
import psutil  # To check memory usage

app = Flask(__name__)

def get_node_info():
    # Check if the app is running in Kubernetes
    if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount'):
        # Running in Kubernetes pod
        try:
            pod_name = open('/etc/hostname').read().strip()  # Get the pod name
            return f"Pod Name: {pod_name}"
        except Exception as e:
            return f"Error fetching pod info: {str(e)}"
    
    # Check if the app is running on EC2 instance
    try:
        metadata_url = "http://169.254.169.254/latest/meta-data/public-ipv4"
        response = requests.get(metadata_url, timeout=2)
        if response.status_code == 200:
            return f"EC2 Instance IP: {response.text}"
    except requests.exceptions.RequestException:
        pass
    
    # If not in Kubernetes or EC2, return the local machine hostname
    return f"Local Machine: {socket.gethostname()}"

def check_memory_usage():
    memory = psutil.virtual_memory()  # Get memory info
    used_memory_percentage = memory.percent  # Get the percentage of memory used
    return used_memory_percentage

@app.route('/')
def hello_docker():
    node_info = get_node_info()
    
    hosting_resource = "Unknown Resource"
    if "Pod Name" in node_info:
        hosting_resource = "Kubernetes Pod"
    elif "EC2 Instance IP" in node_info:
        hosting_resource = "EC2 Instance"
    else:
        hosting_resource = "Local Machine"

    # Check memory usage
    memory_usage = check_memory_usage()
    memory_status = "Healthy"
    if memory_usage > 80:  # If memory usage is above 80%, consider it unhealthy
        memory_status = "Unhealthy"

    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask App</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                color: #fff;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #ff7eb3, #ff758c, #ff637b);
                height: 100vh;
                overflow: hidden; /* Prevent scrollbars */
            }}
            .container {{
                text-align: center;
                padding: 20px;
                position: relative;
                z-index: 2; /* Ensure text is above pandas */
                color: white;
            }}
            h1 {{
                font-size: 2.5rem;
                margin-bottom: 10px;
                color: #ffd700;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
            }}
            p {{
                font-size: 1.2rem;
                line-height: 1.5;
                margin: 0;
            }}
            .panda {{
                position: absolute;
                font-size: 2rem;
                animation: roll infinite linear;
            }}
            @keyframes roll {{
                0% {{
                    transform: translate(-50px, 0);
                }}
                100% {{
                    transform: translate(100vw, 100vh) rotate(360deg);
                }}
            }}
            .host-info {{
                background-color: black;
                color: green;
                padding: 10px;
                margin-top: 20px;
                font-size: 1.2rem;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>This is Anil Soni</h1>
            <p>This is my test app using Python Flask!</p>
            <p>{node_info}</p>
            <div class="host-info">
                This app is hosted on: <span>{hosting_resource}</span><br>
                Memory Status: <span style="color: { 'red' if memory_status == 'Unhealthy' else 'green' }">{memory_status}</span><br>
                Memory Usage: <span>{memory_usage}%</span>
            </div>
        </div>
        <script>
            const numPandas = 20; // Number of pandas
            for (let i = 0; i < numPandas; i++) {{
                const panda = document.createElement('div');
                panda.className = 'panda';
                panda.textContent = '🐼';
                panda.style.top = Math.random() * 100 + 'vh';
                panda.style.left = Math.random() * 100 + 'vw';
                panda.style.animationDuration = Math.random() * 5 + 3 + 's';
                panda.style.animationDelay = Math.random() * 3 + 's';
                document.body.appendChild(panda);
            }}
        </script>
    </body>
    </html>
    '''

@app.route('/health')
def health_check():
    # Check if the app is working fine
    memory_usage = check_memory_usage()
    if memory_usage > 80:
        return "Health Status: Unhealthy\nMemory usage: {}%".format(memory_usage), 500  # Return unhealthy if memory exceeds 30%
    return "Health Status: Healthy\nMemory usage: {}%".format(memory_usage), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
