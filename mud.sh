#!/bin/bash
# Uso: mud.sh start | mud.sh "comando" [espera_s] | mud.sh read [espera_s]
D=/home/lucas/Desktop/mudvalinor
R=$D/logs/raw.log           # tudo que o servidor envia (bruto)
T=$D/logs/transcript.log    # sessão legível: entradas e saídas
F=$D/.mud_in; O=$D/.mud_off
mkdir -p $D/logs; touch $R

clean() { iconv -f latin1 -t utf-8 | sed -e 's/\x1b\[[0-9;]*[a-zA-Z]//g' -e 's/\r//g' | tr -d '\377\373\374\375\376\001\003\030\037'; }

show() {
  sleep "${1:-1.5}"
  off=$(cat $O 2>/dev/null || echo 0); size=$(stat -c %s $R)
  tail -c +$((off+1)) $R | head -c $((size-off)) | clean | tee -a $T > $D/.mud_last
  cat $D/.mud_last
  # chat OOC e mensagens diretas de jogadores: destacar e guardar em logs/chat.log
  grep -E "^\(OOC\) .+ (disse|perguntou|exclamou)|para você '" $D/.mud_last | grep -v "^(OOC) Você" \
    | tee -a $D/logs/chat.log | sed 's/^/### CHAT: /'
  echo $size > $O
  python3 $D/extrair.py
}

case "$1" in
  start)
    pkill -f "[s]ocat - TCP:mud.valinor"; pkill -f "[s]leep 99999999"
    rm -f $F; mkfifo $F
    echo "=== NOVA CONEXÃO $(date '+%F %T') ===" >> $T
    stat -c %s $R > $O
    nohup sleep 99999999 > $F 2>/dev/null &
    nohup sh -c "socat - TCP:mud.valinor.com.br:4000 < $F >> $R 2>&1" >/dev/null 2>&1 &
    show 3 ;;
  read) show "${2:-1}" ;;
  *)
    printf '\n>>> [%s] %s\n' "$(date '+%T')" "$1" >> $T
    printf '%s\r\n' "$1" | iconv -f utf-8 -t latin1 > $F
    show "${2:-1.5}" ;;
esac
