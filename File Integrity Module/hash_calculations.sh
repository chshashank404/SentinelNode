#!/bin/sh

critical_files="
/algod/Wallet1.0.30000.partkey
/algod/Wallet1.rootkey
/algod/data/config.json
/algod/data/genesis.json
/algod/data/algod.token
/algod/data/kmd.token
/algod/data/logging.config
/etc/algorand/config.json
/etc/pam.d/common-auth
/etc/security/limits.conf
/etc/systemd/system/algorand.service
/etc/ssl/private/ssl-cert.key
"

for file in $critical_files; do
    if [ -f "$file" ]; then
        sha256sum "$file"
    else
        echo "File not found: $file"
    fi
done
