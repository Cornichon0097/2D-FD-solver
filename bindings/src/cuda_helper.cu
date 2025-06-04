#include <stdlib.h>
#include <stdio.h>

#include "cuda_helper.h"

#define N_ELEM(n) (n * n)
#define MAT_SIZE(n) (N_ELEM(n) * sizeof(double))

#define INBOUND(idx, ncols) ((idx % ncols > 0) && (idx % ncols < ncols - 1) \
                             && (idx > ncols) && (idx < ncols * (ncols - 1)))

struct d_param {
        size_t ncols;
        double h_bar, m;
        double dx, dy, dt;
};

struct d_data {
        double *v0;
        double *rpart, *ipart;
        double *trpart, *tipart;
        struct d_param *param;
};

struct d_data *d_data = NULL;
size_t ncols;

/**
 * \brief      { function_description }
 */
__global__ void ftcs(const double *const v0, const double *const rpart,
                     const double *const ipart, double *const trpart,
                     double *const tipart, const struct d_param *const p)
{
        int idx = blockDim.x * blockIdx.x + threadIdx.x;

        double const_dx = p->h_bar / (2 * p->m * p->dx * p->dx);
        double const_dy = p->h_bar / (2 * p->m * p->dy * p->dy);
        double potentiel;

        if (INBOUND(idx, p->ncols)) {
                potentiel = ((-1 / p->h_bar) * v0[idx])
                            - 2 * const_dx - 2 * const_dy;

                trpart[idx] = rpart[idx] - p->dt
                              * ((potentiel * ipart[idx])
                              + const_dx * (ipart[idx - p->ncols]
                                            + ipart[idx + p->ncols])
                              + const_dy * (ipart[idx - 1]
                                            + ipart[idx + 1]));

                tipart[idx] = ipart[idx] + p->dt
                              * ((potentiel * rpart[idx])
                              + const_dx * (rpart[idx - p->ncols]
                                            + rpart[idx + p->ncols])
                              + const_dy * (rpart[idx - 1]
                                            + rpart[idx + 1]));
    }
}

/**
 * \brief      Initializes the device matrix.
 *
 * \param[in]  h_data  The h data
 *
 * \return     { description_of_the_return_value }
 */
__host__ int init_device_matrix(const struct h_data *const h_data)
{
        cudaError_t err = cudaMalloc(&(d_data->v0), MAT_SIZE(h_data->ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(d_data->rpart), MAT_SIZE(h_data->ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(d_data->ipart), MAT_SIZE(h_data->ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(d_data->trpart), MAT_SIZE(h_data->ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(d_data->tipart), MAT_SIZE(h_data->ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(d_data->v0, h_data->v0, MAT_SIZE(h_data->ncols),
                         cudaMemcpyHostToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(d_data->rpart, h_data->rpart, MAT_SIZE(h_data->ncols),
                         cudaMemcpyHostToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(d_data->ipart, h_data->ipart, MAT_SIZE(h_data->ncols),
                         cudaMemcpyHostToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        return 0;
}

/**
 * \brief      Initializes the device memory.
 *
 * \param[in]  h_data  The h data
 *
 * \return     { description_of_the_return_value }
 */
__host__ int init_device_memory(const struct h_data *const h_data)
{
        cudaError_t err;

        if (d_data != NULL) {
                fprintf(stderr, "Device memory already initialized\n");
                return -1;
        }

        d_data = (struct d_data *) malloc(sizeof(struct d_data));

        if (d_data == NULL) {
                perror("malloc()");
                return -1;
        }

        if (init_device_matrix(h_data) != 0)
                return -1;

        err = cudaMalloc(&(d_data->param), sizeof(struct d_param));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        cudaMemcpy(d_data->param, &(h_data->ncols), sizeof(struct d_param),
                   cudaMemcpyHostToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        ncols = h_data->ncols;

        return 0;
}

/**
 * \brief      { function_description }
 *
 * \param[in]  scheme  The scheme
 *
 * \return     { description_of_the_return_value }
 */
__host__ int execute_kernel(const char scheme)
{
        cudaError_t err;

        switch (scheme) {
        case 'f':
                ftcs<<<1, ncols>>>(d_data->v0, d_data->rpart, d_data->ipart,
                                   d_data->trpart, d_data->tipart,
                                   d_data->param);
                break;
        default:
                break;
        }

        err = cudaGetLastError();

        if (err != cudaSuccess) {
                fprintf(stderr, "Failed to launch kernel:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        cudaDeviceSynchronize();

        err = cudaMemcpy(d_data->rpart, d_data->trpart, MAT_SIZE(ncols),
                         cudaMemcpyDeviceToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(d_data->ipart, d_data->tipart, MAT_SIZE(ncols),
                         cudaMemcpyDeviceToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        return 0;
}

/**
 * \brief      Retrieves results.
 *
 * \param[out] res   The resource
 *
 * \return     The results.
 */
__host__ int retrieve_results(struct h_data *const res)
{
        cudaError_t err;

        if (res == NULL) {
                fprintf(stderr, "Impossible to retrieve results in (null)\n");
                return -1;
        }

        err = cudaMemcpy(res->rpart, d_data->rpart, MAT_SIZE(ncols),
                   cudaMemcpyDeviceToHost);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy device memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(res->ipart, d_data->ipart, MAT_SIZE(ncols),
                   cudaMemcpyDeviceToHost);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy device memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        return 0;
}

/**
 * \brief      { function_description }
 */
__host__ int clean_up_device(void)
{
        cudaError_t err = cudaDeviceReset();

        if (err != cudaSuccess) {
                fprintf(stderr, "Failed to clean the device:"
                                " %s\n", cudaGetErrorString(err));
                return -1;
        }

        return 0;
}
