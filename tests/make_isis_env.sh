#!/usr/bin/env bash
ROOT_DIR=/tmp/pysis

mkdir -p $ROOT_DIR/isis
mkdir -p $ROOT_DIR/isis/bin
mkdir -p $ROOT_DIR/data
mkdir -p $ROOT_DIR/testData

echo '3.4.8.6010
2014-11-26   # Version date
v002         # 3rd party libraries version
stable       # release stage (alpha, beta, stable)
' > $ROOT_DIR/isis/version

echo '#!/usr/bin/env bash
echo $@
' > $ROOT_DIR/isis/bin/isis_echo

echo '#!/usr/bin/env bash
true
' > $ROOT_DIR/isis/bin/isis_true

echo '#!/usr/bin/env bash
false
' > $ROOT_DIR/isis/bin/isis_false

chmod +x $ROOT_DIR/isis/bin/isis_echo
chmod +x $ROOT_DIR/isis/bin/isis_true
chmod +x $ROOT_DIR/isis/bin/isis_false
