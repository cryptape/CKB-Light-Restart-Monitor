path="/home/ckb/gp/ckb-light-client/target/release/test1"
cd $path
kill $(lsof -t -i:9000)
rm -rf data
cat testnet.log | grep ERR >> error.log
RUST_LOG=info,ckb_light_client=trace ./ckb-light-client run --config-file ./testnet.toml > testnet.log 2>&1 &