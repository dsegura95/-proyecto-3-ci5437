#!/bin/python3

from typing import *
from sys import argv, stderr

if (len(argv) != 4):
  print(
    "\033[1;31mError.\033[0m Sintaxis invalida.\n" +\
    "Ejecute el script como:\n\n" +\
    "  \033[1mpython3 verifyClosuresV2.py\033[0m \033[3;4mTEAMS\033[0m \033[3;4mDAYS\033[0m \033[3;4mDAILY_MATCHES\033[0m\n\n",
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
def enum1(e_i: int, e_j: int, h: int, f: int) -> int:
  """
    Funcion de enumeracion para las variables de tipo 1.
  """
  return e_i - (e_i > e_j)*(e_j) - (e_j > e_i)*(e_j-1) + E*e_j + E*(E-1)*h + E*(E-1)*H*f

def enum2(e: int, t: int, h: int, f: int) -> int:
  """
    Funcion de enumeracion para las variables de tipo 2.
  """
  return E*(E-1)*F*H + 1 + e + E*t + 2*E*h + 2*E*H*f

i = 1
for f in F_c:
  for h in H_c:
    for e_j in E_c:
      for e_i in E_c:
        if e_i != e_j:
          value = enum1(e_i, e_j, h, f)
          assert i == value, f'{ERROR} {(e_i, e_j, h, f)} debe tener el valor {i} pero se obtuvo {value}.'
          i += 1
for f in F_c:
  for h in H_c:
    for t in [0,1]:
      for e in E_c:
        value = enum2(e, t, h, f)
        assert i == value, f'{ERROR} {(e, t, h, f)} debe tener el valor {i} pero se obtuvo {value}.'
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


# 2. Equivalencia entre las variables de tipo 1 y de tipo 2. La variable (e_1, e_2, h, f ) 
# es True si y solo si (e_1, l, h, f ) ∧ (e_2, v, h, f ) es True.
k = 0
for e1 in E_c:
  for e2 in E_c:
    if e1 != e2:
      for h in H_c:
        for f in F_c:
          c = ((False, e1, e2, h, f), (True, e1, 0, h, f))
          add_closure(c, 2)
          k += 1

          c = ((False, e1, e2, h, f), (True, e2, 1, h, f))
          add_closure(c, 2)
          k += 1

          c = ((False, e1, 0, h, f), (False, e2, 1, h, f), (True, e1, e2, h, f))
          add_closure(c, 2)
          k += 1
v2 = 3*E*(E-1)*H*F
assert k == v2, f'{ERROR} Se esperaban {v2} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la segunda restriccion.')


# 3. Dos juegos no pueden ocurrir al mismo tiempo.
k = 0
for e_i in E_c:
  for e_j in E_c:
    if e_i < e_j:
      for f in F_c:
        for h in H_c:
          c = ((False, e_i, 0, h, f), (False, e_j, 0, h, f))
          add_closure(c, 3)
          k += 1

          c = ((False, e_i, 1, h, f), (False, e_j, 1, h, f))
          add_closure(c, 3)
          k += 1
v3 = E*(E-1)*H*F
assert k == v3, f'{ERROR} Se esperaban {v3} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la tercera restriccion.')


# 4. Un participante puede jugar a lo sumo una vez por dı́a.
k = 0
for e in E_c:
  for h_i in H_c:
    for h_j in H_c:
      if h_i < h_j:
        for f in F_c:
          c = ((False, e, 0, h_i, f), (False, e, 0, h_j, f))
          add_closure(c, 4)
          k += 1

          c = ((False, e, 0, h_i, f), (False, e, 1, h_j, f))
          add_closure(c, 4)
          k += 1

          c = ((False, e, 1, h_i, f), (False, e, 0, h_j, f))
          add_closure(c, 4)
          k += 1

          c = ((False, e, 1, h_i, f), (False, e, 1, h_j, f))
          add_closure(c, 4)
          k += 1
v4 = 2*E*F*H*(H-1)
assert k == v4, f'{ERROR} Se esperaban {v4} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la cuarta restriccion.')


# 5. Un participante no puede jugar de visitante en dos dı́as consecutivos, 
# ni de local dos dı́as seguidos.
k = 0
for e in E_c:
  for f in F_c[:-1]:
    for h in H_c:
      for hp in H_c:
        c = ((False, e, 0, h, f), (False, e, 0, hp, f+1))
        add_closure(c, 5)
        k += 1

        c = ((False, e, 1, h, f), (False, e, 1, hp, f+1))
        add_closure(c, 5)
        k += 1
v5 = 2*E*(F-1)*H*H
assert k == v5, f'{ERROR} Se esperaban {v5} clausuras y se obtuvieron {k}.'
print(f'Se generaron correctamente {k} clausuras para la quinta restriccion.')


print(f'Se calcularon {int(v1+v2+v3+v4+v5)} clausuras.')
print('\n\033[1;36mVerificacion exitosa.\033[0m')