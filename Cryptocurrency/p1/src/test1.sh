#!/bin/bash

echo The name of this cryptocurrency is:
./cryptomoney.sh name
echo Creation of the genesis block
./cryptomoney.sh genesis
echo Creating a wallet for alice into alice.wallet.txt
./cryptomoney.sh generate alice.wallet.txt
export alice=`./cryptomoney.sh address alice.wallet.txt`
echo alice.wallet.txt wallet signature: $alice
echo funding alice wallet with 100
./cryptomoney.sh fund $alice 100 01-alice-funding.txt
echo Creating a wallet for bob into alice.wallet.txt
./cryptomoney.sh generate bob.wallet.txt
export bob=`./cryptomoney.sh address bob.wallet.txt`
echo bob.wallet.txt wallet signature: $bob
./cryptomoney.sh fund $alice 1009 02-alice-funding.txt
./cryptomoney.sh fund $alice 200 03-alice-funding.txt

./cryptomoney.sh generate mike.wallet.txt
export mike=`./cryptomoney.sh address mike.wallet.txt`
./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh balance $mike

./cryptomoney.sh transfer alice.wallet.txt $bob 1200 04-alice-to-bob.txt
./cryptomoney.sh transfer mike.wallet.txt $bob 1200 05-mike-to-bob.txt
echo 2 invalid transactions
./cryptomoney.sh verify alice.wallet.txt 04-alice-to-bob.txt
./cryptomoney.sh verify mike.wallet.txt 05-mike-to-bob.txt

echo verify stuff now
./cryptomoney.sh verify alice.wallet.txt 01-alice-funding.txt
./cryptomoney.sh verify alice.wallet.txt 02-alice-funding.txt
./cryptomoney.sh verify alice.wallet.txt 03-alice-funding.txt
./cryptomoney.sh verify alice.wallet.txt 04-alice-to-bob.txt
echo invalid last one
./cryptomoney.sh verify mike.wallet.txt 05-mike-to-bob.txt


./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh balance $mike

./cryptomoney.sh transfer bob.wallet.txt $mike 300 bob-to-mike.txt
./cryptomoney.sh transfer mike.wallet.txt $bob 100 06-mike-to-bob.txt
./cryptomoney.sh mine 3
echo verify these last two then add to blockchain
./cryptomoney.sh verify bob.wallet.txt bob-to-mike.txt
./cryptomoney.sh verify mike.wallet.txt 06-mike-to-bob.txt

./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh balance $mike

./cryptomoney.sh mine 3


./cryptomoney.sh mine 3
./cryptomoney.sh mine 3
./cryptomoney.sh mine 3
./cryptomoney.sh mine 3

./cryptomoney.sh transfer mike.wallet.txt $bob 10 07-mike-to-bob.txt
echo verify these last two then add to blockchain
./cryptomoney.sh verify mike.wallet.txt 07-mike-to-bob.txt
./cryptomoney.sh mine 3

./cryptomoney.sh balance $alice
./cryptomoney.sh balance $bob
./cryptomoney.sh balance $mike

./cryptomoney.sh mine 3
