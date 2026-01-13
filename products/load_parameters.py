import numpy as np
from dataclasses import dataclass


def urban_vars():
    list_urban=["t","tx","tn","tnn","txx","tx35","tx40","tr","dtr","fd","cd","hd","huss","sfcwind","rsds","rlds"]
    return list_urban

def CMIP5_model_list():
    model_list=["CCCma_CanESM2_r1i1p1"
    , "CCCma_CanESM2_r2i1p1"
    , "CNRM-CERFACS_CNRM-CM5_r1i1p1"
    , "ICHEC_EC-EARTH_r12i1p1"
    , "ICHEC_EC-EARTH_r14i1p1"
    , "IPSL_IPSL-CM5A-MR_r1i1p1"
    , "MOHC_HadGEM2-ES_r1i1p1"
    , "MOHC_HadGEM2-ES_r2i1p1"
    , "MPI-M_MPI-ESM-LR_r1i1p1"
    , "MPI-M_MPI-ESM-LR_r2i1p1"
    , "MPI-M_MPI-ESM-LR_r3i1p1"
    , "MPI-M_MPI-ESM-MR_r1i1p1"
    , "NCC_NorESM1-M_r1i1p1"
    , "BCC_bcc-csm1-1-m_r1i1p1"
    , "BCC_bcc-csm1-1_r1i1p1"
    , "CCCma_CanCM4_r1i1p1"
    , "CMCC_CMCC-CESM_r1i1p1"
    , "CMCC_CMCC-CMS_r1i1p1"
    , "CMCC_CMCC-CM_r1i1p1"
    , "CSIRO-BOM_ACCESS1-0_r1i1p1"
    , "CSIRO-BOM_ACCESS1-3_r1i1p1"
    , "CSIRO-QCCCE_CSIRO-Mk3-6-0_r1i1p1"
    , "LASG-CESS_FGOALS-g2_r1i1p1"
    , "MOHC_HadCM3_r1i1p1"
    , "MOHC_HadGEM2-CC_r1i1p1"
    , "NASA-GISS_GISS-E2-R_r6i1p1"
    , "NCAR_CCSM4_r1i1p1"
    , "NOAA GFDL_GFDL-CM3_r1i1p1"
    , "NOAA GFDL_GFDL-ESM2G_r1i1p1"
    , "NOAA GFDL_GFDL-ESM2M_r1i1p1"
    , "NSF-DOE-NCAR_CESM1-BGC_r1i1p1"
    , "NSF-DOE-NCAR_CESM1-CAM5_r1i1p1"
]
    return model_list
def new_name_var(var):
    Dict={"pr":"r",
            "r01mm":"r01",
            "r10mm":"r10",
            "r20mm":"r20",
            "pethg":"pet",
            "r01mmbaisimip":"r01baisimip",
            "r10mmbaisimip":"r10baisimip",
            "r20mmbaisimip":"r20baisimip",}
    if var in list(Dict.keys()):    
        return Dict[var]
    else:
        return var
def obs_datasets():
    list_obs=["ERA5","ERA5-Land","EOBS","E-OBS","ORAS5","ORAS-5","ERA5-land","CERRA","CERRAURB","CERRARUR","CARRA","CPC","BERKELEY","SSTSAT"]
    return list_obs

def proj_datasets():
    list_proj=["CMIP6","CORDEX-EUR-11","CORDEX-EUR","CMIP5","CORDEX-CORE", "CORDEX-EUR-11URB","CORDEX-EUR-11RUR","CORDEX-COREURB","CORDEX-CORERUR"]
    return list_proj

def list_datasets():
    list_obs=obs_datasets()
    list_proj=proj_datasets()
    return list_obs + list_proj

def check_temporal_resolution_out(var,file=False,v2=False):
    """
    Function to determine the final temporal resolution based on the variable.
    
    Parameters:
    var (str): Variable name.
    file (bool, optional): Flag to indicate if the resolution should be adjusted for file naming. Default is False.
    
    Returns:
    str: Final temporal resolution.
    """
    if index_only(var) in ["cd","cdd","hd"]:
        temporal_resolution="year"
        if file:
            temporal_resolution="yr"
        if v2:
             temporal_resolution="YS"

    else:
        temporal_resolution="month"
        if file:
            temporal_resolution="mon"
        if v2:
             temporal_resolution="MS"

    return temporal_resolution


