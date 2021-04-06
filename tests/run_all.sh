c_tests=`ls concurrent`
for test in $c_tests
do
    echo "Deploying servers for concurrent test: $test..."
    bash run.sh ../src/config.yml &
    sleep 25s
    run_pid=$!
    cd concurrent
    echo "Running $test..."
    bash $test
    cd ..
    kill $run_pid
done

s_tests=`ls sequential`
for test in $s_tests
do
    echo "Deploying servers for sequential test: $test..."
    bash run.sh ../src/config.yml &
    sleep 25s
    run_pid=$!
    cd sequential
    echo "Running $test..."
    bash $test
    cd ..
    kill $run_pid
done

function kill_run() {
    kill $run_pid
}
trap kill_run INT TERM EXIT