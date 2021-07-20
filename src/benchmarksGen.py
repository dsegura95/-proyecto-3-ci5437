#!/bin/python

import json
from sys import argv, stderr
from datetime import datetime, timedelta

if (len(argv) != 4):
  print(
    "\033[1;31mError.\033[0m Sintaxis invalida.\n" +\
    "Ejecute el script como:\n\n" +\
    "  \033[1mpython3 benchmarksGen.py\033[0m \033[3;4mTEAMS\033[0m " +\
    "\033[3;4mDAYS\033[0m \033[3;4mDAILY_MATCHES\033[0m\n\n",
    file=stderr
  )
  exit(1)

E, F, H = int(argv[1]), int(argv[2]), int(argv[3])
begin_date = datetime.fromisoformat("1999-11-28")

data = {
  "tournament_name": "POMAC",
  "start_date": str(begin_date)[:10],
  "end_date": str(begin_date + timedelta(days=F))[:10],
  "start_time": "00:00:00",
  "end_time": "0"*(H < 5) + str(2*H) + ":00:00",
  "participants": [f'T{i}' for i in range(E)]
}

with open(f'benchmark_E{E}H{H}F{F}.json', 'w') as f:
  json.dump(data, f)