# FamilyPet
The Ortega and Engmann households family pet. A hacked and redesigned Roomba to support Alexa command control, orientation and owner tracking, and environment control. </br>
Click the image below to watch the video.
[![Watch the video](https://github.com/NickEngmann/FamilyPet/blob/Atom/imgs/youtube.png)](https://youtu.be/eTrfuwPI7Rg)

Table of Contents
============
* [Necessary Hardware](#necessary-hardware)
* [Hardware Build](#hardware-build)
* [Software Install](#software-install)
* [Alexa Integration](#alexa-integration)
* [Running](#running)
* [Model](#model)
* [License](#license)

Necessary Hardware
============
<a href="https://www.adafruit.com/product/3055" target="__blank">Raspberry Pi 3 </a></br>
<a href="https://www.adafruit.com/product/801" target="__blank">Adafruit prototyping board </a></br>
<a href="https://www.amazon.com/Adafruit-74LVC245-Breadboard-Friendly-Shifter/dp/B00SK8OC0S" target="__blank">74LVC245 octal bus transceiver</a></br>
<a href="https://www.adafruit.com/product/2438" target="__blank">A 7-pin mini-DIN cable</a></br>
<a href="http://www.irobot.com/About-iRobot/STEM/Create-2.aspx" target="__blank">iCreate2 Robot</a></br>
<a href="https://github.com/NickEngmann/FamilyPet/blob/Atom/3Dmodel/">3D printable files</a>

Hardware build
============
Print out the 3D shell in the <a href="https://github.com/NickEngmann/FamilyPet/blob/Atom/3Dmodel/">3D model directory</a>, then follow the following tutorials to get your iCreate robot to work with your Raspberry Pi 3.
</br>
http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/Create_2_Serial_to_33V_Logic.pdf
http://www.irobotweb.com/-/media/MainSite/PDFs/About/STEM/Create/RaspberryPi_Tutorial.pdf?la=en

Software install
============
To get the Raspberry Pi up and running with our code we need to install the necessary libraries

```bash
python3 -m pip install python-firebase
python3 -m pip install requests
```
Setup I2C on your Raspberry Pi: </br>
https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
</br>

Now you are ready to clone the repo on the Raspberry Pi </br>
```bash
cd ~
git clone https://github.com/NickEngmann/FamilyPet
```
Then generate a config file for the drive train.
```bash
python configGenerator.py
```

Alexa Integration
============
Go to the alexa directory and install node dependencies.
```bash
cd alexa-icarus
npm install
```

Go to firebase and set up a firebase application. Get config data from firebase and save it as config.json </br>

```bash 
config = {
    apiKey: "{api-key}",
    authDomain: "{app-id}.firebaseapp.com",
    databaseURL: "https://{app-id}.firebaseio.com",
    projectId: "{app-id}",
    storageBucket: "{app-id}.appspot.com",
    messagingSenderId: ""
  }
```

Save all items in the folder as a .zip file.

Follow the following instructions from Amazon to set up your own Lambda service and nodejs skill:</br>
https://developer.amazon.com/alexa-skills-kit/alexa-skill-quick-start-tutorial </br>
Load the .zip file into your lambda service </br>

Add the following command configurations to your Alexa skill in the Alexa skill developer portal </br>
## Different Commands we Support:
<b>ComeToMe:</b> </br>
Come to {INSERT NAME HERE} </br>
Go to {INSERT NAME HERE} </br>

<b>CleanUp:</b>  </br>
Atom clean up this mess </br>
Atom clean up this room </br>
Atom clean up after yourself </br>
Atom clean up </br>
Atom clean this room </br>
Atom clean this up </br>
Atom clean now </br>
Atom clean </br>

<b>Tricks:</b> </br>
Atom do tricks </br>
Atom be fancy </br>
Atom do tricks </br>

<b>GoHome:</b> </br>
Atom go home and charge </br>
Atom go charge </br>
Atom you are finished go home to charge </br>
Atom go to your charging station </br>
Atom find your charging station </br>
Atom go back to your charging station </br>
Atom head back to your charging station </br>
Atom go charge yourself </br>
Atom go charge </br>

<b>Speak:</b> </br>
Atom tell me something </br>
Atom speak </br>
Atom how is it going Atom </br>
Atom do you have anything to tell me </br>


Running
============
```bash
python3 atom_controller_interface.py
```

Model
============
# Want to make your own shell for your Roomba?
Located in the <a href="https://github.com/NickEngmann/FamilyPet/blob/Atom/3Dmodel/">3Dmodel</a> directory. Follow the instructions in the README.
![3DModel](https://github.com/NickEngmann/FamilyPet/blob/Atom/3Dmodel/3Dmodel.png)

License
============
The MIT License

Copyright (c) 2004-2018 Quod Certamine

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.