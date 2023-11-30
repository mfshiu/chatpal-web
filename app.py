# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for

from book import book_app
import helper
from setting import setting_app
import app_config

   
app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.register_blueprint(book_app)
app.register_blueprint(setting_app)
      
     
@app.context_processor
def inject_stage_and_region():  
    return dict(title="vChat 管理系統")

   
@app.route('/')
def home():
    # return render_template('/app-user-list.html')
    return render_template('/index.html')
    # return redirect(url_for('booking.book'))
    
     
@app.route('/upload_voice', methods=['POST'])
def upload_voice():
    if 'audio_data' in request.files:
        audio_file = request.files['audio_data']
        
        # To read the file directly
        audio_content = audio_file.read()
        cmd_insert = f'''insert into "AudioInput"
    (wave_data) values (%s) RETURNING id;'''
        params = (audio_content,)
        audio_id = helper.insert_and_fetch_id(cmd_insert, params)
        print(f"audio_id: {audio_id}")

        # Alternatively, to save the file and then read it
        filename = f"/Users/xumingfang/Work/chatpal/web/_input/received_audio_{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav"
        audio_file.save(filename)
        # with open(filename, 'rb') as f:
        #     audio_content = f.read()
 
        return jsonify({'message': 'Audio processed successfully'})
    else:
        return jsonify({'error': 'No audio file provided'}), 400


@app.route('/app-user-list.html')
def userList():
    return render_template('/app-user-list.html')
 
  
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    #app.run(host=config.app_ip, port=config.app_port)
            