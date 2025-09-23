#external modules
import os
import json
import random
import datetime
import traceback
import time

#internal modules
import AppCore

#Global system instance
class GlobalState:
    system = AppCore.AppCore()
    
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.debug_mode = self.system.config.get("debug_mode", False)
        self.language = self.system.config.get("default_language", "en")
        self.user_data = {}
        self.current_scene = None
        self.previous_scene = None
        self.running = True
        self.last_command = None
        self.command_history = []
        self.error_log = []

global_state = GlobalState()
