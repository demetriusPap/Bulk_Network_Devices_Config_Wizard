# Bulk_Network_Devices_Config_Wizard

A project that is at an early stage of development.

An ambitious attempt to make a nagios wizard work with python scripts and use nagios' api.

Requirements: Python3.6 and packages: netmiko , pandas , requests , xlrd must be installed on your nagios server.

Commands:

    ' sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm '

    ' sudo yum -y install python36u '

    ' sudo yum -y install python36u-pip '

    ' sudo pip3.6 install netmiko ' 

    ' sudo pip3.6 install pandas '

    ' sudo pip3.6 install requests '

    ' sudo pip3.6 install xlrd '

# Wizard Installation

Zip 'wizardbnd' folder.

Log in to your nagios server's interface.

Then navigate to "Admin > System Extensions > Manage Config Wizards".

Click the Browse button to select the 'wizardbnd.zip' file you have just created.

Click Open and then click the  Upload & Install button to upload the configuration wizard.

Once our wizard is uploaded, you will receive a message saying it was installed and it will appear in
the list of wizards.

Now when you Navigate back to the Configure menu you will see the new wizard in the list.



