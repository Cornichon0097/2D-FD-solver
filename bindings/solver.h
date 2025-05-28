#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>

class Solver
{
public:
    // attributes
    arma::mat V0;
    arma::mat psi_real_part;
    arma::mat psi_imag_part;
    double h_bar = 1.0;
    double m = 1.0;
    std::string methode;
    double dx;
    double dy;
    double dt;

    // methods
    Solver(void);

    Solver(arma::mat V0);

    Solver(arma::mat &_V0, arma::mat &_psi0_real_part, arma::mat &_psi0_imag_part,
           double _h_bar, double _m, std::string _methode, double _dx, double _dy, double _dt);

    arma::mat mat_add_zeros(arma::mat);

    void calcul_psi_t_plus_dt(void);

    void ftcs(void);
    void btcs(void);
    void ctcs(void);
};

#endif /* solver.h */
