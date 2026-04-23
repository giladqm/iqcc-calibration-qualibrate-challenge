# %% {Imports}
import numpy as np
import xarray as xr

from qm.qua import *

from iqcc_calibration_tools.qualibrate_config.qualibrate.node import QualibrationNode
from quam_builder.architecture.superconducting.qpu import FluxTunableQuam as Quam
from qualibrate import NodeParameters
from qualibration_libs.parameters import get_qubits
from typing import Optional, List
from iqcc_calibration_tools.storage.iqcc_cloud_data_storage_utils.download_state_and_wiring import download_state_and_wiring

# %% {Node initialisation}
description = """Init and shuffle the QUAM state for the Qualibrate challenge. """

class Parameters(NodeParameters):
    qubits: Optional[List[str]] = ["qA1", "qA2"]
    shuffle: bool=True

# Be sure to include [Parameters, Quam] so the node has proper type hinting
node = QualibrationNode[Parameters, Quam](
    name="00_init_challenge",  # Name should be unique
    description=description,  # Describe what the node is doing, which is also reflected in the QUAlibrate GUI
    parameters=Parameters(),  # Node parameters defined under quam_experiment/experiments/node_name
)

# Any parameters that should change for debugging purposes only should go in here
# These parameters are ignored when run through the GUI or as part of a graph
@node.run_action(skip_if=node.modes.external)
def custom_param(node: QualibrationNode[Parameters, Quam]):
    """Allow the user to locally set the node parameters for debugging purposes, or execution in the Python IDE."""
    # You can get type hinting in your IDE by typing node.parameters.
    # node.parameters.qubits = ["q1", "q2"]
    pass


# Instantiate the QUAM class from the state file
# node.machine = Quam.load("C:/git/SQA-2025-Conference/iqcc-calibration/reference_state_qolab/")
download_state_and_wiring("arbel") 
node.machine = Quam.load()
node.machine.active_qubit_names = ["qA1", "qA2"]


# %% {Shuffle_state}
@node.run_action()
def update_state(node: QualibrationNode[Parameters, Quam]):
    """Update the relevant parameters if the qubit data analysis was successful."""
    node.namespace["qubits"] = get_qubits(node)
    with node.record_state_updates():
        for q in node.namespace["qubits"]:
            if node.parameters.shuffle:
                q.resonator.f_01 += np.random.randint(-5_000_000, 5_000_000)
                q.f_01 += np.random.randint(-5_000_000, 5_000_000)
                q.xy.operations["x180"].amplitude *= (np.random.randint(5, 15) / 10)
                q.T1 *= (np.random.randint(5, 15) / 10)
                q.T2ramsey *= (np.random.randint(5, 15) / 10)


# %% {Save_results}
@node.run_action()
def save_results(node: QualibrationNode[Parameters, Quam]):
    node.save()
