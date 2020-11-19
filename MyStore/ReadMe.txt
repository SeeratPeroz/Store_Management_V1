+================================================================================================+
|                                                                                                |
|                                 STORE MANAGEMENT SYSTEM                                        |
|                                                                                                |
+================================================================================================+

    1. Install Python (https://www.python.org/downloads/)
        NOTE: Add path while install Python
    2. Open CMD and install following requirements:
        a) pip install django
        b) pip install opencv-python
        c) pip install pyzbar
        d) pip install cv2
        e) pip install pisa
        f) pip install xhtml2pdf
        g) pip install -r requirements.txt



    NOTE: if pip doesn't work in your case then you can use pip3,pe3.8 or any other version of pip you have.
    NOTE: you need an external camera for this project. if you don't then change the ( camera = cv2.VideoCapture(1) )
          to ( camera = cv2.VideoCapture(0) ) to use the webcam of your laptop.
