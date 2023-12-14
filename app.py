# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
 
from datetime import datetime
from flask import Flask, jsonify, redirect, render_template, request, url_for
from logging import Logger
import os
import queue
from threading import Thread

import paho.mqtt.client as mqtt

import helper
import app_config


logger:Logger = helper.get_logger() 
response_queue = queue.Queue()
mqtt_client = None
mqtt_thread = None


def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code " + str(rc))
    client.subscribe("voice.text")
    client.subscribe("voice.url")

def on_message(client:mqtt.Client, db, message):
    global response_queue
    logger.debug(f"Topic: {message.topic}, Payload: {message.payload}")
    text = message.payload.decode('utf-8', 'ignore')
    if "voice.text" == message.topic:
        logger.info(f"Reply text: {text}")
    elif "voice.url" == message.topic:
        response_queue.put(text)
        logger.info(f"Reply voice: {text}, response_queue: {response_queue}")
        client.publish("voice.spoken")


def initialize_mqtt():
    logger.debug(f"initialize_mqtt")
    global mqtt_client, mqtt_thread

    if mqtt_client:
        logger.info(f"MQTT is initialized.")
        return
    
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_params = app_config.mqtt_params
    mqtt_client.username_pw_set(mqtt_params["username"], mqtt_params["password"])
    mqtt_client.connect(mqtt_params["host"], mqtt_params["port"], mqtt_params["keepalive"])

    def run_mqtt():
        mqtt_client.loop_start()
    mqtt_thread = Thread(target=run_mqtt)
    mqtt_thread.start()
    

app = Flask(__name__) 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
initialize_mqtt()

       
def cleanup_mqtt():
    """ Clean up MQTT client resources. """
    global mqtt_client
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()


@app.context_processor
def inject_stage_and_region():  
    return dict(title="Chat Pal")
   
               
@app.route('/')
def home():
    # return render_template('/app-user-list.html')
    return render_template('index.html')
    # return render_template('test/test_kdavis_vad.html')
    # return redirect(url_for('booking.book'))
     

@app.route('/upload_voice', methods=['POST'])
def upload_voice():
    if 'audio_data' in request.files:
        audio_file = request.files['audio_data']
       
        audio_content = audio_file.read()
        # logger.debug(f"publish:'hearing.voice', audio_content: {len(audio_content)}")
        mqtt_client.publish("hearing.voice", audio_content)
        filepath = os.path.join(app_config.audio_temp_dir, f"received_audio_{datetime.now().strftime('%Y%m%d-%H%M%S')}.wav")
        with open(filepath, 'wb') as f: 
            f.write(audio_content)
     
        try:
            global response_queue
            logger.debug(f"Wait for responsing")
            response = response_queue.get(timeout=10)  # Timeout in seconds
            logger.debug(f"response: {response}")
            return jsonify({"audioUrl": response})
        except queue.Empty:
            logger.error("queue.Empty")
            return jsonify({"error": "No response received within timeout"}), 408
        # return jsonify({'message': 'Audio processed successfully'})
    else:
        return jsonify({'error': 'No audio file provided'}), 400
         
           
@app.route('/app-user-list.html')
def userList():
    return render_template('/app-user-list.html')
 
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # initialize_mqtt()
    #app.run(host=config.app_ip, port=config.app_port)
