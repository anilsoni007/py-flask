from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_docker():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask App</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                color: #fff;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #ff7eb3, #ff758c, #ff637b);
                height: 100vh;
                overflow: hidden; /* Prevent scrollbars */
            }
            .container {
                text-align: center;
                padding: 20px;
                position: relative;
                z-index: 2; /* Ensure text is above pandas */
                color: white;
            }
            h1 {
                font-size: 2.5rem;
                margin-bottom: 10px;
                color: #ffd700;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.6);
            }
            p {
                font-size: 1.2rem;
                line-height: 1.5;
                margin: 0;
            }
            .panda {
                position: absolute;
                font-size: 2rem;
                animation: roll infinite linear;
            }
            @keyframes roll {
                0% {
                    transform: translate(-50px, 0);
                }
                100% {
                    transform: translate(100vw, 100vh) rotate(360deg);
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>This is Anil Soni</h1>
            <p>This is my test app using Python Flask!</p>
        </div>
        <script>
            const numPandas = 20; // Number of pandas
            for (let i = 0; i < numPandas; i++) {
                const panda = document.createElement('div');
                panda.className = 'panda';
                panda.textContent = '🐼';
                panda.style.top = Math.random() * 100 + 'vh';
                panda.style.left = Math.random() * 100 + 'vw';
                panda.style.animationDuration = Math.random() * 5 + 3 + 's';
                panda.style.animationDelay = Math.random() * 3 + 's';
                document.body.appendChild(panda);
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
