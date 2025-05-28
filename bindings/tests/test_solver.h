#include <cxxtest/TestSuite.h>

#include <iostream>
#include <armadillo>

#include "../solver.h"

using namespace std;

class TestSolver: public CxxTest::TestSuite
{
public:

    void Test_Init_Def(void)
    {
        Solver mySolver;

        TS_ASSERT_EQUALS(mySolver.h_bar, 1.);
        TS_ASSERT_EQUALS(mySolver.m, 1.);
        TS_ASSERT_EQUALS(mySolver.dt, 1.);
        TS_ASSERT_EQUALS(mySolver.dx, 1.);
        TS_ASSERT_EQUALS(mySolver.dy, 1.);
        TS_ASSERT_EQUALS(mySolver.methode, "ftcs");
    }

    void Test_Init(void)
    {
        arma::mat _V0(3, 3);
        arma::mat _imag_part(3, 3);
        arma::mat _real_part(3, 3);

        _V0.ones();
        _imag_part.ones();
        _real_part.ones();
        double _h_bar = 1.0;
        double _m = 1.0;
        std::string _methode = "ftcs";
        double _dx = 1.0;
        double _dy = 1.0;
        double _dt = 1.0;

        Solver mySolver(_V0, _real_part, _imag_part, _h_bar, _m, _methode, _dx, _dy, _dt);

        arma::mat expected_mat =
        {
            {1, 1, 1},
            {1, 1, 1},
            {1, 1, 1},
        };

        TS_ASSERT_EQUALS(mySolver.h_bar, _h_bar);
        TS_ASSERT_EQUALS(mySolver.m, _m);
        TS_ASSERT_EQUALS(mySolver.methode, _methode);
        TS_ASSERT_EQUALS(mySolver.dx, _dx);
        TS_ASSERT_EQUALS(mySolver.dy, _dy);
        TS_ASSERT_EQUALS(mySolver.dt, _dt);

        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                TS_ASSERT_EQUALS(expected_mat(i, j), mySolver.V0(i, j));
                TS_ASSERT_EQUALS(expected_mat(i, j), mySolver.psi_real_part(i, j));
                TS_ASSERT_EQUALS(expected_mat(i, j), mySolver.psi_imag_part(i, j));
            }
        }
    }

    void Test_adding_zeros(void)
    {
        Solver mySolver;

        arma::mat _V0(3, 3);
        _V0.ones();
        arma::mat V0_with_zeros = mySolver.mat_add_zeros(_V0);

        arma::mat expected_result =
        {
            {0, 0, 0, 0, 0},
            {0, 1, 1, 1, 0},
            {0, 1, 1, 1, 0},
            {0, 1, 1, 1, 0},
            {0, 0, 0, 0, 0}
        };

        for (int i = 0; i < 4; ++i)
        {
            for (int j = 0; j < 4; ++j)
                TS_ASSERT_EQUALS(expected_result(i, j), V0_with_zeros(i, j));
        }
    }

    void Test_FTCS_With_Zeros(void)
    {
        arma::mat _V0(3, 3);
        arma::mat _imag_part(3, 3);
        arma::mat _real_part(3, 3);

        _V0.zeros();
        _imag_part.zeros();
        _real_part.zeros();
        double _h_bar = 1.0;
        double _m = 1.0;
        std::string _methode = "ftcs";
        double _dx = 1.0;
        double _dy = 1.0;
        double _dt = 1.0;

        Solver mySolver(_V0, _real_part, _imag_part, _h_bar, _m, _methode, _dx, _dy, _dt);

        arma::mat expected_result =
        {
            {0, 0, 0},
            {0, 0, 0},
            {0, 0, 0}
        };

        mySolver.ftcs();

        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                TS_ASSERT_EQUALS(expected_result(i, j), mySolver.psi_imag_part(i, j));
                TS_ASSERT_EQUALS(expected_result(i, j), mySolver.psi_real_part(i, j));
            }
        }
    }

    void Test_FTCS(void)
    {

        arma::mat _V0(2, 2);
        arma::mat _imag_part(2, 2);
        arma::mat _real_part(2, 2);

        _V0.ones();
        _imag_part.ones();
        _real_part.zeros();

        double _h_bar = 1.0;
        double _m = 1.0;
        std::string _methode = "ftcs";
        double _dx = 1.0;
        double _dy = 1.0;
        double _dt = 1.0;

        Solver mySolver(_V0, _real_part, _imag_part, _h_bar, _m, _methode, _dx, _dy, _dt);

        mySolver.calcul_psi_t_plus_dt();

    }
};
