#!usr/bin/env python3.6

import glob
import re

def get_file_data(filename):
	f = open(filename, "r")
	lines = []
	for line in f:
		lines.append(line.rstrip("\n"))

	f.close
	return(lines)

###########################
#extract_branch_lengths.py#
###########################

#This will produce a file of tab seperated values, with a header line. The columns are duplication freqs, transfer freqs, origination freqs, loss_freqs. The rows are your branch ids as in ale
#Make sure all the ale output files are in one directory, within your current directory, which the program will ask you to specify


#Here I have included the identifiers for the branches used in my analyses
#You should replace these with the identifiers found in your ale output (the .uml_rec one), in the order they appear in the table at the bottom of said file
#It doesn't matter if there are more or less than I have
#Do this for all the dictionaries (the long bois laid out bellow.)

duplication_freqs = {"Anolis" : 0,
"Branchiostoma" : 0,
"Callorhinchus" : 0,
"Carassius" : 0,
"Ciona" : 0,
"Danio" : 0,
"Gallus" : 0,
"Homo" : 0,
"Latimeria" : 0,
"Lepisosteus" : 0,
"Ornithorhynchus" : 0,
"Petromyzon" : 0,
"Saccoglossus" : 0,
"Strongylocentrotus" : 0,
"Taeniopygia" : 0,
"Xenopus" : 0,
"16" : 0,
"17" : 0,
"18" : 0,
"19" : 0,
"20" : 0,
"21" : 0,
"22" : 0,
"23" : 0,
"24" : 0,
"25" : 0,
"26" : 0,
"27" : 0,
"28" : 0,
"29" : 0,
"30" : 0}

transfer_freqs = duplication_freqs.copy()
origination_freqs = duplication_freqs.copy()
loss_freqs = duplication_freqs.copy() 

directory = input("which directory are the ale output files in?\n")
filename = input("what do you want the output table to be called?\n")
treefile = input("what do you want the treefile to be called?\n")

path = str(directory + "/")
files = glob.glob(str(path + "/*.uml_rec"))
for file in files:
	lines = get_file_data(file)
	for key in duplication_freqs.keys():
		for line in lines:
			pattern1 = "S_terminal_branch\s+" + key
			pattern2 = "S_internal_branch\s+" + key
			if re.search(pattern1, str(line)) or re.search(pattern2, str(line)):
				fields = line.split("\t")
				duplication_freqs[key] = duplication_freqs[key] + float(fields[2])
				transfer_freqs[key] = transfer_freqs[key] + float(fields[3])
				loss_freqs[key] = loss_freqs[key] + float(fields[4])
				origination_freqs[key] = origination_freqs[key] + float(fields[5])

f = open(filename, "w")
f.write("branch\tduplciations\ttransfers\tlosses\toriginations")
for key in duplication_freqs.keys():
	f.write("\n" + key + "\t" + str(duplication_freqs[key]) + "\t" + str(transfer_freqs[key]) + "\t" + str(loss_freqs[key]) + "\t" + str(origination_freqs[key]))
f.close()

out = open(treefile, "w")
ordered_list = ["30", "29", "28", "27", "26", "25", "24", "23", "22", "21", "20", "19", "18", "17", "16",
                "Anolis", "Branchiostoma", "Callorhinchus", "Carassius", "Ciona", "Danio", "Gallus",
                "Homo", "Latimeria", "Lepisosteus", "Ornithorhynchus", "Petromyzon", "Saccoglossus",
                "Strongylocentrotus", "Taeniopygia", "Xenopus"]
tree = "((((((((((Homo:1,Ornithorhynchus:1)18:1,((Taeniopygia:1,Gallus:1)17:1,Anolis:1)21:1)22:1,Xenopus:1)23:1,Latimeria:1)24:1,((Carassius:1,Danio:1)16:1,Lepisosteus:1)19:1)25:1,Callorhinchus:1)26:1,Petromyzon:1)27:1,Ciona:1)28:1,Branchiostoma:1)29:1,(Saccoglossus:1,Strongylocentrotus:1)20:1)30;"
for key in ordered_list:
    pattern = re.compile("([^.]" + key + ")")
    tree = re.sub(pattern, r'\1_D=' + str(duplication_freqs[key]), tree)
    tree = re.sub(pattern, r'\1_L=' + str(loss_freqs[key]), tree)
out.write(tree)
out.close()



exit()
