source ${HOME}/.bashrc

cd /home/ec2-user/hoikuen-jisan/
source venv/bin/activate
python notify_jisan.py weekly
deactivate