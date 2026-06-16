# To connect my VM
ssh -i "C:\Users\ARUNKUMAR\Downloads\my-sys_key.pem" azureuser@74.225.252.211

# update and download nginx
sudo apt update
sudo apt upgrade -y
sudo apt install git curl nginx -y

# update and download docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
docker --version

# Git repo
git clone https://github.com/ARUNKUMAR2202/Devops.git


# View running containers
docker ps

# View logs
docker logs -f flask-app-test

# Stop container
docker stop flask-app-test

# Start container
docker start flask-app-test

# Remove container
docker rm -f flask-app-test

# Rebuild image
docker build -t flask-app .

# Run container
docker run -d --name flask-app-test -p 8080:8080 flask-app