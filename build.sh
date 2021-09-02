#! /bin/sh
cp /media/sf_share/chemtek/chemtek_linux_ARM_GUI.py .
#cp /media/sf_share/chemtek/Release.py chemtek_linux_ARM_GUI.py

str1="dll_name = \"lib_linux_ARM_1.0.15.so\""
str2="#dll_name = \"lib_linux_ARM_1.0.15.so\""
sed -i "s/$str1/$str2/g" chemtek_linux_ARM_GUI.py

str3="#dll_name = \"lib_linux_X64_1.0.15.so\""
str4="dll_name = \"lib_linux_X64_1.0.15.so\""
sed -i "s/$str3/$str4/g" chemtek_linux_ARM_GUI.py

str5="hand = c_void_p(0)"
str6="hand = c_uint64(0)"
sed -i "s/$str5/$str6/g" chemtek_linux_ARM_GUI.py

str7="import RPi.GPIO as GPIO"
str8="#import RPi.GPIO as GPIO"
sed -i "s/$str7/$str8/g" chemtek_linux_ARM_GUI.py

str9="if Serial_mode == 0 : #RS232"
str10="#if Serial_mode == 0 : #RS232"
sed -i "s/$str9/$str10/g" chemtek_linux_ARM_GUI.py

str11="self.RS232_initial()"
str12="#self.RS232_initial()"
sed -i "s/$str11/$str12/g" chemtek_linux_ARM_GUI.py

str13="elif Serial_mode == 1 : #RS485"
str14="#elif Serial_mode == 1 : #RS485"
sed -i "s/$str13/$str14/g" chemtek_linux_ARM_GUI.py

str15="self.RS485_initial()"
str16="#self.RS485_initial()"
sed -i "s/$str15/$str16/g" chemtek_linux_ARM_GUI.py

str17="self.ser.write(buffer_string)"
str18="#self.ser.write(buffer_string)"
sed -i "s/$str17/$str18/g" chemtek_linux_ARM_GUI.py

str19="root.overrideredirect(1)    #toolbar 隱藏"
str20="#root.overrideredirect(1)    #toolbar 隱藏"
sed -i "s/$str19/$str20/g" chemtek_linux_ARM_GUI.py

str21="root.attributes('-fullscreen', True)"
str22="#root.attributes('-fullscreen', True)"
sed -i "s/$str21/$str22/g" chemtek_linux_ARM_GUI.py

str23="if max(buffer)>5000 :"
str24="if max(buffer)>10 :"
sed -i "s/$str23/$str24/g" chemtek_linux_ARM_GUI.py

#cp /media/sf_share/chemtek/setup.ini .
cp /media/sf_share/chemtek/config.ini .
cp /media/sf_share/chemtek/HB/dark .

sudo python3 chemtek_linux_ARM_GUI.py
