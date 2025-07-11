/**
 * \file       solver.h
 */
#ifndef SOLVER_H
#define SOLVER_H

#include <armadillo>

class Solver
{
public:
    /**
     * \brief      Solver constructor.
     *
     * \param      <unnamed>  The potentiel field
     * \param      <unnamed>  The real part
     * \param      <unnamed>  The imaginary part
     * \param[in]  <unnamed>  The scheme
     * \param[in]  <unnamed>  The x speed
     * \param[in]  <unnamed>  The y speed
     * \param[in]  <unnamed>  The delta time
     */
    Solver(arma::mat&, arma::mat&, arma::mat&,
           std::string, double, double, double);

    /**
     * \brief      Solevr constructor.
     *
     * \param      <unnamed>  The potentiel field
     * \param      <unnamed>  The real part
     * \param      <unnamed>  The imaginary part
     * \param[in]  <unnamed>  The Planck constant
     * \param[in]  <unnamed>  The particle masse
     * \param[in]  <unnamed>  The scheme
     * \param[in]  <unnamed>  The x speed
     * \param[in]  <unnamed>  The y speed
     * \param[in]  <unnamed>  The delta time
     */
    Solver(arma::mat&, arma::mat&, arma::mat&, double, double,
           std::string, double, double, double);

    /**
     * \brief      Compute the next psi value.
     */
    void compute(void);

    /**
     * \brief      Returns the real part.
     *
     * \return     The current real part.
     */
    arma::mat r_part(void);

    /**
     * \brief      Returns the imaginary part.
     *
     * \return     The current imaginary part.
     */
    arma::mat i_part(void);

private:
    arma::mat V0;
    arma::mat rpart, ipart;

    std::string scheme;

    double h_bar, m;
    double dx, dy, dt;

    /**
     * \brief      Adds padding to a matrix.
     *
     * \param[in]  <unnamed>  A square matrix
     *
     * \return     The matrix with padding.
     */
    arma::mat padded(arma::mat);

    /**
     * \brief      FTCS compute scheme.
     */
    void ftcs(void);

    /**
     * \brief      BTCS compute scheme:
     */
    void btcs(void);

    /**
     * \brief      CTCS compute scheme.
     */
    void ctcs(void);
};

#endif /* solver.h */
