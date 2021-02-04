#!/bin/bash

cd /app/application_name/build
cmake ..
make

#build/add source
echo '<h1>Hello Drogon!</h1>' >>index.html
./application_name