find ./proto -name "*.proto" | while read file; do
  dir=$(dirname "$file")
  protoc \
    --proto_path=./proto \
    --go_out="$dir" \
    --go-grpc_out="$dir" \
    "$file"
done
