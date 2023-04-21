// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from "next";
import { HID } from "node-hid";

type Data = {
  gyroX: number;
  gyroY: number;
  gyroZ: number;
  distance1: number;
  distance2: number;
  buttonPressed: boolean;
};

const VENDOR_ID = 0x1234;
const PRODUCT_ID = 0x5678;
const REPORT_SIZE = 9;

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  const device = new HID(VENDOR_ID, PRODUCT_ID);
  device.on("data", (data) => {
    const reportId = data[0];
    const gyroX = data.readInt16LE(1);
    const gyroY = data.readInt16LE(3);
    const gyroZ = data.readInt16LE(5);
    const distance1 = data[7];
    const distance2 = data[8];
    const buttonPressed = data[6] !== 0;

    device.pause();

    res.status(200).json({
      gyroX,
      gyroY,
      gyroZ,
      distance1,
      distance2,
      buttonPressed,
    });
  });
}