def index_only(index):
    if "ba" in index:
        index=index.split("ba")[0]  
    return index

def threshold_parameter(index):
    """
    Function to associate thresold value for cfile for index
    """
    
    index=index_only(index)
     
    if index in ["hd"]:
        #extr_digits=list(filter(str.isdigit, index))
        #threshold_value=int("".join(extr_digits))
        threshold_value="15.5"
    elif index in ["cd"]:
        threshold_value="22"
    else:
        threshold_value="None"
    threshold=f"threshold : {threshold_value}"
    return threshold,threshold_value

def check_aggregation(index):
    """
    Function to check if the index represents only an aggregation.
    
    Parameters:
    index (str): Index value.
    
    Returns:
    bool: True if it represents only an aggregation, False otherwise.
    """
    only_aggregation = index in ["pr", "sfcwind", "psl", "huss", "prsn", "rsds", "sst", "siconc", "mrso", "clt", "rlds", "evspsbl","mrro"]
    return only_aggregation


def load_AR6():    
    Dict_AR6={}
    List_Name=['Greenland/Iceland', 'N.W.North-America', 'N.E.North-America', 'W.North-America', 'C.North-America', 'E.North-America', 'N.Central-America', 'S.Central-America', 'Caribbean', 'N.W.South-America', 'N.South-America', 'N.E.South-America', 'South-American-Monsoon', 'S.W.South-America', 'S.E.South-America', 'S.South-America', 'N.Europe', 'West&Central-Europe', 'E.Europe', 'Mediterranean', 'Sahara', 'Western-Africa', 'Central-Africa', 'N.Eastern-Africa', 'S.Eastern-Africa', 'W.Southern-Africa', 'E.Southern-Africa', 'Madagascar', 'Russian-Arctic', 'W.Siberia', 'E.Siberia', 'Russian-Far-East', 'W.C.Asia', 'E.C.Asia', 'Tibetan-Plateau', 'E.Asia', 'Arabian-Peninsula', 'S.Asia', 'S.E.Asia', 'N.Australia', 'C.Australia', 'E.Australia', 'S.Australia', 'New-Zealand', 'E.Antarctica', 'W.Antarctica', 'Arctic-Ocean', 'N.Pacific-Ocean', 'Equatorial.Pacific-Ocean', 'S.Pacific-Ocean', 'N.Atlantic-Ocean', 'Equatorial.Atlantic-Ocean', 'S.Atlantic-Ocean', 'Arabian-Sea', 'Bay-of-Bengal', 'Equatorial.Indic-Ocean', 'S.Indic-Ocean', 'Southern-Ocean']
    List_id=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
    List_acronym=['GIC', 'NWN', 'NEN', 'WNA', 'CNA', 'ENA', 'NCA', 'SCA', 'CAR', 'NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA', 'NEU', 'WCE', 'EEU', 'MED', 'SAH', 'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF', 'MDG', 'RAR', 'WSB', 'ESB', 'RFE', 'WCA', 'ECA', 'TIB', 'EAS', 'ARP', 'SAS', 'SEA', 'NAU', 'CAU', 'EAU', 'SAU', 'NZ', 'EAN', 'WAN', 'ARO', 'NPO', 'EPO', 'SPO', 'NAO', 'EAO', 'SAO', 'ARS', 'BOB', 'EIO', 'SIO', 'SOO']
    Dict_AR6["Name"]=List_Name
    Dict_AR6["Id"]=List_id
    Dict_AR6["Acronym"]=List_acronym

    Dict_AR6["Ocean"]=["ARO","NPO","EPO","SPO","NAO","EAO","SAO","ARS","BOB","EIO","SIO","SOO"]
    Dict_AR6["Continent"]=["GIC","NWN","NEN","WNA","CNA","ENA","NCA","SCA","NWS","NSA","NES","SAM","SWS","SES","SSA","NEU","WCE","EEU","SAH","WAF","CAF","NEAF","SEAF","WSAF","ESAF","MDG","RAR","WSB","ESB","RFE","WCA","ECA","TIB","EAS","ARP","SAS","NAU","CAU","EAU","SAU","NZ","EAN","WAN"]				
    Dict_AR6["Continent_and_ocean"]=["CAR","MED","SEA"]
    Dict_AR6["Russia"]=["EEU","WSB","ESB","RAR"]
    Dict_AR6["Europe"]=["MED","WCE","NEU"]
    Dict_AR6["Not_Europe"]=['GIC', 'NWN', 'NEN', 'WNA', 'CNA', 'ENA', 'NCA', 'SCA', 'CAR', 'NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA', 'EEU', 'SAH', 'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF', 'MDG', 'RAR', 'WSB', 'ESB', 'RFE', 'WCA', 'ECA', 'TIB', 'EAS', 'ARP', 'SAS', 'SEA', 'NAU', 'CAU', 'EAU', 'SAU', 'NZ', 'EAN', 'WAN', 'ARO', 'NPO', 'EPO', 'SPO', 'NAO', 'EAO', 'SAO', 'ARS', 'BOB', 'EIO', 'SIO', 'SOO']
    Dict_AR6["Antartid"]=["WAN","EAN"]

    return Dict_AR6


