import cv2
import RPi.GPIO as GPIO
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import Response, StreamingResponse
from pydantic import BaseModel
from gpiozero import Motor
from dotenv import load_dotenv
load_dotenv()
import os

# define pin constants
enA = 22
in1 = 17
in2 = 27

enB = 25
in3 = 23
in4 = 24

# define speed
speed = 0.65


motorA = motorB = None

# setup gpio pins
def setup():
    global motorA, motorB
    
    # define the motor objects
    motorA = Motor(in2, in1, enable=enA, pwm=True)
    motorB = Motor(in4, in3, enable=enB, pwm=True)

app = FastAPI()

class Movement(BaseModel):
    sensor: str
    angle_data: list


class CameraCapture:
    # 
    camera = cv2.VideoCapture(0)

    def gen_frames(self):
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


camera = CameraCapture()

# define a controller route for video
@app.get('/video_feed')
def video_feed():
    return StreamingResponse(camera.gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


# define a controller route for the movements
@app.post('/movement')
def move(movement: Movement):
    if movement.angle_data[0] >= 390:
        motorA.forward(speed)
        motorB.stop()
        print('rigth')
    elif movement.angle_data[0] <= 300:
        motorA.stop()
        motorB.forward(speed)
        print('left')
    elif movement.angle_data[1] <= 290:
        motorA.backward(speed)
        motorB.backward(speed)
        print('backward')
    elif movement.angle_data[1] >= 390:
        motorA.forward(speed)
        motorB.forward(speed)
        print('forward')
    else:
        motorA.stop()
        motorB.stop()
        print('stop')

if __name__ == '__main__':
    # call the setup function to initialize the pins
    setup()
    # run the server
    uvicorn.run(app, host=os.environ.get("host"), port=int(os.environ.get("port")))
    # cleanup the gpio pins
    GPIO.cleanup()
