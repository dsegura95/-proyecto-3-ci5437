#include <iostream>

using namespace std;

/*
 * Enumera las variables del CNF.
 */
int enumVars(int e_i, int e_j, int h, int f, int E, int H) {
  return e_i - (e_i>e_j)*e_j - (e_j>e_i)*(e_j-1) + E*e_j + E*(E-1)*h + E*(E-1)*H*f; 
}

int main(int argc, char *argv[]) {
  if (argc != 4) {
    cerr << "\e[1;31mError.\e[0m" << "Sintaxis invalida.\n"
      << "Ejecute el script como:\n\n"
      << "  \e[1mgenClosures.out\e[0m \e[3;4mTEAMS\e[0m \e[3;4mDAYS\e[0m \e[3;4mDAILY_MATCHES\e[0m\n\n";
    return 1;
  }
  int E = atoi(argv[1]);
  int F = atoi(argv[2]);
  int H = atoi(argv[3]);
  // Numero de variables.
  long unsigned vars = E * (E - 1) * F * H;
  // Numero de clausuras.
  long unsigned closures = E * (E - 1) + 
    E * (E - 1) * (E * (E - 1) - 1) * F * H / 2 +
    E * F * H * (H - 1) * (E - 1) * (E - 2) + E * (E - 1) * (E - 2) * F * H * (H - 1) + 
      E * (E - 1) * F * H * (H - 1) + 
    2 * E * (E - 1) * (E - 2) * (F - 1) * H * H;

  cout << "c CNF file for game scheduling with " << E << " teams, " << F << " days and " 
    << H << " daily matches.\nc\n";
  cout << "p cnf " << vars << " " << closures << "\nc\n";
  

  // ============================== Primera restriccion ============================== //
  for (int e_1 = 0; e_1 < E; e_1++) 
    for (int e_2 = 0; e_2 < E; e_2++) 
      if (e_1 != e_2) {
        for (int f = 0; f < F; f++) 
          for (int h = 0; h < H; h++) 
            cout << enumVars(e_1, e_2, h, f, E, H) << " ";
        cout << "0\n";
      }


  // ============================== Segunda restriccion ============================== //
  for (int f = 0; f < F; f++) 
    for (int h = 0; h < H; h++) 
      for (int e_i = 0; e_i < E; e_i++) 
        for (int e_j = 0; e_j < E; e_j++) 
          if (e_i != e_j) 
            for (int e_mp = 0; e_mp < E; e_mp++) 
              for (int e_np = 0; e_np < E; e_np++) 
                if (e_mp != e_np && (e_mp > e_i || (e_mp == e_i && e_np > e_j))) 
                  cout << -enumVars(e_i, e_j, h, f, E, H) << " " 
                    << -enumVars(e_mp, e_np, h, f, E, H) << " 0\n";


  // ============================== Tercera restriccion ============================== //
  for (int e = 0; e < E; e++)
    for (int e_i = 0; e_i < E; e_i++)
      if (e != e_i)
        for (int e_j = 0; e_j < E; e_j++)
          if (e != e_j && e_i < e_j)
            for (int f = 0; f < F; f++)
              for (int h = 0; h < H; h++)
                for (int h_p = 0; h_p < H; h_p++)
                  if (h != h_p) {
                    cout << -enumVars(e, e_i, h, f, E, H) << " " 
                      << -enumVars(e, e_j, h_p, f, E, H) << " 0\n";

                    cout << -enumVars(e_i, e, h, f, E, H) << " " 
                      << -enumVars(e_j, e, h_p, f, E, H) << " 0\n";
                  }
  for (int e = 0; e < E; e++)
    for (int e_i = 0; e_i < E; e_i++)
      if (e != e_i)
        for (int e_j = 0; e_j < E; e_j++)
          if (e != e_j && e_i != e_j)
            for (int f = 0; f < F; f++)
              for (int h = 0; h < H; h++)
                for (int h_p = 0; h_p < H; h_p++)
                  if (h != h_p) 
                    cout << -enumVars(e, e_i, h, f, E, H) << " " 
                      << -enumVars(e_j, e, h_p, f, E, H) << " 0\n";
  for (int e = 0; e < E; e++)
    for (int e_p = 0; e_p < E; e_p++)
      if (e < e_p)
        for (int f = 0; f < F; f++)
          for (int h = 0; h < H; h++)
            for (int h_p = 0; h_p < H; h_p++)
              if (h < h_p) {
                cout << -enumVars(e, e_p, h, f, E, H) << " " 
                  << -enumVars(e, e_p, h_p, f, E, H) << " 0\n";

                cout << -enumVars(e_p, e, h, f, E, H) << " " 
                  << -enumVars(e_p, e, h_p, f, E, H) << " 0\n";

                cout << -enumVars(e, e_p, h, f, E, H) << " " 
                  << -enumVars(e_p, e, h_p, f, E, H) << " 0\n";

                cout << -enumVars(e_p, e, h, f, E, H) << " " 
                  << -enumVars(e, e_p, h_p, f, E, H) << " 0\n";
              }


  // ============================== Cuarta restriccion ============================== //
  for (int e = 0; e < E; e++)
    for (int e_1 = 0; e_1 < E; e_1++)
      if (e != e_1)
        for (int e_2 = 0; e_2 < E; e_2++)
          if (e != e_2 && e_1 != e_2)
            for (int f = 0; f < F-1; f++)
              for (int h = 0; h < H; h++)
                for (int h_p = 0; h_p < H; h_p++) {
                  cout << -enumVars(e, e_1, h, f, E, H) << " " 
                    << -enumVars(e, e_2, h_p, f+1, E, H) << " 0\n";

                  cout << -enumVars(e_1, e, h, f, E, H) << " " 
                    << -enumVars(e_2, e, h_p, f+1, E, H) << " 0\n";
                }

  return 0;
}