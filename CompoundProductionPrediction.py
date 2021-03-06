# Script to make predict the production of value-added compounds by the contribution of underground reactions
# Created: 23 June 2019
# Author: Szabolcs Cselgo Kovacs
# Contact: kovszasz@gmail.com

import cobra, cobra.io, cobra.test, csv,pandas,codecs, email, smtplib,sys,random,pickle
#from cameo import load_model
import escher
from email.mime.text import MIMEText
from cobra import Reaction, Metabolite, Model
pandas.options.display.max_rows = 100
from random import randint
from cobra.util.solver import linear_reaction_coefficients
model="underground.xml"
model=cobra.io.sbml.create_cobra_model_from_sbml_file(model, False, False,False)
#model=cobra.io.load_json_model(model)
model.reactions.ATPM.lower_bound=3.15

BIOMASS=model.reactions.Ec_biomass_iJO1366_core_53p95M
def white_space_remover(string): #while reading the '.txt' files, the lines are separated wit the '\n' character. This function removes '\n' from the end of the strings.
    string=list(string)
    string.pop()
    string="".join(string)
    return string


def binary_saver(obj,name): #We store the results and other important variables binary. It is easer and faster to read and save.
    f=''
    outfile=open(f+name,'wb')
    pickle.dump(obj,outfile)
    outfile.close()

def binary_loader(name): #We store the results and other important variables binary. It is easer and faster to read and save.
    f=''
    infile=open(f+name,'rb')
    return pickle.load(infile)

#blocked_reaction_list=cobra.flux_analysis.find_blocked_reactions(model)# Remove reactions that are blocked: no flux through these reactions possible. This will reduce the search space for the solver, if not done already.

underground_reactions={} #the key is the ID of the underground reaction, the item is information about its reversibility.
for i in model.reactions:
    if i.id.find("u0")>-1:
#        if i.id in blocked_reaction_list:#only if blocked reactions are determined
#            model.reactions.get_by_id(i.id).lower_bound=0
#            model.reactions.get_by_id(i.id).upper_bound=0
#        else:
        underground_reactions[i.id]=i.reversibility

def c_atom_number(s): #For the yield calculation it is required to get information about the carbon atom numbe of the given compund. This function calculates it from the formula of the compound.
    e=model.reactions.get_by_id(s).metabolites
    for i in e.keys():
        a=model.metabolites.get_by_id(i.id).formula
    C={}
    for i in ['Cl','H','O','S','P','C','N']:
        if a.find(i)>-1:
            a=a.replace(i,','+i+';')
    l1=a.split(',')
    for i in l1:
        p=i.split(';')
        if len(p)==2:
            if p[1]=='':
                C[p[0]]=1
            else:
                C[p[0]]=int(p[1])
    return C['C']

