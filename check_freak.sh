#!/usr/bin/env bash

# check_freak.sh
# (c) 2015 Martin Seener

# Simple script which checks SSL/TLS services for the FREAK vulnerability (CVE 2015-0204)
# It will output if the checked host is vulnerable and returns the right exit code
# so it can also be used as a nagios check!

PROGNAME=$(basename $0)
VERSION="v0.2"
AUTHOR="2015, Martin Seener (martin@seener.de)"

# Set the timeout how long openssl can try to connect to the service
TIMEOUT=10

print_help() {
  echo ""
  echo "$PROGNAME is a small shell script which checks remote SSL/TLS services for the FREAK vulnerability (CVE 2015-0204)"
  echo "It will return if the service is vulnerable or not and exit with 0 (OK) or 2 (CRIT) so it can be used as"
  echo "a nagios check too"
  echo ""
  echo "Usage: ./$PROGNAME <IP or Hostname> <port>"
  echo "Example: ./$PROGNAME www.google.com 443"
  echo ""
}

initialize() {
  if [ -z "$1" ]; then
    echo "The Hostname/IP Argument is missing!"
    echo ""
    print_help
    exit 3
  fi
  if [[ ! $2 =~ ^[0-9]+$ ]] || [ $2 -eq 0 ] || [ $2 -gt 65535 ] ; then
    echo "The Port argument must be a positive integer value starting at 1 up to 65535"
    echo ""
    print_help
    exit 3
  fi
  OPENSSL=$(which openssl)
  if [ "$OPENSSL" == "" ]; then
    echo "Cannot find openssl! Aborting!"
    echo ""
    print_help
    exit 3
  fi
}

check_freak() {
  # Get the information (we use the strange sleep/kill method here because timeout doesn't work on OSX by default!)
  CHK=$( $OPENSSL s_client -connect $1:$2 -cipher EXPORT < /dev/null 2>/dev/null & sleep $TIMEOUT; kill $! 2>/dev/null )
  if [ "$CHK" == "" ]; then
    echo "UNKNOWN - Timeout connecting to $1 on port $2"
    exit 3
  fi
  # Check if there is an export cipher
  echo $CHK | grep "Cipher is EXP" > /dev/null
}

case "$1" in
  --help|-h)
    print_help
    exit 3;;
  *)
    ;;
esac

# Initialize
initialize $1 $2

# Do the check
check_freak $1 $2

# Return the result
if [ $? -eq 1 ]; then
  echo "OK - $1 on port $2 is PROBABLY NOT vulnerable to FREAK (CVE 2015-0204)"
  exit 0
else
  echo "CRITICAL - $1 on port $2 IS PROBABLY VULNERABLE to FREAK (CVE 2015-0204)"
  exit 2
fi