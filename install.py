import os
ruta = os.getcwd()

##Instalacion de la herramienta BlackWidow
blackWidow = os.getcwd() + "/BlackWidow/"
os.system("git clone https://github.com/1N3/BlackWidow")
os.chdir(blackWidow)
os.system("./install.sh")
os.chdir(ruta)
os.system("rm -R BlackWidow")

##Instalacion de la herramienta a2sv
a2sv = os.getcwd() + "/a2sv/"
os.system("git clone https://github.com/hahwul/a2sv.git")
os.chdir(a2sv)
os.system("./install.sh")
os.chdir(ruta)

##instalacion herramienta joomscan
os.system("apt-get install joomscan -y")

##instalacion herramienta wpscan
os.system("gem install wpscan")

##Permisos check_freak.sh
os.system("chmod +x check_freak.sh")

##Instalar flash
os.system("pip3 install flask")

##Instalar flash
os.system("pip3 install flask-ngrok")