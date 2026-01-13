import xarray as xr
import matplotlib.pyplot as plt 
import os 
import pandas as pd

def plot_triple_map(ds_a, ds_b, var_name, time_index=0, cmap="viridis", diff_cmap="RdBu_r",output_dir="outputs"):
    

    os.makedirs(output_dir,exist_ok=True)


    

    # Seleccionar variable y tiempo
    da_a = ds_a[var_name].isel(time=time_index)
    da_b = ds_b[var_name].isel(time=time_index)

    if 'time' in da_a.coords:
        timestamp = pd.to_datetime(da_a['time'].values).strftime('%Y%m')
    else:
        timestamp=f't{time_index:02d}'

    # Calcular diferencia
    da_diff = da_a - da_b


    # Crear figura
    fig, axes = plt.subplots(1, 3, figsize=(15, 5), subplot_kw={'projection': None})


    im1 = da_a.plot(ax=axes[0], cmap=cmap, add_colorbar=True)
    axes[0].set_title('Mapa A')


    im2 = da_b.plot(ax=axes[1], cmap=cmap, add_colorbar=True)
    axes[1].set_title('Mapa B')


    im3 = da_diff.plot(ax=axes[2], cmap=diff_cmap, add_colorbar=True)
    axes[2].set_title('A - B')


    plt.tight_layout()

    filename= f"{var_name}_comparacion_{timestamp}.png"
    output_file = os.path.join(output_dir, filename)

    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close(fig)
    # Cerrar datasets
    print(output_file)



def plot_single_map(ds, var_name, time_index=0, cmap='viridis',output_dir='outputs'):
    os.makedirs(output_dir,exist_ok=True)

    da=ds[var_name].isel(time=time_index)

    if 'time' in da.coords:
        timestamp = pd.to_datetime(da['time'].values).strftime('%Y%m')
    else:
        timestamp = f't{time_index:02d}'


    fig,ax = plt.subplots(figsize=(6,5))

    da.plot(ax=ax,cmap=cmap,add_colorbar=True)
    ax.set_title(f'Mapa', fontsize=10)
    

    filename=f'{var_name}_{timestamp}.png'
    output_file=os.path.join(output_dir,filename)
    plt.savefig(output_file,dpi=150,bbox_inches='tight')

    plt.close(fig)
    

def main():
    
    file_a="/gpfs/projects/meteo/DATA/CERRA-land/final_products-ruben-test/Global/CERRA/mon/pr/gr006/day/pr_gr006_mon_CERRA_day_200001_200012.nc"
   
    file_b="/gpfs/projects/meteo/DATA/CERRA-land/final_products-ruben-test/Global/CERRA/mon/pr/gr006/day/pr_gr006_mon_CERRA_day_198501_198512.nc"


    ds_a=xr.open_dataset(file_a)
    ds_b=xr.open_dataset(file_b)
    plot_triple_map(ds_a,ds_b,"pr")    
    plot_single_map(ds_b,'pr')
    plot_single_map(ds_a,'pr')
    
    ds_a.close()
    ds_b.close()



if __name__=='__main__':
    main()
