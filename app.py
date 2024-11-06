from flask import Flask, jsonify, request, render_template
from databaser import Databaser

app = Flask(__name__)
db = Databaser()

def handle_exception(e):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/')
def root():
    try:
        video = db.get_random_video()
        next_video = db.get_random_video([video['id']] if video else None)
        return render_template('index.html', video=video, next_video=next_video)
    except Exception as e:
        return handle_exception(e)

@app.route('/next')
def next_video():
    try:
        history = request.args.get('hist')
        history = list(map(int, history.rstrip(',').split(','))) if history and history != 'null' else None
        video = db.get_random_video(history)
        return jsonify(video)
    except Exception as e:
        return handle_exception(e)

@app.route('/get_<int:video_id>')
def get_video(video_id):
    try:
        video = db.get_video(video_id)
        if video:
            return jsonify(video)
        else:
            return jsonify({"error": "Video not found"}), 404
    except Exception as e:
        return handle_exception(e)

if __name__ == '__main__':
    app.run(debug=True)
