# alexa_pi_jp
Alexa pi with Japanese voice interface

# API
google speech API  
google translate API  
AWS Polly  
Alexa Voice Service  

# status
This project is work in progress.

# environment
[raspbian jessie lite 2017.04.10](https://www.raspberrypi.org/downloads/raspbian/)
python 2.7.9

# install
    sudo apt-get update
    sudo apt-get install vim git
    sudo apt-get install portaudio19-dev python-pyaudio sox swig3.0 vlc
    sudo apt-get install libatlas-base-dev
    git clone https://github.com/haruharuharuby/alexa_pi_jp.git
    cd alexa_pi_jp
    pip install -r requirements.txt

# add google api credentials
    export GOOGLE_APPLICATION_CREDENTIALS=/home/pi/alexa/alexa_pi_jp/tlanslation/xxxxxxxx.json >> ~/.profile


# add AWS credentials
    export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXX >> ~/.profile
    export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXX >> ~/.profile

# run(manually only)
python main.py
