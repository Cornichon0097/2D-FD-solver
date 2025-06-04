#include <stdlib.h>
#include <string.h>

#include "solver.h"
#include "cuda_helper.h"

Solver::Solver(arma::mat &_V0, arma::mat &_rpart, arma::mat &_ipart,
               std::string scheme, double _dx, double _dy, double _dt):
    scheme(scheme), dx(_dx), dy(_dy), dt(_dt)
{
    struct h_data h_d;

    h_bar = 1.0;
    m     = 1.0;

    V0    = padded(_V0);
    rpart = padded(_rpart);
    ipart = padded(_ipart);

    h_d.v0     = V0.memptr();
    h_d.rpart  = rpart.memptr();
    h_d.ipart  = ipart.memptr();
    h_d. ncols = V0.n_cols;
    h_d.h_bar  = h_bar;
    h_d.m      = m;
    h_d.dx     = dx;
    h_d.dy     = dy;
    h_d.dt     = dt;

    init_device_memory(&h_d);

    if (init_device_memory(&h_d) < 0) {
        clean_up_device();
        exit(EXIT_FAILURE);
    }
}

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
 * @param scheme charactère donnant par quelle scheme on souhaite calculer (f pour FTCS, b pour BTCS, c pour CTCS)
 * @param dx pas d'espace sur l'axe x
 * @param dy pas d'espace sur l'axe y
 * @param dt pas de temps
*/
Solver::Solver(arma::mat &_V0, arma::mat &_rpart, arma::mat &_ipart,
               double _h_bar, double _m, std::string scheme,
               double _dx, double _dy, double _dt):
    scheme(scheme), h_bar(_h_bar), m(_m), dx(_dx), dy(_dy), dt(_dt)
{
    struct h_data h_d;

    V0    = padded(_V0);
    rpart = padded(_rpart);
    ipart = padded(_ipart);

    h_d.v0     = V0.memptr();
    h_d.rpart  = rpart.memptr();
    h_d.ipart  = ipart.memptr();
    h_d. ncols = V0.n_cols;
    h_d.h_bar  = h_bar;
    h_d.m      = m;
    h_d.dx     = dx;
    h_d.dy     = dy;
    h_d.dt     = dt;

    if (init_device_memory(&h_d) < 0) {
        clean_up_device();
        exit(EXIT_FAILURE);
    }
}

/**
 * Calcul la valeur de psi(t+dt)
 * fait appel à une fonction auxiliaire en fonction de la méthode de calcul choisie
 *
 * les méthodes implémentées sont FTCS (Forward), BTCS (Backward), CTCS (Crank-Nicolson)
 *
*/
void Solver::compute(void)
{
    struct h_data h_d = {.rpart = rpart.memptr(), .ipart = ipart.memptr()};

    execute_kernel(scheme.front());
    retrieve_results(&h_d);
}

arma::mat Solver::r_part(void)
{
    return rpart.submat(1, 1, rpart.n_rows - 2, rpart.n_cols - 2);
}

arma::mat Solver::i_part(void)
{
    return ipart.submat(1, 1, ipart.n_rows - 2, ipart.n_cols - 2);
}

/**
 * ajoute un "contour" de zeros sur une matrice
 * sera utile pour les calcul de bord
 *
 * @param mat une matrice carré
*/
arma::mat Solver::padded(const arma::mat m)
{
    arma::mat res(m.n_rows + 2, m.n_cols + 2, arma::fill::zeros);
    res.submat(1, 1, m.n_rows, m.n_cols) = m;

    return res;
}

/**
 * calcul la valeur de psi(t+dt) avec le schéma de calcul FTCS (forward)
*/
void Solver::ftcs(void)
{
    /* TODO */
}

void Solver::btcs(void)
{
    /* TODO */
}

void Solver::ctcs(void)
{
    /* TODO */
}
