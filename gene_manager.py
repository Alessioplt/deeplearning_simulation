import json
import all_genes_functions
#"0000111": [INTERNAL, "N"],
all_sensor = {
            "1" : all_genes_functions.EDB,
            "2" : all_genes_functions.SBD,
            "3" : all_genes_functions.DS,
            "4" : all_genes_functions.DN,
            "5" : all_genes_functions.DW,
            "6" : all_genes_functions.DE,
            "7" : all_genes_functions.RNI,
            "8" : all_genes_functions.DSW,
            "9" : all_genes_functions.DSE,
            "10" : all_genes_functions.DNW,
            "11" : all_genes_functions.DNE
}

all_action = {

            "1": all_genes_functions.MS,
            "2": all_genes_functions.MN,
            "3": all_genes_functions.MW,
            "4": all_genes_functions.ME,
            "5": all_genes_functions.MR,
            "6": all_genes_functions.MSW,
            "7": all_genes_functions.MSE,
            "8": all_genes_functions.MNW,
            "9": all_genes_functions.MNE
}


def getTypeGene(type):
    keys = []
    if type == "S":
        for key in all_sensor.keys():
            value = str(bin(int(key))).replace('0b', "").zfill(7)
            keys.append(value)
    elif type == "A":
        for key in all_action.keys():
            value = str(bin(int(key))).replace('0b', "").zfill(7)
            keys.append(value)
    return keys


def callFunction(name, params=None, type = None):
    name = str(int(name, 2))
    if params is None:
        params = []
    if type=="S":
        return all_sensor[name](params)
    else:
        return all_action[name](params)
