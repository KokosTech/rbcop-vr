import cv2
import RPi.GPIO as GPIO
import uvicorn
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import Response, StreamingResponse
from fastapi.templating import Jinja2Templates

en1 = 25
in1 = 23
in2 = 24

en2 = 22
in3 = 17
in4 = 27

lowSpeed = 50
medSpeed = 75
maxSpeed = 100

pwm_en_1 = None
pwm_en_2 = None


def setup():
    GPIO.cleanup()

    global pwm_en_1, pwm_en_2

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(en1, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

    GPIO.setup(en2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)

    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

    pwm_en_1 = GPIO.PWM(en1, 1000)
    pwm_en_2 = GPIO.PWM(en2, 1000)

    pwm_en_1.start(65)
    pwm_en_2.start(65)


def enable_movement():
    GPIO.output(en1, GPIO.HIGH)
    GPIO.output(en2, GPIO.HIGH)


def forward(pin1: int, pin2: int):
	GPIO.output(pin1, GPIO.HIGH)
	GPIO.output(pin2, GPIO.LOW)


def backward(pin1: int, pin2: int):
	GPIO.output(pin1, GPIO.LOW)
	GPIO.output(pin2, GPIO.HIGH)


def stop(pin1: int, pin2: int):
	GPIO.output(pin1, GPIO.LOW)
	GPIO.output(pin2, GPIO.LOW)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


class Movement:
    sensor: str
    angle_data: list


class CameraCapture:
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


@app.get('/')
def index(request: Request):
    return {"hello": "world"}


@app.get('/video_feed')
def video_feed():
    return StreamingResponse(camera.gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')


@app.get('/snap')
def snap_pic():
    return Response(camera.snap(), media_type='image/jpeg')


@app.post('/movement')
async def move(request: Request):
    json = await request.json()

    if json['angle_data'][0] >= 7:
        forward(in1, in2)
        stop(in3, in4)
        print('rigth')

    elif json['angle_data'][0] <= -7:
        print('left')
        forward(in3, in4)
        stop(in1, in2)
    elif json['angle_data'][1] <= -5:
        print('backward')
        backward(in1, in2)
        backward(in3, in4)
    elif json['angle_data'][1] >= 5:
        forward(in1, in2)
        forward(in3, in4)
        print('forward')
    else:
        print('stop')
        stop(in1, in2)
        stop(in3, in4)

if __name__ == '__main__':
    setup()
    enable_movement()
    uvicorn.run(app, host='0.0.0.0', port=8000)
