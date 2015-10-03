#!/bin/bash
#
# install the Google Material Design Icons to /var/icons
#

# must be run as root
if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root" 1>&2
  exit 1
fi

# array of directorys in the gmdi
declare -a dirs=("action" "alert" "av" "communication" "content" "device" "editor" "file" "hardware" "image" "maps" "navigation" "notification" "social" "toggle")

# clone the git
git clone https://www.github.com/google/material-design-icons
cd material-design-icons

# create the /var/icons dir
mkdir /var/icons

# iterate through all the dirs
for i in "${dirs[@]}"; do
  mkdir /var/icons/$i
  cd $i
  cp drawable-mdpi/* /var/icons/$i
  cd ..
done
