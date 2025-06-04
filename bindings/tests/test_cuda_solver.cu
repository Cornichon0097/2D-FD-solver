#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <assert.h>

#include <cuda_helper.h>

#define SIZE 5

#define COUNT 1

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

void print_mat(const char *const head, const double *const mat, size_t size)
{
        int i, j;

        printf("%s\n", head);

        for (i = 0; i < size; ++i) {
                for (j = 0; j < size; ++j)
                        printf("[%f]", mat[i * size + j]);

                printf("\n");
        }
}

void print_data(const struct h_data *const h_d)
{
        print_mat("rpart:", h_d->rpart, h_d->ncols);
        print_mat("ipart:", h_d->ipart, h_d->ncols);
}

int main(void)
{
        struct h_data h_d;
        struct h_data results;
        int i;

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

        print_data(&h_d);

        results.rpart = (double *) malloc(SIZE * SIZE * sizeof(double));
        results.ipart = (double *) malloc(SIZE * SIZE * sizeof(double));
        results.ncols = SIZE;

        if (init_device_memory(&h_d) != 0) {
                clean_up_device();
                exit(EXIT_FAILURE);
        }

        retrieve_results(&results);
        print_data(&results);

        assert(memcmp(h_d.rpart, results.rpart, h_d.ncols * h_d.ncols * sizeof(double)) == 0);
        assert(memcmp(h_d.ipart, results.ipart, h_d.ncols * h_d.ncols * sizeof(double)) == 0);

        for (i = 0; i < COUNT; ++i)
                execute_kernel('f');

        retrieve_results(&results);
        print_data(&results);

        assert(memcmp(h_d.rpart, results.rpart, h_d.ncols * h_d.ncols * sizeof(double)) != 0);
        assert(memcmp(h_d.ipart, results.ipart, h_d.ncols * h_d.ncols * sizeof(double)) != 0);

        clean_up_device();
        free(results.rpart);
        free(results.ipart);
        free(h_d.v0);
        free(h_d.rpart);
        free(h_d.ipart);

        return EXIT_SUCCESS;
}
