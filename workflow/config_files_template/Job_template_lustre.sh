#!/bin/bash
#SBATCH --job-name=CICA_project_replace_domain_replace_index_replace_model_replace_experiment_replace 
#SBATCH --output=CICA_project_replace_domain_replace_index_replace_model_replace_experiment_replace.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=n_procs_replace
#SBATCH --time=time_replace
#SBATCH --mem-per-cpu=ram_replace
#SBATCH --partition=meteo_long



#DIRECTORIES
WORKDIR=$SLURM_SUBMIT_DIR/
RUNDIR=$SLURM_SUBMIT_DIR/
cfile=config_var_replace
jobfile=job_file_replace
outfile=FAO_project_replace_domain_replace_index_replace_model_replace_experiment_replace.out

config="$(basename $cfile .yml)"
job="$(basename $jobfile .sh)"

Date=$(date +'%Y%m%d%H%M%S')
logfile=$RUNDIR/${config}_${Date}.log
echo python runners/pipeline/run_climate_pipeline.py $cfile
echo $logfile
echo $jobfile
source /nfs/home/gmeteo/chantreuxa/mambaforge/etc/profile.d/conda.sh
source activate climate-data-pipeline-xclim-update

python root_replace/runners/pipeline/run_climate_pipeline.py $cfile > $logfile 2>&1

end_log=$( tail -n 1 $logfile )
end_message=${end_log##*—}
if [ "$end_message" == " Finished" ]; then
    mkdir -p $RUNDIR/save_finished/$dataset/logs/
    mkdir -p $RUNDIR/save_finished/$dataset/jobs/
    mkdir -p $RUNDIR/save_finished/$dataset/outs/
    mv $logfile $RUNDIR/save_finished/$dataset/logs/.
    mv $jobfile $RUNDIR/save_finished/$dataset/jobs/.
    mv $outfile $RUNDIR/save_finished/$dataset/outs/.
else
    mkdir -p $RUNDIR/save_error/$dataset/logs/
    mkdir -p $RUNDIR/save_error/$dataset/jobs/
    mkdir -p $RUNDIR/save_error/$dataset/outs/
    mv $logfile $RUNDIR/save_error/$dataset/logs/.
    mv $jobfile $RUNDIR/save_error/$dataset/jobs/.
    mv $outfile $RUNDIR/save_error/$dataset/outs/.
fi
