def list_core():
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
    return Dict


def associate_core(self):
    Dict={}

    for model in list_core()["list_core_refact"]:
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
def core_list():
    core_list=[                
       'AFR-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',  
       'AFR-22_MOHC-HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0',
       'AFR-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'AFR-22_MPI-M-MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0',
       'AFR-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'AFR-22_NCC-NorESM1-M_r1i1p1_ICTP_RegCM4-7_v0',

       'AUS-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'AUS-22_MOHC-HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0',
       'AUS-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'AUS-22_MPI-M-MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0',
       'AUS-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'AUS-22_NCC-NorESM1-M_r1i1p1_ICTP_RegCM4-7_v0',

       'CAM-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'CAM-22_MOHC-HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0',
       'CAM-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'CAM-22_MPI-M-MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0',
       'CAM-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'CAM-22_NOAA-GFDL-GFDL-ESM2M_r1i1p1_ICTP_RegCM4-7_v0',
       'CAS-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'CAS-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'CAS-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',

       'EAS-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'EAS-22_MOHC-HadGEM2-ES_r1i1p1_ICTP_RegCM4-4_v0',
       'EAS-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'EAS-22_MPI-M-MPI-ESM-MR_r1i1p1_ICTP_RegCM4-4_v0',
       'EAS-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'EAS-22_NCC-NorESM1-M_r1i1p1_ICTP_RegCM4-4_v0',

       'EUR-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'EUR-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'EUR-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',

       'NAM-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'NAM-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'NAM-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',

       'SAM-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'SAM-22_MOHC-HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0',
       'SAM-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'SAM-22_MPI-M-MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0',
       'SAM-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'SAM-22_NCC-NorESM1-M_r1i1p1_ICTP_RegCM4-7_v0',

       'SEA-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'SEA-22_MOHC-HadGEM2-ES_r1i1p1_ICTP_RegCM4-7_v0',
       'SEA-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'SEA-22_MPI-M-MPI-ESM-MR_r1i1p1_ICTP_RegCM4-7_v0',
       'SEA-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'SEA-22_NCC-NorESM1-M_r1i1p1_ICTP_RegCM4-7_v0',

       'WAS-22_MOHC-HadGEM2-ES_r1i1p1_GERICS_REMO2015_v1',
       'WAS-22_MPI-M-MPI-ESM-LR_r1i1p1_GERICS_REMO2015_v1',
       'WAS-22_MPI-M-MPI-ESM-MR_r1i1p1_ORNL_RegCM4-7_v0',
       'WAS-22_NCC-NorESM1-M_r1i1p1_GERICS_REMO2015_v1',
       'WAS-22_NCC-NorESM1-M_r1i1p1_ORNL_RegCM4-7_v0']
    return core_list
