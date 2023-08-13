# thrive_bureau_erp
Thrive Bureau ERP

For installation in vps server use this three line, in end of the installation process, when ask for github user id: then input your github email then input password, it will install thrive_bureau_erp.

login to vps terminal then insert three line then it will start automatically start the installation process

step 1)
sudo wget https://github.com/u16052642/thrive_erp_install_script/blob/main/thrive1669_install.sh

step 2)
sudo chmod +x thrive1669_install.sh

step 3)
sudo ./thrive1669_install.sh


after finsih installation you will see the (yourvpsip):8069 then you should provide master password then use database name and user id and password

when need mannually start restart or stop then use this command

sudo /etc/init.d/thrive1669-server restart
sudo /etc/init.d/thrive1669-server stop
sudo /etc/init.d/thrive1669-server start
