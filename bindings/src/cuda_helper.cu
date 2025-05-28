#include <stdlib.h>
#include <stdio.h>

#include "cuda_helper.h"

#define N_ELEM(n) (n * n)
#define MAT_SIZE(n) (N_ELEM(n) * sizeof(double))

#define INBOUND(idx, ncols) ((idx % ncols > 0) && (idx % ncols < ncols - 1) \
                             && (idx > ncols) && (idx < ncols * (ncols - 1)))

struct d_data *d_data = NULL;

double *d_rpart, *d_ipart;

static size_t ncols = 0;

/**
 * \brief      { function_description }
 */
__global__ void ftcs(double *drp, double *dip, struct d_data *const d)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;

    double const_dx = d->h_bar / (2 * d->m * d->dx * d->dx);
    double const_dy = d->h_bar / (2 * d->m * d->dy * d->dy);
    double potentiel;

    if (INBOUND(idx, d->ncols)) {
        potentiel = ((-1 / d->h_bar) * d->v0[idx])
                    - 2 * const_dx - 2 * const_dy;

        drp[idx] = d->rpart[idx] - d->dt
                * ((potentiel * d->ipart[idx])
                + const_dx * (d->ipart[idx - d->ncols]
                        + d->ipart[idx + d->ncols])
                + const_dy * (d->ipart[idx - 1] + d->ipart[idx + 1]));

        dip[idx] = d->ipart[idx] + d->dt
                * ((potentiel * d->rpart[idx])
                + const_dx * (d->rpart[idx - d->ncols]
                        + d->rpart[idx + d->ncols])
                + const_dy * (d->rpart[idx - 1] + d->rpart[idx + 1]));
    }
}

/**
 * \brief      Initializes the device matrix.
 *
 * \param[in]  h_data  The h data
 *
 * \return     { description_of_the_return_value }
 */
__host__ int init_device_matrix(struct d_data *const th_data, const struct d_data *const h_data)
{
        cudaError_t err = cudaMalloc(&d_rpart, MAT_SIZE(ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&d_ipart, MAT_SIZE(ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(th_data->v0), MAT_SIZE(ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(th_data->v0, h_data->v0, MAT_SIZE(ncols),
                         cudaMemcpyHostToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(th_data->rpart), MAT_SIZE(ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(th_data->rpart, h_data->rpart, MAT_SIZE(ncols),
                         cudaMemcpyHostToDevice);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy host memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMalloc(&(th_data->ipart), MAT_SIZE(ncols));

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMalloc(): failed to allocate memory:"
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(th_data->ipart, h_data->ipart, MAT_SIZE(ncols),
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
__host__ int init_device_memory(const struct d_data *const h_data)
{
        struct d_data tmp_h_data;

        if (ncols != 0) {
                fprintf(stderr, "Device memory already initialized\n");
                return -1;
        }

        ncols = h_data->ncols;

        if (init_device_matrix(&tmp_h_data, h_data) != 0)
                return -1;

        tmp_h_data.ncols = h_data->ncols;
        tmp_h_data.h_bar = h_data->h_bar;
        tmp_h_data.m     = h_data->m;
        tmp_h_data.dx    = h_data->dx;
        tmp_h_data.dy    = h_data->dy;
        tmp_h_data.dt    = h_data->dt;

        cudaMalloc(&d_data, sizeof(struct d_data));
        cudaMemcpy(d_data, &tmp_h_data, sizeof(struct d_data), cudaMemcpyHostToDevice);

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
                ftcs<<<1, ncols>>>(d_rpart, d_ipart, d_data);
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

        return 0;
}

/**
 * \brief      Retrieves results.
 *
 * \param[out] res   The resource
 *
 * \return     The results.
 */
__host__ int retrieve_results(struct d_data *const res)
{
        struct d_data tmp_h_data;
        cudaError_t err;

        if (res == NULL) {
                fprintf(stderr, "Impossible to retrieve results in (null)\n");
                return -1;
        }

        cudaMemcpy(d_data, &tmp_h_data, sizeof(struct d_data), cudaMemcpyDeviceToHost);

        err = cudaMemcpy(&(tmp_h_data.rpart), res->rpart, MAT_SIZE(ncols),
                         cudaMemcpyDeviceToHost);

        if (err != cudaSuccess) {
                fprintf(stderr, "cudaMemcpy(): failed to copy device memory: "
                                "%s\n", cudaGetErrorString(err));
                return -1;
        }

        err = cudaMemcpy(&(tmp_h_data.ipart), res->ipart, MAT_SIZE(ncols),
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
