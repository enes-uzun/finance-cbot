  #!/bin/bash -xe
  export DEBIAN_FRONTEND=noninteractive
  sudo apt update
  sudo apt-add-repository universe -y
  sudo apt install -y git --assume-yes
  sudo apt install -y python3 --assume-yes
  sudo git clone https://github.com/ML-std/finance-cbot.git
  cd ./finance-cbot
  sudo sed -i "s/OPEN_AI_KEY/$API_KEY/" stockGPT.py
  sudo apt install python3-pip -y --assume-yes
  sudo pip install -r requirements.txt
  sudo nohup streamlit run stockGPT.py &
