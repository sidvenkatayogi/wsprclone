import threading
from src.app import WsprEditApp
from src.transcription import load_model

if __name__ == "__main__":
    app = WsprEditApp()
    
    model_thread = threading.Thread(target=load_model, daemon=True)
    model_thread.start()
    
    listener_thread = threading.Thread(target=app.run_hotkey_listener, daemon=True)
    listener_thread.start()

    app.run()
