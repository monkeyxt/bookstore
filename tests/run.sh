# This script deploys the frontend, order, and catalog server, then sleeps 
# indefinitely and kills the servers when the script terminates.
# Run this script with a config file specifying hosts for each server.
# The file must be named config.yml, though it can be in any directory 
# Example usage: bash run.sh path/to/file/config.yml

# IMPORTANT: be sure to update USERNAME and KEY variables to match the ssh
# credentials of the hosts
USERNAME=ec2-user
KEY=lab1.pem

# Get config file path
config=$1

# Get hosts for each server as well as ip addresses without ports
frontend_host=$(grep -A0 'frontend:' $config | awk '{ print $2}' | tr -d '"')
frontend_ip=$(echo $frontend_host | cut -f1 -d":")

order_host=$(grep -A0 'order:' $config | awk '{ print $2}' | tr -d '"')
order_ip=$(echo $order_host | cut -f1 -d":")

catalog_host=$(grep -A0 'catalog:' $config | awk '{ print $2}' | tr -d '"')
catalog_ip=$(echo $catalog_host | cut -f1 -d":")


echo "Target Server for Frontend: "$frontend_ip
# Install python and required modules
ssh -i $KEY -l ${USERNAME} ${frontend_ip} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
# Create logs folder
ssh -i $KEY -l ${USERNAME} ${frontend_ip} "mkdir -p logs"
# Copy server file and config file
scp -i $KEY "../src/frontend.py" ${USERNAME}@${frontend_ip}:~
scp -i $KEY $config ${USERNAME}@${frontend_ip}:~
# Run server and reteive its PID
frontend_pid=($(ssh -i $KEY -l ${USERNAME} ${frontend_ip} "python3 frontend.py &> frontend_log.txt & echo \$! &"))
echo $frontend_pid


echo "Target Server for Order: "$order_ip
# Install python and required modules
ssh -i $KEY -l ${USERNAME} ${order_ip} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
# Create logs folder
ssh -i $KEY -l ${USERNAME} ${order_ip} "mkdir -p logs"
# Copy server file and config file
scp -i $KEY "../src/order.py" ${USERNAME}@${order_ip}:~
scp -i $KEY $config ${USERNAME}@${order_ip}:~
# Run server and reteive its PID
order_pid=($(ssh -i $KEY -l ${USERNAME} ${order_ip} "python3 order.py &> order_log.txt & echo \$! &"))
echo $order_pid

echo "Target Server for Catalog: "$catalog_ip
# Install python and required modules
ssh -i $KEY -l ${USERNAME} ${catalog_ip} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
# Create logs folder
ssh -i $KEY -l ${USERNAME} ${catalog_ip} "mkdir -p logs"
# Copy server file and config file
scp -i $KEY "../src/catalog.py" ${USERNAME}@${catalog_ip}:~
scp -i $KEY $config ${USERNAME}@${catalog_ip}:~
# Run server and reteive its PID
catalog_pid=($(ssh -i $KEY -l ${USERNAME} ${catalog_ip} "python3 catalog.py &> catalog_log.txt & echo \$! &"))
echo $catalog_pid

# Function/trap to kill servers when this script terminates
function kill_servers() {
    ssh -i $KEY -l ${USERNAME} ${frontend_ip} "kill $frontend_pid"
    ssh -i $KEY -l ${USERNAME} ${order_ip} "kill $order_pid"
    ssh -i $KEY -l ${USERNAME} ${catalog_ip} "kill $catalog_pid"
}
trap kill_servers INT TERM EXIT

# Sleep indefinitely
sleep infinity