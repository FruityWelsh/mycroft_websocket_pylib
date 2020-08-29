#!/bin/env python
import json
from websocket import create_connection  # type: ignore
import logging

class connect():
    def __init__(self, mycroft_addr, mycroft_port, LOGLEVEL=logging.WARN):
        logging.basicConfig(level=LOGLEVEL)
        self.url = f"ws://{mycroft_addr}:{mycroft_port}/core" 
        logging.debug(f"Websocket url: {self.url}")
        try:
           self.mycroft_connection = create_connection(self.url)
           logging.debug("Websocket connected to {self.url}") 
        except:    
           self.mycroft_connection.close() 
           raise

        
    def _send(self, message): 
        logging.debug(f"Data being sent: {message}")
        send_status = self.mycroft_connection.send(json.dumps(message))
        logging.debug(f"Send status: {send_status}")
        return send_status
      
    def listen(self):  
        message_recevied = self.mycroft_connection.recv() 
        logging.debug(f"message_recevied: {message_recevied}")
        yield message_recevied
    
    def close(self):
        logging.debug("Mycroft websocket closing")
        self.mycroft_connection.close()
        logging.debug("Mycroft websocket closed")

    def __exit__(self):
        self.close()

    def speak(self, utterance):
        message = {'type': 'speak',
                   'data': {'utterance': utterance}
                  }
        send_status = self._send(message)
        return send_status 
