PORT=1234
PYTHON=python3
PAUSE=60

cyan="$(tput setaf 6)"
nrm="$(tput sgr0)"

echo "${cyan}Initiating autorun script.$nrm"
while true; do
  $PYTHON main.py $PORT

  if [ -r .killscript ]; then
    echo "${cyan}Shutdown requested.  Autorun script terminating.$nrm"
    rm .killscript
    break
  fi

  if [ -r .pausescript ]; then
  	echo "${cyan}Reboot requested.  Waiting a full minute before rebooting.$nrm"
    rm .pausescript
    sleep $(($PAUSE - 5))
    continue
  fi

  sleep 5
done
