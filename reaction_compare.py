# Script to make predict the production of value-added compounds by the contribution of underground reactions
# Created: 23 June 2019
# Author: Szabolcs Cselgo Kovacs
# Contact: kovszasz@gmail.com

import cobra, cobra.io, cobra.test, csv,pandas,codecs, email, smtplib,sys,random,pickle
#from cameo import load_model
from email.mime.text import MIMEText
from cobra import Reaction, Metabolite, Model
pandas.options.display.max_rows = 100
from random import randint
from cobra.util.solver import linear_reaction_coefficients
model="underground.xml"
underground=cobra.io.sbml.create_cobra_model_from_sbml_file(model, False, False,False)
model="heterologous.xml"
heterologous=cobra.io.sbml.create_cobra_model_from_sbml_file(model, False, False,False)

heterologous_reactions=[i for i in heterologous.reactions if i.id.find('MetaCyc')>-1]
underground_reactions=[i for i in underground.reactions if i.id.find('u0')>-1]   

heterologous.reactions.EX_glc_lp_e_rp_.lower_bound=-10
heterologous.reactions.ATPM.lower_bound=3.15

underground.reactions.EX_glc_e.lower_bound=-10
underground.reactions.ATPM.lower_bound=3.15


het_blocked = cobra.flux_analysis.find_blocked_reactions(heterologous)
ug_blocked = cobra.flux_analysis.find_blocked_reactions(underground)

het_MetaCyc=[i for i in het_blocked if i.find('MetaCyc')>-1]
ug_u0=[i for i in ug_blocked if i.find('u0')>-1]
METDICT={}
for i in heterologous_reactions:
    for j in i.metabolites:
        if len(j.name)==6 and j.name[0]=='C':
            METDICT[j.id]=j.name+j.id[-2:]
        else:
            METDICT[j.id]=j.id


def reaction_comparer(het,ug):
    return_set=[]
    if len(het.metabolites) == len(ug.metabolites) and het.reversibility==ug.reversibility:
        for h in het.metabolites:
            for u in ug.metabolites:
                if METDICT[h.id]==u.id:
                    if het.metabolites[h] == ug.metabolites[u]:
                        return_set.append(u)
                elif (h.id=='nad_c' and u.id=='nadp_c') or (h.id=='nadp_c' and u.id=='nad_c') or (h.id=='nadh_c' and u.id=='nadph_c') or (h.id == 'nadph_c' and u.id=='nadh_c'):
                    if het.metabolites[h] == ug.metabolites[u]:
                        return_set.append(u)
    if len(het.metabolites)==len(return_set):
        return True
    else:
        return False


result=[]
for het in heterologous_reactions:
    for ug in underground_reactions:
        r=reaction_comparer(het,ug)
        if r:
            result.append([het,ug])


def is_blocked(reaction):
    if reaction.id.find('u0')>-1:
        if reaction.id in ug_u0:
            return True
        else:
            return False
    elif reaction.id.find('MetaCyc')>-1:
        if reaction.id in het_MetaCyc:
            return True
        else:
            return False

def reaction_writer(reaction,is_het):
    return_string=""
    for m in reaction.reactants:
        if is_het:
            return_string=return_string+str(reaction.metabolites[m])+METDICT[m.id]+' +'
        else:
            return_string=return_string+str(reaction.metabolites[m])+m.id+' +'
    if reaction.reversibility:
        return_string=return_string[:-1]+' <=> '
    else:
        return_string=return_string[:-1]+' -> '
    for p in reaction.products:
        if is_het:
            return_string=return_string+str(reaction.metabolites[p])+METDICT[p.id]+' +'
        else:
            return_string=return_string+str(reaction.metabolites[p])+p.id+' +'
    return return_string[:-1]


for r in result:
    print(r[0].id,'\t',is_blocked(r[0]),'\t',r[1].id,'\t',is_blocked(r[1]),'\t',reaction_writer(r[0],True),'\t',reaction_writer(r[1],False))
#print(len(result))
