sudo sed -i 's/noquiet splash"/noquiet splash 3"/g' /etc/default/grub
sudo update-grub
sudo apt install -y xfce4-session xfce4-goodies x11-apps xfce4-panel xinit
sudo apt install qterminal firefox

echo 'export PYTHONPATH="${PYTHONPATH}:'$(pwd)'"
if [[ "$(tty)" = "/dev/tty1" ]]; then
	pgrep xfce || startxfce4
fi' >> ~/.bashrc
