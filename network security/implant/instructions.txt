I created an implant python file that has similar features to a Meterpreter. It logs your keystrokes, takes a screenshot (when you press escape), and will use the web camera to record you and send the frames over an encrypted channel. 

How to run: Use two terminals to run the python files. Run the web camera file first, then run implant.py with root permission. You can see the frames get sent over in the terminal after you press the escape key. After running, you can see the screenshot and keystrokes captured in new files that have been created in the same directory. 

The web camera code is not mine. That has a minor bug in it with how it records. 

Youtube Demo: https://www.youtube.com/watch?v=eUwjWj5gUeQ 

Environment: I am running a MacBook Pro with Ventura 13.5.1. 