path="/home/ckb/gp/ckb-light-client/target/release/test1"
cd $path
kill $(lsof -t -i:9000)
rm -rf data
cat testnet.log | grep ERR >> error.log
RUST_LOG=info,ckb_light_client=trace ./ckb-light-client run --config-file ./testnet.toml > testnet.log 2>&1 &
sleep 60
curl http://localhost:9000/ -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method":"get_scripts", "params": [], "id": 1}'
curl http://localhost:9000/ -X POST -H "Content-Type: application/json" -d '{"jsonrpc": "2.0", "method":"set_scripts", "params": [[{"script": {"code_hash": "0x9bd7e06f3ecf4be0f2fcd2188b23f1b9fcc88e5d4b65a8637b17723bbda3cce8", "hash_type": "type", "args": "0xda648442dbb7347e467d1d09da13e5cd3a0ef0e1"}, "script_type": "lock", "block_number": "0x0"}]], "id": 1}'