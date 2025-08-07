 #!/bin/bash
 PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
 TODAY=$(date)
 echo "This scan was created on $TODAY"
 DOMAIN=$1
 DIRECTORY=${DOMAIN}_recon
 echo "Creating directory $DIRECTORY."
 mkdir $DIRECTORY
 nmap_scan() 1
 {
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
 }
 dirsearch_scan() 2
 {
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
 }
 crt_scan() 3
 {
  curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
  echo "The results of cert parsing is stored in $DIRECTORY/crt."
 }
 case $2 in 4
  nmap-only)
    nmap_scan
    ;;
  dirsearch-only)
    dirsearch_scan
    ;;         
  crt-only)       
    crt_scan
    ;;
  *)       
    nmap_scan
 87
 Web Hacking Reconnaissance   
    dirsearch_scan
    crt_scan
    ;;     
esac