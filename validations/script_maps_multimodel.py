from maps import single_map
import matplotlib.pyplot as plt
import xarray


save_dir="/gpfs/users/chantreuxa/FAO/validation_multimodel/"
# List of file paths
var="sfcwind"
file_paths = [
    f"CORDEX-CORE_{var}_historical_1970.nc",
    f"CORDEX-CORE_{var}_rcp26_2006.nc",
    f"CORDEX-CORE_{var}_rcp85_2006.nc"
]

# Load each dataset, plot the variable, and save the plot
for file_path in file_paths:
    experiment = file_path.split("_")[2]
    year = file_path.split("_")[3].split(".")[0]
    file_path = save_dir + file_path

    # Load the dataset
    ds = xarray.open_dataset(file_path)

    # Assuming the variable of interest is named 'values_all'
    variable = 'number_of_simulations'

    if variable in ds:
        sum_values = ds[variable]
        mask = sum_values >= 3
        ds[variable] = ds[variable].where(mask, drop=True)
        # Plot the variable with a specified color scale
        data=ds[variable]
        fig=single_map(data,model_name='', experiment=experiment, year="",month=None, var1_name='number_of_simulations',
            units="number",dataset1="FAO",vscale_name="multimodel_number")
        # Add a title to the plot
        plt.title(f"Plot of {variable} for {var} and {experiment} equal or above 3")
        # Save the plot as an image file
        output_file = f"{file_path.replace('.nc', '')}_above_3_plot.png"
        plt.savefig(output_file, bbox_inches='tight')

        # Close the plot to free memory
        plt.close()

        print(f"Plot saved as {output_file}")
# Close the dataset to free resources
    ds.close()
