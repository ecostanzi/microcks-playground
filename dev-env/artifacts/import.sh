#!/bin/bash

shopt -s nullglob

import_specs() {
    local dir="$1"
    local main_flag="$2"
    echo "importing $dir as main $2"

    for spec in "$dir"/*.yaml; do
        [[ -e "$spec" ]] || break
        echo "importing $spec"
        microcks-cli import "$spec:$main_flag" \
            --microcksURL=http://microcks:8080/api \
            --insecure \
            --keycloakClientId=foo \
            --keycloakClientSecret=bar
    done
}

declare -A dirs=(
    ["/microcks/artifacts/main"]="true"
    ["/microcks/artifacts/secondary"]="false"
)

for dir in "${!dirs[@]}"; do
    import_specs "$dir" "${dirs[$dir]}"
done
