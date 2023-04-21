"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";
import Webcam from "react-webcam";

interface HIDRequestFilters {
  vendorId?: number;
  productId?: number;
  usagePage?: number;
  usage?: number;
}

interface HIDDeviceRequestOptions {
  filters: HIDRequestFilters[];
}

interface HIDDevice {
  opened: boolean;
  close(): void;
  sendReport(reportId: number, data: BufferSource): Promise<void>;
  receiveFeatureReport(reportId: number, length: number): Promise<DataView>;
  sendFeatureReport(reportId: number, data: BufferSource): Promise<void>;
  addEventListener(
    type: "inputreport",
    listener: (this: HIDDevice, event: HIDInputReportEvent) => void,
    options?: boolean | AddEventListenerOptions
  ): void;
  removeEventListener(
    type: "inputreport",
    listener: (this: HIDDevice, event: HIDInputReportEvent) => void,
    options?: boolean | EventListenerOptions
  ): void;
}

interface HIDInputReportEvent extends Event {
  reportId: number;
  data: DataView;
}

interface NavigatorHID {
  requestDevice(options: HIDDeviceRequestOptions): Promise<HIDDevice>;
  readonly onconnect: ((this: NavigatorHID, event: Event) => void) | null;
  readonly ondisconnect: ((this: NavigatorHID, event: Event) => void) | null;
}

interface Navigator {
  readonly hid: NavigatorHID;
}

const VENDOR_ID = 0x1234;
const PRODUCT_ID = 0x5678;
const REPORT_SIZE = 9;

export default function Home() {
  const [gyroX, setGyroX] = useState(0);
  const [gyroY, setGyroY] = useState(0);
  const [gyroZ, setGyroZ] = useState(0);
  const [distance1, setDistance1] = useState(0);
  const [distance2, setDistance2] = useState(0);
  const [buttonPressed, setButtonPressed] = useState(false);
  const [videoSource, setVideoSource] = useState<MediaStream | null>(null);

  const switchWebcam = () => {
    if (videoSource) {
      // Stop current video stream
      videoSource.getTracks().forEach((track) => {
        track.stop();
      });
    }
    // Switch to built-in webcam
    navigator.mediaDevices
      .getUserMedia({ video: { facingMode: "user" } })
      .then((stream) => {
        setVideoSource(stream);
      });
  };


  const allowHID = async () => {
    try {
      const device = await navigator.hid.requestDevice({
        filters: [
          {
            vendorId: VENDOR_ID,
            productId: PRODUCT_ID,
          },
        ],
      });

      if (device) {
        await device.open();
        device.addEventListener("inputreport", (event) => {
          const reportId = event.reportId;
          const view = new DataView(event.data.buffer);
          const gyroX = view.getInt16(1, true);
          const gyroY = view.getInt16(3, true);
          const gyroZ = view.getInt16(5, true);
          const distance1 = view.getUint8(7);
          const distance2 = view.getUint8(8);
          const buttonPressed = view.getUint8(6) !== 0;

          // Update component state
          setGyroX(gyroX);
          setGyroY(gyroY);
          setGyroZ(gyroZ);
          setDistance1(distance1);
          setDistance2(distance2);
          setButtonPressed(buttonPressed);

          // Switch video source if button is pressed
          if (buttonPressed) {
            if (videoSource) {
              // Stop current video stream
              videoSource.getTracks().forEach((track) => {
                track.stop();
              });
            }
            // Switch to built-in webcam
            navigator.mediaDevices
              .getUserMedia({ video: { facingMode: "user" } })
              .then((stream) => {
                setVideoSource(stream);
              });
          } else {
            // Switch back to default video source
            navigator.mediaDevices

              .getUserMedia({ video: true })
              .then((stream) => {
                setVideoSource(stream);
              });
          }
        });
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <main className={styles.main}>
      <p>Gyro X: {gyroX}</p>
      <p>Gyro Y: {gyroY}</p>
      <p>Gyro Z: {gyroZ}</p>
      <p>Distance 1: {distance1}</p>
      <p>Distance 2: {distance2}</p>
      <p>Button Pressed: {buttonPressed ? "Yes" : "No"}</p>
      <button onClick={switchWebcam}>Allow HID</button>
      {videoSource ? (
        <>
          <Webcam
            videoConstraints={{
              deviceId: videoSource.getVideoTracks()[0].getSettings().deviceId,
            }}
          />
          <Webcam
            videoConstraints={{
              deviceId: videoSource.getVideoTracks()[0].getSettings().deviceId,
            }}
          />
        </>
      ) : (
        <>
          <img src="http://78.90.5.61:8000/video_feed" />
          <img src="http://78.90.5.61:8000/video_feed" />
        </>
      )}
    </main>
  );
}
