from logging import INFO
from typing import List, Tuple, Union, Optional, Dict
import numpy as np
import flwr as fl
from flwr.common import FitRes, Scalar, Parameters
from flwr.server.client_proxy import ClientProxy
from flwr.common.logger import log


class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(
            self,
            server_round: int,
            results: List[Tuple[fl.server.client_proxy.ClientProxy, fl.common.FitRes]],
            failures: List[Union[Tuple[ClientProxy, FitRes], BaseException]],
    ) -> Tuple[Optional[Parameters], Dict[str, Scalar]]:
        # Call aggregate_fit from base class (FedAvg) to aggregate parameters and metrics
        aggregated_parameters, aggregated_metrics = super().aggregate_fit(server_round, results, failures)

        if aggregated_parameters is not None:
            # Convert `Parameters` to `List[np.ndarray]`
            aggregated_ndarrays: List[np.ndarray] = fl.common.parameters_to_ndarrays(aggregated_parameters)

            # Save aggregated_ndarrays
            log(INFO, f"Saving round {server_round} aggregated_ndarrays...")
            np.savez(f"/app/output/server/round-{server_round}-weights.npz", *aggregated_ndarrays)

        return aggregated_parameters, aggregated_metrics


if __name__ == "__main__":
    fl.common.logger.configure(identifier="myFlowerExperiment", filename="server_log.txt")
    strategy = SaveModelStrategy()
    fl.server.start_server(config=fl.server.ServerConfig(num_rounds=3), strategy=strategy)
