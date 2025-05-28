#include <iostream>

#include "solver.h"

/**
 * constructeur par défaut de la classe solver
 *
 * les paramètres physiques sont initialisées à des valeurs par défaut
 * les paramètres de l'état initial psi et V0 ne sont pas initialisés
*/
Solver::Solver(void):
    h_bar(1.),
    m(1.),
    methode("ftcs"),
    dx(1.),
    dy(1.),
    dt(1.)
{}

Solver::Solver(arma::mat V0):
    V0(V0)
{}

/**
 * Initialiseur de la classe solver
 * On y prend l'état initial de la simulation, donc le champ de potentiel et psi à l'instant 0
 * les autres arguments sont des paramètres ou des matrices que nous initialisons une fois pour les utiliser dans les calculs de phi de t+dt
 *
 * @param V0 la matrice du champ de potentiel
 * @param _psi0_real_part psi à l'instant 0, partie réelle
 * @param _psi0_imag_part psi à l'instant 0, partie imaginaire
 * @param h_bar la constante de plank réduite
 * @param m la masse de la particule
 * @param methode charactère donnant par quelle methode on souhaite calculer (f pour FTCS, b pour BTCS, c pour CTCS)
 * @param dx pas d'espace sur l'axe x
 * @param dy pas d'espace sur l'axe y
 * @param dt pas de temps
*/
Solver::Solver(arma::mat &_V0, arma::mat &_psi0_real_part, arma::mat &_psi0_imag_part,
               double _h_bar, double _m, std::string _methode, double _dx, double _dy, double _dt):
    V0(_V0),
    psi_real_part(_psi0_real_part),
    psi_imag_part(_psi0_imag_part),
    h_bar(_h_bar),
    m(_m),
    methode(_methode),
    dx(_dx),
    dy(_dy),
    dt(_dt)
{
}

/**
 * ajoute un "contour" de zeros sur une matrice
 * sera utile pour les calcul de bord
 *
 * @param mat une matrice carré
*/
arma::mat Solver::mat_add_zeros(arma::mat mat)
{
    int n = mat.n_cols; // egale a n_rows car mat est carrée

    arma::mat new_mat(n + 2, n + 2);
    new_mat.zeros();
    new_mat.submat(1, 1, n, n) = mat;

    return new_mat;
}

/**
 * Calcul la valeur de psi(t+dt)
 * fait appel à une fonction auxiliaire en fonction de la méthode de calcul choisie
 *
 * les méthodes implémentées sont FTCS (Forward), BTCS (Backward), CTCS (Crank-Nicolson)
 *
*/
void Solver::calcul_psi_t_plus_dt(void)
{
    if (!methode.compare("ftcs"))
    {
        ftcs();
    }
    else if(!methode.compare("btcs"))
    {
        btcs();
    }
    else if(!methode.compare("ctcs"))
    {
        ctcs();
    }
}

/**
 * calcul la valeur de psi(t+dt) avec le schéma de calcul FTCS (forward)
*/
void Solver::ftcs(void)
{

    int n = psi_imag_part.n_cols; //egal à n_rows car matrice carrée

    arma::mat potentiel(n, n);

    arma::mat tmp_real_part = mat_add_zeros(psi_real_part);
    arma::mat tmp_imag_part = mat_add_zeros(psi_imag_part);

    double const_dx = h_bar / (2 * m * dx * dx);
    double const_dy = h_bar / (2 * m * dy * dy);
    potentiel = ((-1 / h_bar) * V0) - 2 * const_dx - 2 * const_dy;

    arma::mat new_real_part = psi_real_part - dt * (
        (potentiel % psi_imag_part) +
        const_dx * (tmp_imag_part.submat(1, 2, n, n + 1) + tmp_imag_part.submat(1, 0, n, n - 1)) +
        const_dy * (tmp_imag_part.submat(0, 1, n - 1, n) + tmp_imag_part.submat(2, 1, n + 1, n))
    );

    arma::mat new_imag_part = psi_imag_part + dt * (
        (potentiel % psi_real_part) +
        const_dx * (tmp_real_part.submat(1, 2, n, n + 1) + tmp_real_part.submat(1, 0, n, n - 1)) +
        const_dy * (tmp_real_part.submat(0, 1, n - 1, n) + tmp_real_part.submat(2, 1, n + 1, n))
    );

    psi_imag_part = new_imag_part;
    psi_real_part = new_real_part;
}

void Solver::btcs(void)
{
    // TODO
}

void Solver::ctcs(void)
{
    // TODO
}
