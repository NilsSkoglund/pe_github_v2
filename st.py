################################# Imports #####################################
import streamlit as st

################################ Functions ####################################

def calc_score(dct, name):
	'''
	Calculate total score
	'''
	total_score = 0
	for index, question in enumerate(dct):
		key = f"{name}{index}"
		if st.session_state[key]: # if True means the checkbox is ticked
			total_score += dct.get(question)
	return total_score

def display(name, total_score, green, yellow):
	'''
	Display green/yellow/red status bar 
	'''
	if total_score < green:
		return st.success(f"{name} total poäng: {total_score} | Låg risk")
	elif total_score < yellow:
		return st.warning(f"{name} total poäng: {total_score} | Måttlig risk")
	else: 
		return st.error(f"{name} total poäng: {total_score} | Hög risk")

def initialize_keys(dct, name):
	'''
	Initializing 'keys' 
	Check if 'key' already exists in session_state
	If not, then initialize it as 'False'
	'''
	for index in enumerate(dct):
		key = f"{name}{index}"
		if key not in st.session_state:
			st.session_state[key] = False
	return None

def update_pe():
	st.session_state["total_score_dvt"] =\
		calc_score(wells_dvt_dct, wells_dvt_name)
	if st.session_state["total_score_dvt"] > 0:
		st.session_state["wells_pe0"] = True
	else:
		st.session_state["wells_pe0"] = False
	return None
		

def create_checkboxes(dct, name):
	'''
	Generate checkboxes
	'''
	if name == wells_dvt_name:
		for index, question in enumerate(dct.items()):
			st.checkbox(
				label=f"{question[0]} ({question[1]})", 
				key=f"{name}{index}",
				on_change=update_pe
				)
	else:
		for index, question in enumerate(dct.items()):
			if index == 0:
				st.checkbox(
				label=f"{question[0]} ({question[1]})", 
				key=f"{name}{index}",
				help="Uppdateras baserat på input till DVT-formuläret"
				)
			else:
				st.checkbox(
					label=f"{question[0]} ({question[1]})", 
					key=f"{name}{index}"
					)
	return None


def change_pe_in_to_out():
	if st.session_state["pe_mark_inside"]: 
		st.session_state["pe_mark_outside"] = True
	else:
		st.session_state["pe_mark_outside"] = False
	
def change_pe_out_to_in():
	if st.session_state["pe_mark_outside"]: 
		st.session_state["pe_mark_inside"] = True
	else:
		st.session_state["pe_mark_inside"] = False
	

############################### Variables #####################################

# Initialize variables for Wells' Criteria for PE
	# dct with question:score
	# name for key
wells_pe_dct={
	"Symtom DVT":3,
	"PE är mest sannolika diagnos":3,
	"Puls över 100":1.5,
	"Immobiliserad i 3 dagar ALTERNATIVT opererad senaste 4 veckor":1.5,
	"Tidigare PE eller DVT diagnos":1.5,
	"Hemoptysis":1,
	"Sista kriteriet som va jobbigt att översätta":1
	}

wells_pe_name = "wells_pe"

# Initialize variables for Wells' Criteria for DVT
	# dct with question:score
	# name for key
wells_dvt_dct={
	"Aktiv cancer":1,
	"Sängliggande senaste 3 dagar ALTERNATIVT större operation senaste 12 veckor":1,
	"Svullen vad (över 3cm) jämfört med andra benet":1,
	"Collateral (nonvaricose) superficial veins present":1,
	"Helt ben svullet":1,
	"Localized tenderness along the deep venous system":1,
	"Pitting edema, confined to symptomatic leg":1,
	"Paralysis, paresis, or recent plaster immobilization of the lower extremity":1,
	"Previously documented DVT":1, 
	"Alternative diagnosis to DVT as likely or more likely":-2
	}
wells_dvt_name = "wells_dvt"

# Initialize variables for PERC Rule for PE
	# dct with question:score
	# name for key
perc_dct={
	"Ålder ≥50":1,
	"Puls över 100":1,
	"Svullen vad (över 3cm) jämfört med andra benet":1,
	"Collateral (nonvaricose) superficial veins present":1,
	"Helt ben svullet":1,
	"Localized tenderness along the deep venous system":1,
	"Pitting edema, confined to symptomatic leg":1,
	"Paralysis, paresis, or recent plaster immobilization of the lower extremity":1,
	"Previously documented DVT":1, 
	"Alternative diagnosis to DVT as likely or more likely":-2
	}
perc_name = "perc"

# Initialize session variable for total score for Wells' PE & DVT form
if "total_score_pe" not in st.session_state:
	st.session_state["total_score_pe"] = 0

if "total_score_dvt" not in st.session_state:
	st.session_state["total_score_dvt"] = 0

# Initialize ...
if "pe_mark_inside" not in st.session_state:
	st.session_state["pe_mark_inside"] = False

if "pe_mark_outside" not in st.session_state:
	st.session_state["pe_mark_outside"] = False

############################## PROGRAM & UI ###################################

# overview
st.subheader("Utförda steg")
col1, col2, col3, col4 = st.columns(4)
with col1:
	st.checkbox("Wells' DVT")
with col2:
	st.checkbox("Wells' PE",\
		key="pe_mark_outside",\
		on_change=change_pe_out_to_in)
with col3:
	st.checkbox("PERC")
with col4:
	st.checkbox("D-Dimer")


st.subheader("Formulär")

# wells' dvt
with st.expander("Wells' Criteria for DVT", expanded=False):
	st.header("\n\nWells' Criteria for DVT")
	st.info("Notera! Sista frågan ger -2 poäng")
	initialize_keys(wells_dvt_dct, wells_dvt_name)
	create_checkboxes(wells_dvt_dct, wells_dvt_name)
	st.session_state["total_score_dvt"] = calc_score(wells_dvt_dct, wells_dvt_name)
	st.write(st.session_state["total_score_dvt"])
	display("Wells' DVT", st.session_state["total_score_dvt"], 1, 3)

# wells' pe
with st.expander("Wells' Criteria for PE"):
	st.header("Wells' Criteria for PE")
	initialize_keys(wells_pe_dct, wells_pe_name)
	create_checkboxes(wells_pe_dct, wells_pe_name)
	st.write("")
	st.session_state["total_score_pe"] = calc_score(wells_pe_dct, wells_pe_name)
	#display("Wells' PE", st.session_state["total_score_pe"], 2, 4)
	#st.write(f"Poäng: {st.session_state['total_score_pe']} av 12.5")
	st.metric("Poäng:", f"{st.session_state['total_score_pe']} av 12.5")
	col1, col2, col3 = st.columns([3,1,3])
	with col2:
		st.checkbox("Klar", key = "pe_mark_inside", on_change=change_pe_in_to_out)
	
	
	

st.subheader("Resultat")
with st.expander("Visa resultat"):
	display("Wells' PE", st.session_state["total_score_pe"], 2, 4)
	display("Wells' DVT", st.session_state["total_score_dvt"], 1, 3)


