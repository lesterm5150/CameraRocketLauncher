import usb.core
import usb.util

vendorID = 0x2123
productID = 0x1010

dev = None
backend = usb.backend.libusb1.get_backend(find_library=lambda x: "C:\Windows\System32\drivers\libusb0.dll")
while dev is None:
        dev = usb.core.find(idVendor=0x2123, idProduct=0x1010, backend = backend)

print("Dev Found")

