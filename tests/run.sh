config=$1
frontend_host=$(grep -A0 'frontend:' $config | awk '{ print $2}' | tr -d '"')
frontend_ip=$(echo $frontend_host | cut -f1 -d":")

order_host=$(grep -A0 'order:' $config | awk '{ print $2}' | tr -d '"')
order_ip=$(echo $order_host | cut -f1 -d":")

catalog_host=$(grep -A0 'catalog:' $config | awk '{ print $2}' | tr -d '"')
catalog_ip=$(echo $catalog_host | cut -f1 -d":")

USERNAME=ec2-user
KEY=lab1.pem


echo "Target Server for Frontend: "$frontend_ip
ssh -i $KEY -l ${USERNAME} ${frontend_ip} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
ssh -i $KEY -l ${USERNAME} ${frontend_ip} "mkdir -p logs"
scp -i $KEY "../src/frontend.py" ${USERNAME}@${frontend_ip}:~
scp -i $KEY "../src/config.yml" ${USERNAME}@${frontend_ip}:~
ssh -i $KEY -l ${USERNAME} ${frontend_ip} "python3 frontend.py &"
frontend_pid=$(ssh -i $KEY -l ${USERNAME} ${frontend_ip} "echo \$!")
echo $frontend_pid

echo "Target Server for Order: "$order_ip
ssh -i $KEY -l ${USERNAME} ${order_ip} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
ssh -i $KEY -l ${USERNAME} ${order_ip} "mkdir -p logs"
scp -i $KEY "../src/order.py" ${USERNAME}@${order_ip}:~
scp -i $KEY "../src/config.yml" ${USERNAME}@${order_ip}:~
ssh -i $KEY -l ${USERNAME} ${order_ip} "python3 order.py &"
order_pid=$(ssh -i $KEY -l ${USERNAME} ${order_ip} "echo \$!")
echo $order_pid

echo "Target Server for Frontend: "$catalog_ip
ssh -i $KEY -l ${USERNAME} ${catalog_ip} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
ssh -i $KEY -l ${USERNAME} ${catalog_ip} "mkdir -p logs"
scp -i $KEY "../src/catalog.py" ${USERNAME}@${catalog_ip}:~
scp -i $KEY "../src/config.yml" ${USERNAME}@${catalog_ip}:~
ssh -i $KEY -l ${USERNAME} ${catalog_ip} "python3 catalog.py &"
catalog_pid=$(ssh -i $KEY -l ${USERNAME} ${catalog_ip} "echo \$!")
echo $catalog_pid

function kill_servers() {
    ssh -i $KEY -l ${USERNAME} ${frontend_ip} "kill $frontend_pid"
    ssh -i $KEY -l ${USERNAME} ${order_ip} "kill $order_pid"
    ssh -i $KEY -l ${USERNAME} ${catalog_ip} "kill $catalog_pid"
}
trap kill_servers INT TERM EXIT