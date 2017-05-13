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
python 3.6.0

# install
    sudo apt-get install portaudio19-dev
    sudo apt-get install python3-pyaudio
    sudo apt-get install vlc
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
