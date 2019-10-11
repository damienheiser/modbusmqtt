init:
	pip3 install -r requirements.txt

install:
	echo "Installing service."
	sudo sed  's|{path}|'${PWD}'|' ./setup/shinemonitor.service /etc/systemd/system/shinemonitor.service
	sudo systemctl enable shinemonitor.service
	sudo systemctl start shinemonitor.service
	echo "Done."