@dataclass
class Dataset:
    project:str
    root:str

    def __post_init__(self):
        self.project_type = self.load_project_type()
        self.var_list=self.calculated_vars()
        self.available_exp=self.calculated_experiments()
        self.domain_list=self.load_domains()
        self.list_var_new =self.load_new_vars()



    def load_project_type(self):
        if self.project not in obs_datasets():
            project_type="projection"
        else:
            project_type="observation"
        return project_type

    def proj_fullname(self,var=False):
        if self.project=="CMIP5":
            if var==False:
                var="t"
            temporal_resolution=self.check_temporal_resolution_in(var)["temporal_resolution"]
            projection_full=f"projections-cmip5-{temporal_resolution}-single-levels"


        if self.project=="CMIP6":
            projection_full="projections-cmip6"
        if "CORDEX" in self.project:
            projection_full="projections-cordex-domains-single-levels"
        return projection_full 

    def load_experiments(self):
        if "CMIP6" in self.project:
            list_experiments = ["historical","ssp119", "ssp126", "ssp245", "ssp370", "ssp585"]
        elif self.project=="CMIP5" or "CORDEX" in self.project:
            if "CORE" in self.project:
                list_experiments = ["historical", "rcp26",  "rcp85"]
            else:
                list_experiments = ["historical", "rcp26", "rcp45", "rcp85"]
        elif self.project in obs_datasets():
            list_experiments = ["None"]
        else:
            raise ValueError("Invalid project specified.")
        return list_experiments

    def no_calculated_experiments(self):
        if self.project == 'CORDEX-COREadsad':
            list_experiments = ["rcp45"]
        else :
            list_experiments=[]
        return list_experiments

    def calculated_experiments(self):
        
        list_experiments =self.load_experiments()
        list_not_calculated=self.no_calculated_experiments()
        for experiment in list_not_calculated:
            list_experiments.remove(experiment)
        return list_experiments


    def load_period(self,var,version="v2"):
        if self.project=="CMIP6":
            fut_period = np.arange(2015, 2101)
            if "ba" in var and version=="v1":
                hist_period = np.arange(1950, 2015)
            else:
                hist_period = np.arange(1850, 2015)
        elif "CORDEX" in self.project:
            hist_period = np.arange(1970, 2006)
            fut_period = np.arange(2006, 2101)
        elif self.project in ["CMIP5"]:
            fut_period = np.arange(2006, 2101)
            if "ba" in var and version=="v1":
                hist_period = np.arange(1950, 2006)
            else:
                hist_period = np.arange(1850, 2006)
        elif self.project in ["ERA5-Land","ERA5-land"]:
        
                hist_period = np.arange(1950, 2025)
                fut_period = None
        elif self.project in ["E-OBS"]:
                hist_period = np.arange(1950, 2025)
                fut_period = None
        elif self.project in ["ORAS5","ORAS-5"]:
                hist_period = np.arange(1958, 2015)
                fut_period = None
        elif self.project in ["ERA5"]:
            hist_period = np.arange(1940, 2025) 
            fut_period = None
        elif "CERRA" in self.project:
            hist_period = np.arange(1985, 2022) 
            fut_period = None
        elif self.project in ["CPC"]:
            hist_period = np.arange(1979, 2021) 
            fut_period = None
        elif self.project in ["BERKELEY"]:
            hist_period = np.arange(1881, 2018) 
            fut_period = None
        elif self.project in ["SSTSAT"]:
            hist_period = np.arange(1982, 2023) 
            fut_period = None
        else:
            raise ValueError("Invalid project specified.")

        return hist_period,fut_period

    def load_period_model(self,var,version="v2"):
        hist_period,fut_period=load_period(var,version="v2")
        return hist_period,fut_period


    def load_years(self,var,experiment,version="v2"):
        hist_period,fut_period = self.load_period(var,version=version)
        if experiment=="historical" or experiment=="None":
            years=[hist_period[0],hist_period[-1]]
        else:
            years=[fut_period[0],fut_period[-1]]
        return years




    def check_vars_proj(self,v2=True,):
        if self.project == 'CMIP6':
            var_list=['tx35',"t",'rx1day','rx5day',"cdd","tx40","txx","tnn","cd","hd","fd","tx","tn","pr","sfcwind","psl","huss","prsn","rsds","sst","mrsos","clt","rlds","evspsbl","siconc","spei6","spi6","mrro","tx35bals","tx40bals"]
        elif self.project == 'CMIP5':
            var_list=["pr","tnn", "tx", "tn", "tx35", "tx40", "rx1day", "rx5day", "sfcwind", "t", "txx","huss"]
        elif 'CORDEX-EUR-11' in self.project :
            var_list=['tx35',"t",'rx1day','rx5day',"cdd","tx40","txx","tnn","fd","tx","tn","pr","sfcwind","huss","rsds","rlds","evspsbl","spi6","spei6","mrro","clt"]
        elif 'CORDEX-CORE' in self.project :
            var_list=['tx35',"t",'rx1day','rx5day',"cdd","tx40","txx","tnn","fd","tx","tn","pr","sfcwind","huss","rsds","rlds","evspsbl","spi6","clt"]
        elif self.project == 'ERA5':
            var_list=['tx35',"t",'rx1day','rx5day',"cdd","tx40","txx","tnn","cd","hd","fd","tx","tn","pr","sfcwind","psl","prsn","rsds","sst","mrsos","clt","rlds","evspsbl","siconc","spei6","spi6","mrro"]
        elif self.project == 'ERA5-Land':
            var_list=['tx35',"t",'rx1day','rx5day',"cdd","tx40","txx","tnn","cd","hd","fd","tx","tn","pr","prsn","rsds","mrsos","rlds","evspsbl","spi6","mrro"]
        elif self.project in ['EOBS', "E-OBS"]:
            var_list=["cd","hd","t","pr","cdd","rsds","psl","sfcwind","rx1day","tn","tx","txx","tx35","tx40","fd","rx5day","tnn"]
        elif self.project == 'ORAS5':
            var_list=["sst","siconc"]
        elif self.project=="BERKELEY":
            var_list=[]
        elif self.project=="CPC":
            var_list=[]
        elif "CERRA" in self.project:
            var_list=[]
        elif self.project=="SSTSAT":
            var_list=[]            
        else:
            raise ValueError(f"Invalid project specified. ")
        if v2==True:
            var_list.extend(self.calculated_vars_v2())
            var_list=list(set(var_list))
        return var_list

    def no_calculated_vars(self):
        if self.project == 'CORDEX-CORE':
            var_list=["psl"]
        else :
            var_list=[]
        return var_list

    def calculated_vars_v2(self):
        if self.project in proj_datasets():
            var_list=["cddbaisimip","fdbals","cdbals","hdbals","txbals","tnbals","tbals","tx35bals","tx40bals","tx35baisimip","tx40baisimip","fdbaisimip",
                      "cdbaisimip","hdbaisimip","txbaisimip","tnbaisimip","tbaisimip","r01mmbaisimip","sdiibaisimip",
                      "trbaisimip","dtrbaisimip","r10mmbaisimip","r20mmbaisimip","trbals","dtrbals","spei6reference","spi6reference"]
        else:
            var_list=[]
        if self.project not in ["ORAS5"]:
            var_list.extend(["r01mm","sdii","tr","dtr","r10mm","r20mm","pethg","spi6","spei6"])
            var_list=list(set(var_list))
        if self.project not in ["ORAS5","ERA5-Land"] and "CORE" not in self.project:
            var_list.extend(["psl"])
        if self.project =="CMIP5":
            var_list.extend(["cdd","fd","cd","hd","prsn", "rsds","mrsos","sst","siconc","evspsbl","mrro","clt","rlds"])
        if self.project =="ERA5-Land":
            var_list.extend(["sfcwind","cd"])
        if  'CORDEX-EUR-11' in self.project :
            var_list.extend(["cd","hd"])
        if 'CORDEX-CORE' in self.project :
            var_list.extend(["cd","hd"])
        if self.project=="BERKELEY":
            var_list=["t","tn","tx","tnn","txx","tx35","tx40","fd","hd","cd","tr","dtr"]
        if self.project=="CPC":
            var_list=["cdd","pr","r10mm","r20mm","r01mm","sdii","rx1day","rx5day","spi6"]

        if "CERRA" in self.project:
            var_list=["prsn","evspsbl","t","tn","tnn","tx","txx","tx35","tx40","cdd","cd","hd","fd","pr","rx1day","rx5day","pethg","r10mm","r20mm","r01mm","sdii","dtr","tr","psl","spi6","spei6","sfcwind","clt","rsds","rlds"]
        if self.project=="SSTSAT":
            var_list=["sst"]
        return var_list
    
    def exclusive_vars(self,version="v2"):
        var_list2=self.calculated_vars_v2()
        var_list1=self.check_vars_proj(v2=False)
        # Convert lists to sets
        set_list1 = set(var_list1)
        set_list2 = set(var_list2)

        unique_to_list1 = set_list1 - set_list2
        unique_to_list1 = list(unique_to_list1)

        unique_to_list2 = set_list2 - set_list1
        unique_to_list2 = list(unique_to_list2)
        if version=="v2":
            return unique_to_list2
        elif version=="v1":
            return unique_to_list1
    def calculated_vars(self):
        var_list=self.check_vars_proj()
        #print(var_list)
        var_not_calculated=self.no_calculated_vars()
        for var in var_not_calculated :
            if var in var_list:
                var_list.remove(var)
        return var_list
    def load_new_vars(self):
        if self.project=="CMIP5" :
            list_var_new=["sfcwind","prsn","rsds","psl","huss","mrsos","mrro","clt","rlds","evspsbl","fdbals","cdbals","hdbals","fdbaisimip","cdbaisimip","hdbaisimip""spei6"]
        if self.project=="CMIP6":
            list_var_new=["rsds","psl","huss","mrsos","mrro","clt","rlds","evspsbl","fdbals","cdbals","hdbals","fdbaisimip","cdbaisimip","hdbaisimip","spei6"]
        if "CORDEX" in self.project:
            list_var_new=["rsds","psl","huss","mrsos","mrro","clt","rlds","evspsbl","fdbals","cdbals","hdbals","fdbaisimip","cdbaisimip","hdbaisimip","spei6"]
        else: 
            list_var_new=[]
        return list_var_new
    
    
    def variable_type(self):
        only_land_vars=["mrro","mrsos","tx35","tx40","tx35bals","tx40bals","tx35baisimip","tx40baisimip"]
        only_sea_vars=["sst","siconc"]
        land_vars=[]
        ocean_vars=[]
        both_vars=[]
        var_list=self.check_vars_proj()
        for var in var_list:
            if var in only_land_vars:
                land_vars.append(var)
            elif var in only_sea_vars:
                ocean_vars.append(var)
            else:
                both_vars.append(var)
        return land_vars,ocean_vars,both_vars

    def check_temporal_resolution_in(self,var,v2=False):
        """
        Function to determine the initial input variable's temporal resolution based on the project and variable.
        
        Parameters:
            var (str): Variable name.Porque
            project (str, optional): Project name. Default is "CMIP6".
        
        Returns:
            str: Initial temporal resolution.
        """

        varin_list = cds_varin(var)
        Dict_resolution={}
        for varin in varin_list:
            Dict_resolution[varin]={}
            if self.project in ["CMIP6","ERA5","ERA5-land","ERA5-Land","EOBS","CMIP5","ORAS5"]:
                if varin in ["tas", "tasmax", "tasmin", "pr"] or self.project=="EOBS":
                    Dict_resolution[varin]["temporal_resolution_cf"] = "daily"
                    Dict_resolution[varin]["temporal_resolution"] = "daily"
                    orig_freq="D"
                else:
                    Dict_resolution[varin]["temporal_resolution_cf"] = "monthly"
                    Dict_resolution[varin]["temporal_resolution"] = "monthly"
                    orig_freq="MS"
            elif "CORDEX" in self.project:
                if varin in ["tas", "tasmax", "tasmin", "pr"] or "CORE" in self.project:
                    if v2==True:
                        Dict_resolution[varin]["temporal_resolution_cf"] = "daily"
                    else:
                        Dict_resolution[varin]["temporal_resolution_cf"] = "day"
                    Dict_resolution[varin]["temporal_resolution"] = "daily_mean"
                    orig_freq="D"
                elif varin in ["mrro"]:
                    Dict_resolution[varin]["temporal_resolution_cf"] = "6hr"
                    Dict_resolution[varin]["temporal_resolution"] = "6_hours"
                    orig_freq="H"

                else:
                    Dict_resolution[varin]["temporal_resolution_cf"] = "mon"
                    Dict_resolution[varin]["temporal_resolution"] = "monthly_mean"
                    orig_freq="MS"
            else:
                raise ValueError(f"Invalid {self.project} project specified and var {varin}.")
            test_var=varin
            test=Dict_resolution[varin]["temporal_resolution_cf"]
        for varin in varin_list :
            if  Dict_resolution[varin]["temporal_resolution_cf"] != test:
                raise ValueError(f"All var should have same resolutuion {varin} is {Dict_resolution[varin]} and {test_var} is {test}")
        return {"temporal_resolution": Dict_resolution[varin]["temporal_resolution"], "temporal_resolution_cf": Dict_resolution[varin]["temporal_resolution_cf"],"orig_freq":orig_freq}



    def check_grid_output(self):
        """
        Function to determine the output grid resolution based on the project.
        
        Parameters:
        project (str): Project name.
        
        Returns:
        float: output Grid resolution  value.
        """
        project=self.project   
        if "CMIP" in project:
            grid_output = 1
        elif 'CORDEX-EUR-11' in project :
            grid_output = 0.12
        elif  'CORDEX_CORE' in project:
            grid_output = 0.25
        elif project in ['ERA5',"ERA5-Land","ERA5-land","EOBS","ORAS5"]:
            grid_output = "raw"
        else:
            raise ValueError("Invalid project specified.")
        
        return grid_output



    def regions_for_domain(self):
    # Define the AR6 reference regions for each CORDEX domains (see Diez-Sierra et. al 2022)
        mosaic = {'NAM': ['NWN', 'NEN', 'WNA', 'CNA', 'ENA'],
                'CAM': ['NCA', 'SCA', 'CAR'],
                'SAM': ['NWS', 'NSA', 'NES', 'SAM', 'SWS', 'SES', 'SSA'],
                'ARC': ['GIC', 'ARO', 'RAR'],
                'EUR': ['NEU', 'WCE', 'MED'],
                'AFR': ['SAH', 'WAF', 'CAF', 'NEAF', 'SEAF', 'WSAF', 'ESAF', 'MDG'],
                'ANT': ['WAN', 'EAN'],
                'CAS': ['WSB', 'ESB', 'EEU'],
                'WAS': ['WCA', 'TIB', 'SAS', 'ARP'],
                'EAS': ['RFE', 'ECA', 'EAS'],
                'SEA': ['SEA'],
                'AUS': ['NAU', 'CAU', 'EAU', 'SAU', 'NZ'],
                'all':["NWN","NEN" ,"WNA" ,"CNA" ,"ENA" ,
                    "NCA" ,"SCA" ,"CAR" ,
                    "NWS" ,"NSA" ,"NES" ,"SAM" ,"SWS" ,"SES" ,"SSA",
                    "GIC","ARO","RAR",
                    "NEU" ,"WCE" ,"MED",
                    "SAH" ,"WAF" ,"CAF" ,"NEAF" ,"SEAF" ,"WSAF" ,"ESAF" ,"MDG", 
                    "EAN" ,"WAN"
                        ,"WSB" ,"ESB","EEU"  ,
                    "WCA" ,"TIB" ,"SAS" ,"ARP" ,
                    "RFE" ,"ECA" ,"EAS" ,
                    "SEA" ,
                    "NAU" ,"CAU" ,"EAU" ,"SAU" ,"NZ",
                    "EAN" ,"WAN" ,"ARO" ,"NPO" ,"EPO" ,"SPO" ,"NAO" ,"EAO" ,"SAO" ,"ARS" ,"BOB" ,"EIO" ,"SIO" ,"SOO",
                    "world" ]       
                    }
        return mosaic
    def list_core(self):
        Dict={}
        list_CORE=["MOHC_HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1",
                "MOHC_HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0" , "MOHC_HadGEM2-ES_r1i1p1_ICTP_RegCM4-4_v0" , "MOHC_HadGEM2-ES_r1i1p1_ICTP_RegCM4-6_v1","MOHC_HadGEM2-ES_r1i1p1_ISU_RegCM4_v4-4-rc8",
                "MPI-M_MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1","MPI-M_MPI-ESM-LR_r3i1p1_GERICS_REMO2015_v1",
                "MPI-M_MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0","MPI-M_MPI-ESM-MR_r1i1p1_ICTP_RegCM4-4_v0","MPI-M_MPI-ESM-MR_r1i1p1_ORNL_RegCM4-7_v0",
                "NCC_NorESM1-M_r1i1p1_GERICS_REMO2015_v1",
                "NCC_NorESM1-M_r1i1p1_ICTP_RegCM4-7_v0","NCC_NorESM1-M_r1i1p1_ICTP_RegCM4-4_v0","NCC_NorESM1-M_r1i1p1_ICTP_RegCM4-6_v1","NCC_NorESM1-M_r1i1p1_ORNL_RegCM4-7_v0",
                "NOAA-GFDL_GFDL-ESM2M_r1i1p1_ICTP_RegCM4-7_v0","NOAA-GFDL_GFDL-ESM2M_r1i1p1_ISU_RegCM4_v4-4-rc8",
                "MIROC_MIROC5_r1i1p1_ORNL-RegCM4-7_v0",
                "MPI-M_MPI-ESM-LR_r1i1p1_ICTP_RegCM4-6_v0","MPI-M_MPI-ESM-LR_r1i1p1_NCAR_RegCM4_v4-4-rc8"]
        list_core_refact=["MOHC_HadGEM2-ES_REMO","MOHC_HadGEM2-ES_RegCM","MPI-M_MPI-ESM-LR_REMO","MPI-M_MPI-ESM-MR_RegCM",
                        "NCC_NorESM1-M_REMO","NCC_NorESM1-M_RegCM","NOAA-GFDL_GFDL-ESM2M_RegCM","MIROC_MIROC5_RegCM",
                        "MPI-M_MPI-ESM-LR_RegCM"]
        Dict["list_core"]=list_CORE

        Dict["list_core_refact"]=list_core_refact
        list_domains=self.load_domains("CORDEX-CORE")
        Dict["list_domains"]=list_domains
        return Dict

    def load_domains(self):
        if self.project=="CORDEX-EUR-11":
            domain_list=["EUR"]
        elif self.project=="CORDEX-CORE":
            domain_list= ["AFR","AUS","CAM","EAS","EUR","NAM","SAM","SEA","WAS"]
        else:
            domain_list=["None"]
        return domain_list


    def associate_core(self):
        Dict={}

        for model in self.list_core()["list_core_refact"]:
            Dict[model]={}
        Dict["MOHC_HadGEM2-ES_REMO"]["models"]=["MOHC_HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1"]
        Dict["MOHC_HadGEM2-ES_RegCM"]["models"]=["MOHC_HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0" , "MOHC_HadGEM2-ES_r1i1p1_ICTP_RegCM4-4_v0" , "MOHC_HadGEM2-ES_r1i1p1_ICTP_RegCM4-6_v1","MOHC_HadGEM2-ES_r1i1p1_ISU_RegCM4_v4-4-rc8"]       
        Dict["MPI-M_MPI-ESM-LR_REMO"]["models"]=["MPI-M_MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1","MPI-M_MPI-ESM-LR_r3i1p1_GERICS_REMO2015_v1"]
        Dict["MPI-M_MPI-ESM-MR_RegCM"]["models"]=["MPI-M_MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0","MPI-M_MPI-ESM-MR_r1i1p1_ICTP_RegCM4-4_v0","MPI-M_MPI-ESM-MR_r1i1p1_ORNL_RegCM4-7_v0"]
        Dict["NCC_NorESM1-M_REMO"]["models"]=["NCC_NorESM1-M_r1i1p1_GERICS_REMO2015_v1"]
        Dict["NCC_NorESM1-M_RegCM"]["models"]=["NCC_NorESM1-M_r1i1p1_ICTP_RegCM4-7_v0","NCC_NorESM1-M_r1i1p1_ICTP_RegCM4-4_v0","NCC_NorESM1-M_r1i1p1_ICTP_RegCM4-6_v1","NCC_NorESM1-M_r1i1p1_ORNL_RegCM4-7_v0"]
        Dict["NOAA-GFDL_GFDL-ESM2M_RegCM"]["models"]=["NOAA-GFDL_GFDL-ESM2M_r1i1p1_ICTP_RegCM4-7_v0","NOAA-GFDL_GFDL-ESM2M_r1i1p1_ISU_RegCM4_v4-4-rc8"]
        Dict["MIROC_MIROC5_RegCM"]["models"]=["MIROC_MIROC5_r1i1p1_ORNL-RegCM4-7_v0"]
        Dict["MPI-M_MPI-ESM-LR_RegCM"]["models"]=["MPI-M_MPI-ESM-LR_r1i1p1_ICTP_RegCM4-6_v0","MPI-M_MPI-ESM-LR_r1i1p1_NCAR_RegCM4_v4-4-rc8","MPI-M_MPI-ESM-LR_r1i1p1_ICTP_RegCM4-6_v1"]

        Dict["MOHC_HadGEM2-ES_REMO"]["domains"]=["AFR","AUS","CAM","EAS","EUR","NAM","SAM","SEA","WAS"]
        Dict["MOHC_HadGEM2-ES_RegCM"]["domains"]=["AFR","AUS","CAM","EAS","EUR","NAM","SAM","SEA"]
        Dict["MPI-M_MPI-ESM-LR_REMO"]["domains"]=["AFR","AUS","CAM","EAS","EUR","NAM","SAM","SEA","WAS"]
        Dict["MPI-M_MPI-ESM-MR_RegCM"]["domains"]=["AFR","AUS","CAM","EAS","SAM","SEA","WAS"]
        Dict["NCC_NorESM1-M_REMO"]["domains"]=["AFR","AUS","CAM","EAS","EUR","NAM","SAM","SEA","WAS"]
        Dict["NCC_NorESM1-M_RegCM"]["domains"]=["AFR","AUS","EAS","EUR","SAM","SEA","WAS"]
        Dict["NOAA-GFDL_GFDL-ESM2M_RegCM"]["domains"]=["CAM","NAM","SEA"]
        Dict["MIROC_MIROC5_RegCM"]["domains"]=["EUR","WAS"]
        Dict["MPI-M_MPI-ESM-LR_RegCM"]["domains"]=["EUR","NAM"]

        return Dict
    

