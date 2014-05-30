#!/usr/bin/bash

one_record(){
  local ID="$1"
  local CAP="$2"
  local NAME="$3"
  local CATEGORY="$4"
  local FILE="$5"

cat >> $FILE <<EOF
#-------------------------------
- model: paedia.Subject
  pk: $ID
  fields:
    name: $NAME
    research: 0
    category: $CATEGORY

- model: paedia.Article
  pk: $ID
  fields:
    caption: "$CAP"
    unlocked: 0
    image: ""
    text: ""
    code: UP-$NAME
    subject: $ID
    level: 0
    researched: 0
    read: 0
EOF
}

echo -n "CAP:  "; read CAP;
echo -n "NAME: "; read NAME;
echo -n "CAT:  "; read CAT;

one_record "$2" "$CAP" "$NAME" "$CAT" "$1"
