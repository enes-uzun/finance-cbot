  #!/bin/bash -xe
  sudo apt update
  sudo apt-add-repository universe -y
  sudo apt install -y git
  sudo apt install -y awscli
  API_KEY=$(aws --region eu-west-2 ssm get-parameter --name "/gpt_api_key" --with-decryption --query "Parameter.Value" --output text)
  sudo apt install -y python3
  sudo git clone https://github.com/ML-std/finance-cbot.git
  sudo cd ./finance-cbot
  sudo sed -i "s/OPEN_AI_KEY/$API_KEY/" stockGPT.py
  sudo apt install python-pip
  sudo pip install -r requirements.txt
  sudo nohup streamlit run stockGPT.py