def yield_prediction(target,g,C_source,turned_on_underground_reactions):
    """
    #   target: the ID of the target compound which production is in demand
    #   g:the percent of the maximum biomass production (according to Maranas et al., 2006, generally the biomass production is constrained to the 0.1 of its maximum production value)
    #   C_source: ID of the exchange reaction of the carbon source, which maximum uptake rate will be set to 10
    #   turned_on_underground_reactions: individual underground reactions turn on/turn off (list)
    """
    EX=[] #list of exchange reactions
    error=[]
    for i in model.reactions:
        if i.id.find("biomass")>-1:
            BIOMASS=i
        if i.id.find("EX_",0)==0:
            EX.append(i.id)


    model.reactions.get_by_id(C_source).lower_bound=-10
    model.reactions.get_by_id(C_source).upper_bound=1000
    model.objective={BIOMASS:1}


    for i in underground_reactions.keys(): # turns off each underground reaction in order to get the only the native metabolic network.
        model.reactions.get_by_id(i).lower_bound=0
        model.reactions.get_by_id(i).upper_bound=0
    reference=cobra.flux_analysis.pfba(model).fluxes[BIOMASS.id]#calculating the maximum biomass production of the native metabolic network
    for i in turned_on_underground_reactions: # turns on each desired underground reaction, which is included in the turned_on_underground_reactions list
        if underground_reactions[i]:
            model.reactions.get_by_id(i).lower_bound=-1000
            model.reactions.get_by_id(i).upper_bound=1000
        else:
            model.reactions.get_by_id(i).lower_bound=0
            model.reactions.get_by_id(i).upper_bound=1000

    model.reactions.get_by_id(BIOMASS.id).lower_bound= 0.0734 #reference*g #set the biomass production contstraint
    target_metabol=model.metabolites.get_by_id(target)
    # creating the DEMAND reaction for the target compound
    target_demand=Reaction("DM_target")
    target_demand.add_metabolites({target_metabol:-1.0})
    model.add_reaction(target_demand)
    model.reactions.get_by_id("DM_target").lower_bound=0
    model.reactions.get_by_id("DM_target").upper_bound=1000
    model.objective={model.reactions.DM_target:1}
    solution=cobra.flux_analysis.pfba(model)
    compound_yield=abs((solution.fluxes["DM_target"]/solution.fluxes[C_source])*(c_atom_number("DM_target")/c_atom_number(C_source)))
    print("Yield of ",target_metabol,":\t",abs(compound_yield))
    f=open('ethylene_glycol.txt','w')
    reaction_data={}
    for i in solution.fluxes.keys():
        reaction_data[i]=solution.fluxes[i]
        #print(i,';',model.reactions.get_by_id(i).reaction,';',model.reactions.get_by_id(i).bounds,';',solution.fluxes[i])
        f.write("{i};{reaction};{lb};{ub};{fl}\n".format(i=i,reaction=model.reactions.get_by_id(i).reaction,lb=model.reactions.get_by_id(i).lower_bound,ub=model.reactions.get_by_id(i).upper_bound,fl=solution.fluxes[i]))
    f.close()
    #escher.Builder(map_name='Underground_u0228',map_json='underground_u0228_Map.json',model=model,reaction_data=reaction_data,local_host='http://localhost:7778/').save_html('Ug_u0228_escher.html')
    model.reactions.get_by_id(C_source).lower_bound=0
    model.remove_reactions(['DM_target'])
    return compound_yield

#------------------------------------------------------------RUN prediction---------------------------------------------------------------------------------

carbon_sources=["EX_glc_e"]#,"EX_glyc_e","EX_xyl_D_e","EX_ac_e","EX_fru_e","EX_fuc_L_e","EX_arab_L_e","EX_succ_e"]

#x={"id":["asp_D_c","abt_c","C01904_c","alein_c","ptrc_c"]}
targets=[]
with open("native_target_compounds.txt") as target_compounds:
    for i in target_compounds:
        targets.append(white_space_remover(i))

targets=['C01380_c']
def increment(x,y):
    if abs(x)<1e-4 and abs(y)<1e-4:
        return 0
    elif y!=0:
        return (x/y)-1
    else:
        return x


result={}
biomass_constraint=0.1
#targets={'pro_L_c'}
data=[]
for target in targets:
    result[target]={}
    row=[]
    columns=[]
    for carbon_source in carbon_sources:
        native=yield_prediction(target,biomass_constraint,carbon_source,[])
        underground=yield_prediction(target,biomass_constraint,carbon_source,['u0228'])#underground_reactions.keys())
        result[target][carbon_source]=[native,underground]
        columns.append(carbon_source+':native')
        columns.append(carbon_source+':underground')
        columns.append(carbon_source+':relative_yield')
        relative_yield=0
        if native==0.0:
            if underground>0:
                relative_yield=underground
        else:
            relative_yield=(underground/native)-1
        row.append(native)
        row.append(underground)
        row.append(relative_yield)
    data.append(row)
#df = pandas.DataFrame(data,index=targets,columns=columns)
#cobra.io.save_json_model(model,'underground_u0228.json')
#df.to_csv(r'results/underground_yield_results_all.txt', header=None, index=targets, sep=',', mode='a')
#binary_saver(result, 'native_underground_comparison')