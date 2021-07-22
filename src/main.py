#!/bin/python3

import subprocess, json
from sys import argv, stderr
from ics import Calendar, Event
from datetime import date, datetime, timedelta
from typing import *
from time import time


# OBTENER EL ARCHIVO DE ENTRADA
if (len(argv) == 5):
  filename = argv[1]
  closure_gen = argv[2]
  cnf_solver = argv[3]
  output_ics = argv[4]
else:
  print(
    "\033[1;31mError de sintaxis\033[0m. Ejecute el script como:\n\n" +\
    "    python main.py  \033[3;4mJSON\033[0m  \033[3;4mCLOSURES_GEN\033[0m  " +\
    "\033[3;4mSAT_SOLVER\033[0m  \033[3;4mOUTPUT\033[0m\n",
    file=stderr
  )
  exit(1)


# LEER ARCHIVO JSON
with open(filename) as f:
  data = json.load(f)


# CREAR ARCHIVO CNF
teams = data['participants']
E = len(teams)

start_date = date.fromisoformat(data['start_date'])
F = (date.fromisoformat(data['end_date']) - start_date).days + 1

tournament = data['tournament_name']

# Obtenemos el numero de horas. Si la hora inicial no es exacta, es decir, sus minutos
# y segundos no son cero, entonces se tomara como hora inicial sera la siguiente. Analogamente, 
# si la hora final no es exacta, entonces se tomara la anterior.
start_timedate = datetime.fromisoformat('2021-01-01T' + data['start_time'])
start_time = start_timedate.hour + (start_timedate.minute != 0 or start_timedate.second != 0)
end_time = datetime.fromisoformat('2021-01-01T' + data['end_time'])
end_time = end_time.hour 
# Tomamos la diferencia entre las horas entre 2, ya que los partidos duran 2 horas.
H = (end_time - start_time) * (start_time < end_time) // 2

# Ejecutamos el binario que genera los CNF
cnf_name = f'schedulingE{E}F{F}H{H}.cnf'
command = f'{closure_gen} {E} {F} {H} > {cnf_name}'
process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if process.stderr:
  print(
    '\033[1;31mError\033[0m. Ha ocurrido el siguiente error al generar el CNF:\n' +\
    f'{str(process.stderr)[2:-1]}',
    file=stderr
  )
  exit(2)


# RESOLVER CNF
file_sol_name = f'schedulingE{E}F{F}H{H}.cnfsol'
command = f'{cnf_solver} {cnf_name} {file_sol_name}'
init = time()
process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(f'El problema SAT fue resuelto en {round(time() - init, 5)} segundos.')
if process.stderr:
  print(
    '\033[1;31mError\033[0m. Ha ocurrido el siguiente error al resolver el CNF:\n' +\
    f'{str(process.stderr)[2:-1]}',
    file=stderr
  )
  exit(2)


# LEER ARCHIVO SOLUCION
with open(file_sol_name) as f:
  sol = f.read()
  if sol == "UNSAT\n":
    print(
      '\033[1;31mError\033[0m. No existe forma de organizar los partidos que cumpla todas las restricciones.',
      file=stderr
    )
    exit(2)
  # Almacenamos aquellas variables que toman el valor de True
  vars = [int(n) for n in sol.split() if 0 < int(n) <= E*(E-1)*H*F]



# CREAMOS EL ARCHIVO ICS  
varTuples = [None]
for f in range(F):
  for h in range(H):
    for e_v in range(E):
      for e_l in range(E):
        if e_v != e_l:
          varTuples.append((e_l, e_v, f, h))

current_date = str(start_date)
def getEvent(var: int):
  """
    Obtenemos un evento dada una variable de SAT.
  """
  # Obtenemos los datos del evento
  (e_l, e_v, f, h) = varTuples[var]
  team_local = teams[e_l]
  team_visitor = teams[e_v]
  date = str(start_date + timedelta(days=f))
  begin_time = str(start_timedate + timedelta(hours=2*h))[-8:]
  end_time = str(start_timedate + timedelta(hours=2*h + 2))[-8:]

  global current_date
  if current_date != date: 
    print('')
    current_date = date
  print(f'{team_local} - {team_visitor}  /  {date} :: {begin_time}')

  # Creamos el evento
  event = Event()
  event.name = f'{tournament}: \'{team_local}\' - \'{team_visitor}\'.'
  event.begin = (date + 'T' + begin_time + 'Z')
  event.end = (date + 'T' + end_time + 'Z')
  event.created = datetime.now()

  return event

# Creamos el icalendar
cal = Calendar()
for v in vars: cal.events.add(getEvent(v))

with open(output_ics, "w") as f:
  f.writelines(cal)


# ELIMINAR ARCHIVOS EXTRA
command = f'rm {cnf_name} {file_sol_name}'
process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

print('\033[1;36mEjecucion exitosa.\033[0m')