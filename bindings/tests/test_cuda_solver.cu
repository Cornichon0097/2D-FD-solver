#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include <cuda_helper.h>

#define SIZE 5

double *rand_mat(size_t size)
{
        double *mat = (double *) malloc(size * size * sizeof(double));
        size_t i;

        if (mat != NULL) {
                for (i = 0; i < size * size; ++i)
                        mat[i] = drand48();
        }

        return mat;
}

int main(void)
{
        struct h_data h_d;

        srand(time(NULL));

        h_d.v0 = rand_mat(SIZE);
        h_d.rpart = rand_mat(SIZE);
        h_d.ipart = rand_mat(SIZE);
        h_d.ncols = SIZE;
        h_d.h_bar = 1.0;
        h_d.m = 1.0;
        h_d.dx = 1.0;
        h_d.dy = 1.0;
        h_d.dt = 5.0;

        if (init_device_memory(&h_d) != 0) {
                clean_up_device();
                exit(EXIT_FAILURE);
        }

        execute_kernel('f');
        retrieve_results(&h_d);
        clean_up_device();

        free(h_d.v0);
        free(h_d.rpart);
        free(h_d.ipart);

        return EXIT_SUCCESS;
}
