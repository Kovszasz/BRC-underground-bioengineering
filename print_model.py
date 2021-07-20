import cobra, cobra.io, cobra.test, csv,pandas,codecs, email, smtplib,sys,random,pickle
#from cameo import load_model
from email.mime.text import MIMEText
from cobra import Reaction, Metabolite, Model
pandas.options.display.max_rows = 100
from random import randint
from cobra.util.solver import linear_reaction_coefficients
model='underground.xml'
model=cobra.io.sbml.create_cobra_model_from_sbml_file(model, False, False,False)
model.reactions.ATPM.lower_bound=3.15
BIOMASS=model.reactions.Ec_biomass_iJO1366_core_53p95M
model.reactions.EX_glc_e.lower_bound=-10

for i in model.reactions:
    if i.id.find('u0')==-1:
        print(i.id,'\t',i.reaction,'\t',i.bounds)