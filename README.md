# FamilyPet
The Ortega and Engmann households family pet. A hacked and redesigned Roomba to support Alexa command control, orientation and owner tracking, and environment control.
Click the image below to watch the video.
![Watch the video](https://github.com/NickEngmann/FamilyPet/blob/Atom/imgs/youtube.png)
(https://youtu.be/eTrfuwPI7Rg)

# Installation

```bash
pip install python-firebase
pip install requests
```

Then generate a config file for the drive train.
```bash
python configGenerator.py
```

# Running
```bash
python3 atom_controller_interface.py
```

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

# Want to make your own shell for your Roomba?

## Adjusted 3D Print files
Located in the 3Dmodel directory. Follow the instructions in the README.
![3DModel](https://github.com/NickEngmann/FamilyPet/blob/Atom/3Dmodel/3Dmodel.png)

## Instructions on raspberry pi board assembly
http://www.irobot.com/~/media/MainSite/PDFs/About/STEM/Create/Create_2_Serial_to_33V_Logic.pdf
http://www.irobotweb.com/-/media/MainSite/PDFs/About/STEM/Create/RaspberryPi_Tutorial.pdf?la=en

