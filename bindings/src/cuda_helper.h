#ifndef CUDA_HELPER_H
#define CUDA_HELPER_H

struct h_data {
        double *v0;
        double *rpart, *ipart;
        size_t ncols;
        double h_bar, m;
        double dx, dy, dt;
};

int init_device_memory(const struct h_data *h_data);

int execute_kernel(char scheme);

int retrieve_results(struct h_data *res);

int clean_up_device(void);

#endif /* cuda_helper.h */
