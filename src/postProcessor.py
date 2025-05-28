from pyevtk.hl import imageToVTK
import numpy as np

def generate_init_vti(V0, psi_real_part, psi_imag_part,):
    """
    use to generate the vti for the initial state

    @param V0 potential field
    @param psi_real_part, real part of the psi function
    @param psi_imag_part, imaginary part of the psi function
    """
    Psi_module = np.sqrt(np.power(psi_real_part, 2) + np.power(psi_imag_part, 2))
    file_name = "vti/initial_state"
    imageToVTK(file_name, pointData=
            {
                'psi_module' : Psi_module.astype(np.float32).reshape((psi_real_part.shape[0], psi_real_part.shape[1], 1), order='C'),
                'psi_real_part' : psi_real_part.astype(np.float32).reshape((psi_real_part.shape[0], psi_real_part.shape[1], 1), order='C'),
                'psi_imag_part' : psi_imag_part.astype(np.float32).reshape((psi_imag_part.shape[0], psi_imag_part.shape[1], 1), order='C'),
                'V0' : V0.astype(np.float32).reshape((V0.shape[0], V0.shape[1], 1), order='C')
            })


def generate_vti(V0, psi_imag_part, psi_real_part, id):
    """
    use to generate the vti for any state

    @param V0 potential field
    @param psi_real_part, real part of the psi function
    @param psi_imag_part, imaginary part of the psi function
    @id the id of the state, to differentiate the vti files
    """
    Psi_module = np.sqrt(np.power(psi_real_part, 2) + np.power(psi_imag_part, 2))
    file_name = "vti/output_vti__%d" % (id)
    imageToVTK(file_name, pointData=
            {
                'psi_module' : Psi_module.astype(np.float32).reshape((psi_real_part.shape[0], psi_real_part.shape[1], 1), order='C'),
                'psi_real_part' : psi_real_part.astype(np.float32).reshape((psi_real_part.shape[0], psi_real_part.shape[1], 1), order='C'),
                'psi_imag_part' : psi_imag_part.astype(np.float32).reshape((psi_imag_part.shape[0], psi_imag_part.shape[1], 1), order='C'),
                'V0' : V0.astype(np.float32).reshape((V0.shape[0], V0.shape[1], 1), order='C')
            })

