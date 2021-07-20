#!/bin/python3

from typing import *
from sys import argv, stderr

if (len(argv) != 4):
  print(
    "\033[1;31mError.\033[0m Sintaxis invalida.\n" +\
    "Ejecute el script como:\n\n" +\
    "  \033[1mpython3 verifyClosures.py\033[0m \033[3;4mTEAMS\033[0m \033[3;4mDAYS\033[0m \033[3;4mDAILY_MATCHES\033[0m\n\n",
    file=stderr
  )
  exit(1)

E, F, H = int(argv[1]), int(argv[2]), int(argv[3])
# 'Conjuntos'
E_c = [i for i in range(E)]
F_c = [i for i in range(F)]
H_c = [i for i in range(H)]

print(f'Iniciando verificacion para {E} equipos, {F} dias y {H} partidas diarias...\n')
ERROR = '\n\033[1;31mVerificacion fallida.\033[0m'


# =========================== VERIFICACION DE LA ENUMERACION =========================== #
def enum(e_i: int, e_j: int, h: int, f: int) -> int:
  """
    Funcion de enumeracion.
  """
  return e_i - (e_i > e_j)*(e_j) - (e_j > e_i)*(e_j-1) + E*e_j + E*(E-1)*h + E*(E-1)*H*f
i = 1
for f in F_c:
  for h in H_c:
    for e_j in E_c:
      for e_i in E_c:
        if e_i != e_j:
          value = enum(e_i, e_j, h, f)
          assert i == value, f'{ERROR} {(e_i, e_j, h, f)} debe tener el valor {i} pero se obtuvo {value}.'
          i += 1
print(f'Se calcularon {i-1} variables.')


# =========================== VERIFICACION DE LAS RESTRICCIONES =========================== #
closures = {}
def add_closure(c: List[Tuple[bool, int, int, int, int]], restriction: int):
  """
    Verifica que una clausura no ha sido agregada, y en caso de ser asi, la agrega.
  """
  # Ordenamos la clausura para que sea facil buscarla
  c_tail = list(c[1:])
  c_tail.sort()
  c = tuple([c[0]] + c_tail)

  assert not c in closures, f'{ERROR} Clausura {c} almacenada 2 veces.\n' +\
    f'La primera en la restriccion {closures[c]} y la segunda en la restriccion {restriction}.'
  closures[c] = restriction

# 1. Todos los participantes deben jugar dos veces con cada uno de los otros participantes, 
# una como "visitantes" y la otra como "locales".
k = 0
for e1 in E_c:
  for e2 in E_c:
    if e1 != e2:
      c = []
      for f in F_c:
        for h in H_c:
          c.append((True, e1, e2, h, f))
      c = tuple(c)
      add_closure(c, 1)
      k += 1
v1 = E*(E-1)
assert k == v1, f'{ERROR} Se esperaban {v1} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la primera restriccion.')


# 2. Dos juegos no pueden ocurrir al mismo tiempo.
k = 0
for f in F_c:
  for h in H_c:
    for e_i in E_c:
      for e_j in E_c:
        if (e_i != e_j):
          for e_mp in E_c:
            for e_np in E_c:
              if (e_mp != e_np) and ((e_mp > e_i) or (e_mp == e_i and e_np > e_j)):
                c = ((False, e_i, e_j, h, f), (False, e_mp, e_np, h, f))
                add_closure(c, 2)
                k += 1
v2 =  E*(E-1)*F*H*(E*(E-1)-1)//2
assert k == v2, f'{ERROR} Se esperaban {v2} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la segunda restriccion.')


# 3. Un participante puede jugar a lo sumo una vez por día.
k = 0
for e in E_c:
  for e_i in E_c:
    if (e != e_i):
      for e_j in E_c:
        if (e != e_j) and (e_i < e_j):
          for f in F_c:
            for h in H_c:
              for hp in H_c:
                if h != hp:
                  c = ((False, e, e_i, h, f), (False, e, e_j, hp, f))
                  add_closure(c, 3)
                  k += 1

                  c = ((False, e_i, e, h, f), (False, e_j, e, hp, f))
                  add_closure(c, 3)
                  k += 1
for e in E_c:
  for e_i in E_c:
    if (e != e_i):
      for e_j in E_c:
        if (e != e_j) and (e_i != e_j):
          for f in F_c:
            for h in H_c:
              for hp in H_c:
                if h != hp:
                  c = ((False, e, e_i, h, f), (False, e_j, e, hp, f))
                  add_closure(c, 3)
                  k += 1
for e in E_c:
  for ep in E_c:
    if (e < ep):
      for f in F_c:
        for h in H_c:
          for hp in H_c:
            if h < hp:
              c = ((False, e, ep, h, f), (False, e, ep, hp, f))
              add_closure(c, 3)
              k += 1

              c = ((False, ep, e, h, f), (False, ep, e, hp, f))
              add_closure(c, 3)
              k += 1

              c = ((False, e, ep, h, f), (False, ep, e, hp, f))
              add_closure(c, 3)
              k += 1

              c = ((False, ep, e, h, f), (False, e, ep, hp, f))
              add_closure(c, 3)
              k += 1
v3 =  E*F*H*(H-1)*(E-1)*(E-2) + E*(E-1)*(E-2)*F*H*(H-1) + E*(E-1)*F*H*(H-1)
assert k == v3, f'{ERROR} Se esperaban {v3} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la tercera restriccion.')


# 4. Un participante no puede jugar de "visitante" en dos días consecutivos, ni de 
# "local" dos días seguidos.
k = 0
for e in E_c:
  for e1 in E_c:
    if e != e1:
      for e2 in E_c:
        if e != e2 and e1 != e2:
          for f in F_c:
            if f != F-1:
              for h in H_c:
                for hp in H_c:
                  c = ((True, e, e1, h, f), (True, e, e2, hp, f+1))
                  add_closure(c, 4)
                  k += 1

                  c = ((True, e1, e, h, f), (True, e2, e, hp, f+1))
                  add_closure(c, 4)
                  k += 1
v4 = 2*E*(E-1)*(E-2)*(F-1)*H*H
assert k == v4, f'{ERROR} Se esperaban {v4} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la cuarta restriccion.')

print(f'Se calcularon {int(v1+v2+v3+v4)} clausuras.')
print('\n\033[1;36mVerificacion exitosa.\033[0m')
