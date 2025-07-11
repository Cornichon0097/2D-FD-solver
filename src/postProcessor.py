""" @package postProcessor.py
Provides a VTK files generator.
"""
import numpy as np

from pyevtk.hl import imageToVTK


def generate_vtk(v0, psi_real_part, psi_imag_part, file_name):
    """ Generates VTK file.

    @param V0            the field potential,
    @param psi_real_part the real part of the psi function,
    @param psi_imag_part the imaginary part of the psi function,
    @param file_name     the output filename.
    """
    Psi_module = np.sqrt(np.power(psi_real_part, 2) + np.power(psi_imag_part, 2))

    imageToVTK(file_name, pointData = {
        'psi_module':    Psi_module.astype(np.float32).reshape((psi_real_part.shape[0], psi_real_part.shape[1], 1), order='C'),
        'psi_real_part': psi_real_part.astype(np.float32).reshape((psi_real_part.shape[0], psi_real_part.shape[1], 1), order='C'),
        'psi_imag_part': psi_imag_part.astype(np.float32).reshape((psi_imag_part.shape[0], psi_imag_part.shape[1], 1), order='C'),
        'V0':            v0.astype(np.float32).reshape((v0.shape[0], v0.shape[1], 1), order='C')
    })


def generate_init_vti(v0, psi_real_part, psi_imag_part):
    """ Generates VTI file for the initial state.

    @param V0            the field potential,
    @param psi_real_part the real part of the psi function,
    @param psi_imag_part the imaginary part of the psi function.
    """
    generate_vtk(v0, psi_real_part, psi_imag_part, "vti/initial_state")


def generate_vti(v0, psi_imag_part, psi_real_part, id):
    """ Generates VTI for any state

    @param V0            the field potential,
    @param psi_real_part the real part of the psi function,
    @param psi_imag_part the imaginary part of the psi function,
    @param id            the state ID.
    """
    generate_vtk(v0, psi_real_part, psi_imag_part, "vti/output_vti__%04d" % (id))
