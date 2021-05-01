#!/bin/bash

# Steps to test this script with your own AWS instances:
# ------------------------------------------------------
#
# First, comment out the line HOSTS="...
# Next, add your own ec2 public IPs.
# Example:
#   HOSTS=("54.162.114.73" "52.87.70.136")
#
# Comment out the KEYS="..." line right under it, and set that to the key file
# Example:
#   KEY=~/.aws/677kp.pem
#
# Now you'll need to modify the username.
# Example:
#   USERNAME=ec2-user
#
# Make sure that your inbound rules on AWS are set to all traffic (-1) for all
# IPs (0.0.0.0/0), or at least the default security group. This just opens up
# every port.
# Finally, run this script and see what happens!
# Example: 'bash run.sh'

# read a list of hosts
# USERNAME=ec2-user
USERNAME=ubuntu
# HOSTS=("54.172.102.164" "54.144.240.179" "34.202.157.206")
HOSTS=("100.25.14.95" "54.237.67.129" "100.26.166.145")
KEY=~/.aws/677kp.pem
# KEY=lab1.pem

catalog1=0
catalog2=1
order1=2
order2=3
frontend=4
service_names=("catalog1" "catalog2" "order1" "order2" "frontend")
service_hosts=()
service_ports=()

# function installs docker if it doesn't exist, and builds each image assuming
# the files have been copied.
function build_docker_on_host() {
    local service_name=$1
    local host=$2
    ssh -i $KEY -l $USERNAME $host "docker -v"
    local status=$?
    if [ $status -ne 0 ]; then
        ssh -i $KEY -l $USERNAME $host "curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh"
        ssh -i $KEY -l $USERNAME $host "sudo groupadd docker"
        ssh -i $KEY -l $USERNAME $host "sudo usermod -aG docker $USERNAME"
    fi
    ssh -i $KEY -l $USERNAME $host "cd ~/bookstore/$service_name/src/; bash docker/docker_builds.sh"
}

# install_docker installs services on a host for a particular service
function install_onto_host() {
    local service_name=$1
    local host=$2
    echo "Installing $service_name onto $host..."
    ssh -i $KEY -l $USERNAME $host "mkdir -p ~/bookstore/$service_name"
    scp -i $KEY -r ../../bookstore/* $USERNAME@$host:~/bookstore/$service_name/

    # now put remote config in the right spot
    scp -i $KEY ./remote_config.yml $USERNAME@$host:~/bookstore/$service_name/src/config.yml
}

# Create trap to kill all docker containers when script is stopped.
# go through host list and according pids
function kill_bookstore() {
    echo "Killing docker containers..."

    # kill pids on each server
    for host in ${HOSTS[@]}; do
        echo "Logging on to $host to kill docker containers..."
        ssh -i $KEY -l ${USERNAME} $host "docker kill \$(docker ps -q)"
    done

}

# create the remote yaml config
rm remote_config.yml
touch remote_config.yml

# First, let's define where each service will be hosted by looping through the
# hosts.
for i in $(seq 0 4); do
    service_host=${HOSTS[$i%${#HOSTS[@]}]}
    service_port=$((10000+$i))
    service_hosts+=($service_host)
    service_ports+=($service_port)
    echo "${service_names[$i]}: \"${service_hosts[$i]}:${service_ports[$i]}\"" >> remote_config.yml
done

echo "Config used for deployment:"
cat remote_config.yml

# Install for each host
install_pids=()
for i in $(seq 0 4); do
    install_onto_host ${service_names[$i]} ${service_hosts[$i]} & install_pids+=($!)
done

# wait for install to finish on each host
wait "${install_pids[@]}"

docker_build_pids=()
# we can build once on each host
for i in $(seq 0 $((${#HOSTS[@]}-1))); do
    build_docker_on_host ${service_names[$i]} ${HOSTS[$i]} & docker_build_pids+=($!)
done

wait "${docker_build_pids[@]}"

# make sure we trap here so services will be killed if exiting
trap kill_bookstore INT TERM EXIT

# start with catalog stuff
for i in $(seq 0 1); do
    ssh -i $KEY -l $USERNAME ${service_hosts[$i]} "docker run -p ${service_ports[$i]}:${service_ports[$i]} catalog ${service_names[$i]}" &
    sleep 0.1s
done

sleep 0.5s

# now do order stuff
for i in $(seq 2 3); do
    ssh -i $KEY -l $USERNAME ${service_hosts[$i]} "docker run -p ${service_ports[$i]}:${service_ports[$i]} order ${service_names[$i]}" &
    sleep 0.1s
done

sleep 0.5s

# now do frontend stuff
for i in $(seq 4 4); do
    ssh -i $KEY -l $USERNAME ${service_hosts[$i]} "docker run -p ${service_ports[$i]}:${service_ports[$i]} frontend" &
    sleep 0.1s
done

sleep 30s