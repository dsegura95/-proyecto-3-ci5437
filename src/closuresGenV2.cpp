#include <iostream>

using namespace std;

/*
 * Enumera las variables de tipo 1 del CNF.
 */
int enum1(int e_i, int e_j, int h, int f, int E, int H) {
  return e_i - (e_i>e_j)*e_j - (e_j>e_i)*(e_j-1) + E*e_j + E*(E-1)*h + E*(E-1)*H*f; 
}

/*
 * Enumera las variables de tipo 2 del CNF.
 */
int enum2(int e, int t, int h, int f, int E, int H, int F) {
  return E*(E-1)*F*H + 1 + e + E*t + 2*E*h + 2*E*H*f;
}

int main(int argc, char *argv[]) {
  if (argc != 4) {
    cerr << "\e[1;31mError.\e[0m" << "Sintaxis invalida.\n"
      << "Ejecute el script como:\n\n"
      << "  \e[1mgenClosuresV2.out\e[0m \e[3;4mTEAMS\e[0m \e[3;4mDAYS\e[0m \e[3;4mDAILY_MATCHES\e[0m\n\n";
    return 1;
  }
  int E = atoi(argv[1]);
  int F = atoi(argv[2]);
  int H = atoi(argv[3]);
  // Numero de variables.
  long unsigned vars = E * (E + 1) * F * H;
  // Numero de clausuras.
  long unsigned closures = E * (E - 1) + 
    3 * E * (E - 1) * H * F +
    E * (E - 1) * F * H  +
    2 * E * F * H * (H - 1) + 
    2 * E * (F - 1) * H * H;

  cout << "c CNF file for game scheduling with " << E << " teams, " << F << " days and " 
    << H << " daily matches.\nc\n";
  cout << "p cnf " << vars << " " << closures << "\nc\n";


  // ============================== Primera restriccion ============================== //
  for (int e_1 = 0; e_1 < E; e_1++) 
    for (int e_2 = 0; e_2 < E; e_2++) 
      if (e_1 != e_2) {
        for (int f = 0; f < F; f++) 
          for (int h = 0; h < H; h++) 
            cout << enum1(e_1, e_2, h, f, E, H) << " ";
        cout << " 0\n";
      }


  // ============================== Segunda restriccion ============================== //
  for (int e_1 = 0; e_1 < E; e_1++)
    for (int e_2 = 0; e_2 < E; e_2++)
      if (e_1 != e_2)
        for (int h = 0; h < H; h++)
          for (int f = 0; f < F; f++) {
            cout << -enum1(e_1, e_2, h, f, E, H) << " "
              << enum2(e_1, 0, h, f, E, H, F) << " 0\n";
              
            cout << -enum1(e_1, e_2, h, f, E, H) << " "
              << enum2(e_2, 1, h, f, E, H, F) << " 0\n";

            cout << -enum2(e_1, 0, h, f, E, H, F) << " "
              << -enum2(e_2, 1, h, f, E, H, F) << " "
              << enum1(e_1, e_2, h, f, E, H) << " 0\n";
          }


  // ============================== Tercera restriccion ============================== //
  for (int e_i = 0; e_i < E; e_i++)
    for (int e_j = 0; e_j < E; e_j++)
      if (e_i < e_j)
        for (int h = 0; h < H; h++)
          for (int f = 0; f < F; f++) {
            cout << -enum2(e_i, 0, h, f, E, H, F) << " "
              << -enum2(e_j, 0, h, f, E, H, F) << " 0\n";

            cout << -enum2(e_i, 1, h, f, E, H, F) << " "
              << -enum2(e_j, 1, h, f, E, H, F) << " 0\n";
          }


  // ============================== Cuarta restriccion ============================== //
  for (int e = 0; e < E; e++)
    for (int h_i = 0; h_i < H; h_i++)
      for (int h_j = 0; h_j < H; h_j++)
        if (h_i < h_j)
          for (int f = 0; f < F; f++) {
            cout << -enum2(e, 0, h_i, f, E, H, F) << " "
              << -enum2(e, 0, h_j, f, E, H, F) << " 0\n";

            cout << -enum2(e, 0, h_i, f, E, H, F) << " "
              << -enum2(e, 1, h_j, f, E, H, F) << " 0\n";

            cout << -enum2(e, 1, h_i, f, E, H, F) << " "
              << -enum2(e, 0, h_j, f, E, H, F) << " 0\n";

            cout << -enum2(e, 1, h_i, f, E, H, F) << " "
              << -enum2(e, 1, h_j, f, E, H, F) << " 0\n";
          }


  // ============================== Quinta restriccion ============================== //
  for (int e = 0; e < E; e++)
    for (int f = 0; f < F-1; f++)
      for (int h = 0; h < H; h++)
        for (int hp = 0; hp < H; hp++) {
          cout << -enum2(e, 0, h, f, E, H, F) << " "
              << -enum2(e, 0, hp, f+1, E, H, F) << " 0\n";

          cout << -enum2(e, 1, h, f, E, H, F) << " "
              << -enum2(e, 1, hp, f+1, E, H, F) << " 0\n";
        }

  return 0;
}

