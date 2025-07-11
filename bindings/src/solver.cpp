/**
 * \file       solver.cpp
 */
#include "solver.h"

/**
 * \brief      Solevr constructor.
 *
 * Creates a new solver with the Planck constant and the particle masse set to
 * default value (1.0).
 *
 * \param      _V0     The potentiel field
 * \param      _rpart  The real part
 * \param      _ipart  The imaginary part
 * \param[in]  scheme  The scheme
 * \param[in]  _dx     The x speed
 * \param[in]  _dy     The y speed
 * \param[in]  _dt     The delta time
 */
Solver::Solver(arma::mat &_V0, arma::mat &_rpart, arma::mat &_ipart,
               std::string scheme, double _dx, double _dy, double _dt):
    scheme(scheme), dx(_dx), dy(_dy), dt(_dt)
{
    h_bar = 1.0;
    m     = 1.0;

    V0    = padded(_V0);
    rpart = padded(_rpart);
    ipart = padded(_ipart);
}

/**
 * \brief      Solevr constructor.
 *
 * \param      _V0     The potentiel field
 * \param      _rpart  The real part
 * \param      _ipart  The imaginary part
 * \param[in]  _h_bar  The Planck constant
 * \param[in]  _m      The particle masse
 * \param[in]  scheme  The scheme
 * \param[in]  _dx     The x speed
 * \param[in]  _dy     The y speed
 * \param[in]  _dt     The delta time
 */
Solver::Solver(arma::mat &_V0, arma::mat &_rpart, arma::mat &_ipart,
               double _h_bar, double _m, std::string scheme,
               double _dx, double _dy, double _dt):
    scheme(scheme), h_bar(_h_bar), m(_m), dx(_dx), dy(_dy), dt(_dt)
{
    V0    = padded(_V0);
    rpart = padded(_rpart);
    ipart = padded(_ipart);
}

/**
 * \brief      Compute the next psi value.
 *
 * Calls the right function depending on the scheme to compute the next value of
 * psi.
 */
void Solver::compute(void)
{
    switch (scheme.front()) {
    case 'f':
        ftcs();
        break;
    case 'b':
        btcs();
        break;
    case 'c':
        ctcs();
        break;
    default:
        break;
    }
}

/**
 * \brief      Returns the real part.
 *
 * \return     The current real part.
 */
arma::mat Solver::r_part(void)
{
    return rpart.submat(1, 1, rpart.n_rows - 2, rpart.n_cols - 2);
}

/**
 * \brief      Returns the imaginary part.
 *
 * \return     The current imaginary part.
 */
arma::mat Solver::i_part(void)
{
    return ipart.submat(1, 1, ipart.n_rows - 2, ipart.n_cols - 2);
}

/**
 * \brief      Adds padding to a matrix.
 *
 * \param[in]  m     A square matrix
 *
 * \return     The matrix with padding.
 */
arma::mat Solver::padded(const arma::mat m)
{
    arma::mat res(m.n_rows + 2, m.n_cols + 2, arma::fill::zeros);
    res.submat(1, 1, m.n_rows, m.n_cols) = m;

    return res;
}

/**
 * \brief      FTCS compute scheme.
 */
void Solver::ftcs(void)
{
    double const_dx = h_bar / (2 * m * dx * dx);
    double const_dy = h_bar / (2 * m * dy * dy);

    arma::mat potentiel = ((-1 / h_bar) * V0) - 2 * const_dx - 2 * const_dy;

    arma::mat nrpart = rpart - dt * ((potentiel % ipart) +
        const_dx * (arma::shift(ipart, -1) + arma::shift(ipart, +1)) +
        const_dy * (arma::shift(ipart, -1, 1) + arma::shift(ipart, +1, 1)));

    arma::mat nipart = ipart + dt * ((potentiel % rpart) +
        const_dx * (arma::shift(rpart, -1) + arma::shift(rpart, +1)) +
        const_dy * (arma::shift(rpart, -1, 1) + arma::shift(rpart, +1, 1)));

    rpart = nrpart;
    ipart = nipart;
}

/**
 * \brief      BTCS compute scheme.
 */
void Solver::btcs(void)
{
    /* TODO */
}

/**
 * \brief      CTCS compute scheme.
 */
void Solver::ctcs(void)
{
    /* TODO */
}
