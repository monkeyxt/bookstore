config=$1
frontend_host=$(grep -A0 'frontend:' $config | awk '{ print $2}' | tr -d '"')
order_host=$(grep -A0 'order:' $config | awk '{ print $2}' | tr -d '"')
catalog_host=$(grep -A0 'catalog:' $config | awk '{ print $2}' | tr -d '"')
USERNAME=ec2-user
KEY=lab1.pem


echo "Target Server for Frontend: "$frontend_host
ssh -i $KEY -l ${USERNAME} ${frontend_host} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
ssh -i $KEY -l ${USERNAME} ${frontend_host} "mkdir -p logs"
scp -i $KEY "../src/frontend.py" ${USERNAME}@${frontend_host}:~
scp -i $KEY "../src/config.yml" ${USERNAME}@${frontend_host}:~
ssh -i $KEY -l ${USERNAME} ${frontend_host} "cd ~ && python3 frontend.py &"
frontend_pid=$(ssh -i $KEY -l ${USERNAME} ${frontend_host} "echo \$!")
echo $frontend_pid

echo "Target Server for Order: "$order_host
ssh -i $KEY -l ${USERNAME} ${order_host} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
ssh -i $KEY -l ${USERNAME} ${order_host} "mkdir -p logs"
scp -i $KEY "../src/order.py" ${USERNAME}@${order_host}:~
scp -i $KEY "../src/config.yml" ${USERNAME}@${order_host}:~
ssh -i $KEY -l ${USERNAME} ${order_host} "cd ~ && python3 order.py &"
order_pid=$(ssh -i $KEY -l ${USERNAME} ${order_host} "echo \$!")
echo $order_pid

echo "Target Server for Frontend: "$catalog_host
ssh -i $KEY -l ${USERNAME} ${catalog_host} "sudo yum install python3 -y && sudo pip3 install pyyaml requests flask"
ssh -i $KEY -l ${USERNAME} ${catalog_host} "mkdir -p logs"
scp -i $KEY "../src/catalog.py" ${USERNAME}@${catalog_host}:~
scp -i $KEY "../src/config.yml" ${USERNAME}@${catalog_host}:~
ssh -i $KEY -l ${USERNAME} ${catalog_host} "cd ~ && python3 catalog.py &"
catalog_pid=$(ssh -i $KEY -l ${USERNAME} ${catalog_host} "echo \$!")
echo $catalog_pid

function kill_servers() {
    ssh -i $KEY -l ${USERNAME} ${frontend_host} "kill $frontend_pid"
    ssh -i $KEY -l ${USERNAME} ${order_host} "kill $order_pid"
    ssh -i $KEY -l ${USERNAME} ${catalog_host} "kill $catalog_pid"
}
trap kill_servers INT TERM EXIT