#!/bin/bash

# ---------------------------------
# Configurable variables
# ---------------------------------
URL=""
AUTH_TOKEN=""

# ---------------------------------
# Input data (easy to change)
# ---------------------------------
AGE=19
SEX=0        # 0=female, 1=male
BMI=27.9
CHILDREN=0
SMOKER=1     # 0=no, 1=yes
REGION=0     # 0=sw, 1=se, 2=nw, 3=ne

# ---------------------------------
# Build JSON payload
# ---------------------------------
read -r -d '' PAYLOAD <<EOF
{
  "data": [
    {
      "age": $AGE,
      "sex": $SEX,
      "bmi": $BMI,
      "children": $CHILDREN,
      "smoker": $SMOKER,
      "region": $REGION
    }
  ]
}
EOF

# ---------------------------------
# Send request
# ---------------------------------
curl -k -X POST "$URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -d "$PAYLOAD"

echo ""

