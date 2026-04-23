from quam.core import quam_dataclass
from quam_builder.architecture.superconducting.qpu import FluxTunableQuam

__all__ = ["Quam"]


@quam_dataclass
class Quam(FluxTunableQuam):
    """Minimal Quam root: only the hooks needed by QualibrationNode.save()."""

    @classmethod
    def remove_macros_from_qubits(cls, quam_obj: "Quam") -> None:
        """Remove all macros from qubits and qubit pairs."""
        for qubit_data in quam_obj.qubits.values():
            if hasattr(qubit_data, "macros"):
                qubit_data.macros = {}
