# [Thrive](https://www.thrivebureau.com "Thrive ERP's Homepage") Install Script

This script will also give you the ability to define an xmlrpc_port in the .conf file that is generated under /etc/
This script can be safely used in a multi-thrive code base server because the default port is changed BEFORE the ERP is started.


##### 1. Download the script:

Thrive Bureau ERP
open ports:
8069-App
8074 - logs

For installation in VPS server use these three lines, in the end of the installation process, when asking for GitHub user id: then input your GitHub email then input your password, it will install thrive_bureau_erp.

login to vps terminal then insert three lines then it will start automatically start the installation process

sudo apt-get update -y

sudo apt-get upgrade -y

sudo apt -y install net-tools vim screen curl tcpdump sysstat wget telnet bmon htop mlocate

step 1)
sudo wget https://raw.githubusercontent.com/u16052642/thrive_erp_install_script/main/thrive1669_install.sh

step 2)
sudo chmod +x thrive1669_install.sh

step 3)
sudo ./thrive1669_install.sh

step 4)
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb

sudo apt install -f ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb -y


after finishing installation you will see the (yourvpsip):8069 then you should provide the master password then use database name and user id and password


vi /etc/thrive1669-server.conf

addons:

/thrive1669/custom/addons/new/finance,/thrive1669/custom/addons/new/hr,/thrive1669/custom/addons/new/inventory_mrp,/thrive1669/custom/addons/new/marketing,/thrive1669/custom/addons/new/miscellaneous,/thrive1669/custom/addons/new/productivity,/thrive1669/custom/addons/new/reporting,/thrive1669/custom/addons/new/sales,/thrive1669/custom/addons/new/services,/thrive1669/custom/addons/new/website



when need manually start restart or stop then use this command:

sudo /etc/init.d/thrive1669-server restart

sudo /etc/init.d/thrive1669-server stop

sudo /etc/init.d/thrive1669-server start

sudo /etc/init.d/thrive1669-server force-reload


log file:

tail -400f /var/log/thrive1669/thrive1669-server.log

python addons: 

sudo apt install python3-pandas -y

sudo apt install python3-geopy -y

sudo apt install python3-cachetools -y

pip3 install pdfminer.six
