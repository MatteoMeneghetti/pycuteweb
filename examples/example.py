from pycuteweb import Application
import threading
# sudo apt install --reinstall libxcb-xinerama0

if __name__ == '__main__':
    app = Application()
    app.addSplashScreen("./galileo.jpg")
    app.spawn_window("https://www.meneghetti.dev")
    app.start()
