from app import App
from setup import Setup
from gpio.service import GPIO

Setup(GPIO).set()
App(GPIO).start()
