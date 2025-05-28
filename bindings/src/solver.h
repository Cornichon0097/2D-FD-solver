#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>

class Solver
{
public:
    Solver(arma::mat&, arma::mat&, arma::mat&,
           std::string, double, double, double);

    Solver(arma::mat&, arma::mat&, arma::mat&, double, double,
           std::string, double, double, double);

    void compute(void);

    arma::mat r_part(void);

    arma::mat i_part(void);

private:
    arma::mat V0;
    arma::mat rpart, ipart;

    std::string scheme;

    double h_bar, m;
    double dx, dy, dt;

    arma::mat padded(arma::mat);

    void ftcs(void);

    void btcs(void);

    void ctcs(void);
};

#endif /* solver.h */
