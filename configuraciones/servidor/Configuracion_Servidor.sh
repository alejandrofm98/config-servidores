# Nos damos admin
sudo -i
#Actualizamos todas las dependencias
dnf update -y

#Instalamos docker
dnf config-manager --add-repo=https://download.docker.com/linux/centos/docker-ce.repo
dnf install docker-ce -y

systemctl start docker
systemctl enable docker

systemctl status docker


#instalamos curl
dnf install -y curl
#descargamos docker compose
curl -L  https://github.com/docker/compose/releases/download/v2.26.0/docker-compose-linux-aarch64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version

#Activar borrado usando patrones
shopt -s extglob

#Subimos la carpeta proyectos a /home/opc/

#DAR PERMISOS de docker al usuario opc
sudo groupadd docker
sudo usermod -aG docker ${USER}
su -s ${USER}

#Instalar sshfs

sudo dnf config-manager --set-enabled ol8_codeready_builder
sudo dnf install fuse-sshfs
