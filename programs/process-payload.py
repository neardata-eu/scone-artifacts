import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pandas as pd

from sm.engine.config import SMConfig
from sm.engine.annotation_lithops.annotation_job import LocalAnnotationJob
from sm.engine.annotation_lithops.executor import Executor

from tests.annotation_lithops.test_annotation_job import \
    MOCK_DECOY_ADDUCTS, MOCK_FORMULAS, make_test_imzml, make_test_molecular_db


SM_CONFIG_FILE = "sm-config-singularity.json"
DS_CONFIG_FILE = "ds-config-local.json"


def run_job():

    sm_config = json.load(open(SM_CONFIG_FILE, "r"))
    ds_config = json.load(open(DS_CONFIG_FILE, "r"))

    executor = Executor(sm_config["lithops"])

    SMConfig.set_path(SM_CONFIG_FILE)

    ds_config['database_ids'] = [1]
    ds_config['isotope_generation']['adducts'] = ['[M]+']
    ds_config['image_generation']['ppm'] = 0.001
    ds_config['fdr']['decoy_sample_size'] = len(MOCK_DECOY_ADDUCTS)

    with make_test_imzml(ds_config) as (imzml_path, ibd_path):
        with make_test_molecular_db() as moldb_path:
            with TemporaryDirectory() as out_dir:
                job = LocalAnnotationJob(
                    imzml_file="Image5.imzML",
                    ibd_file="Image5.ibd",
                    moldb_files=["mol_db1.tsv"],
                    sm_config=sm_config,
                    ds_config=ds_config,
                    executor=executor,
                    out_dir=out_dir,
                    use_cache=False
                )

                job.run(debug_validate=True, perform_enrichment=False)

                output_files = list(Path(out_dir).glob('*.png'))
                print('len(output_files)')
                print(len(output_files))
                print('len(MOCK_FORMULAS) * 4')
                print(len(MOCK_FORMULAS) * 4)

                results_csv = pd.read_csv(Path(out_dir) / 'results_mol_db1.csv')
                print('len(results_csv)')
                print(len(results_csv))
                print('len(MOCK_FORMULAS)')
                print(len(MOCK_FORMULAS))


if __name__ == "__main__":
    run_job()
