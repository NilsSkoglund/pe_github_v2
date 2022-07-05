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

def display(total_score, green, yellow):
	'''
	Display green/yellow/red status bar 
	'''
	if total_score < green:
		return st.success("")
	elif total_score < yellow:
		return st.warning("")
	else: 
		return st.error("")

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

def create_checkboxes(dct, name):
	'''
	Generate checkboxes
	'''
	for index, question in enumerate(dct.items()):
		st.checkbox(
			label=f"{question[0]} ({question[1]})", 
			key=f"{name}{index}"
			)
	return None


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

################################# PROGRAM #####################################

# wells' pe
with st.expander("Wells' Criteria for PE"):
	st.header("Wells' Criteria for PE")
	initialize_keys(wells_pe_dct, wells_pe_name)
	create_checkboxes(wells_pe_dct, wells_pe_name)
	total_score_pe = calc_score(wells_pe_dct, wells_pe_name)
	st.write(total_score_pe)
	display(total_score_pe, 2, 4)

# wells' dvt
with st.expander("Wells' Criteria for DVT"):
	st.header("Wells' Criteria for DVT")
	st.info("Note: You get -2 points for Q10")
	initialize_keys(wells_dvt_dct, wells_dvt_name)
	create_checkboxes(wells_dvt_dct, wells_dvt_name)
	total_score_dvt = calc_score(wells_dvt_dct, wells_dvt_name)
	st.write(total_score_dvt)
	display(total_score_dvt, 1, 3)