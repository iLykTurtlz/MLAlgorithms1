import exemple # Pour pouvoir utiliser les methodes de exemple.py
from exemple import *
import copy
import random
import time
import matplotlib.pyplot as plt

def lirePreferencesEtuSurSpe(nomFichier: str) -> list[list[int]]:
	lignes = lectureFichier(nomFichier)
	pref = []
	for i in range(1,len(lignes)):
		'''
		l=[]
		for j in range(2,len(lignes[i])):
			l.append(int(lignes[i][j]))
		'''
		l = [int(lignes[i][j]) for j in range(2,len(lignes[i]))]	#version liste compréhension
		pref.append(l)

	return pref

def lirePreferencesSpeSurEtu(nomFichier: str) -> tuple[list[list[int]],list[int]]:
	lignes = lectureFichier(nomFichier)
	pref = []
	cap = [int(x) for x in lignes[1][1:]]
	
	for i in range(2,len(lignes)):
		'''
		l=[]
		for j in range(2,len(lignes[i])):
			l.append(int(lignes[i][j]))
		'''
		l = [int(lignes[i][j]) for j in range(2,len(lignes[i]))]	#version liste compréhension
		pref.append(l)

	return cap,pref
	

def GaleShapleyCoteEtu(lPrefEtu: list[list[int]], capacites: list[int], lPrefSpe: list[list[int]]) -> list[tuple[int,int]]:
	'''
	en entrée :	la matrice lPrefEtu[i,j] des préférences j pour chaque étudiant i
				la liste d'entiers des capacités de chaque parcours
				la matrice lPrefSpe[i,j] des préférences j pour chaque parcours i
	en sortie :	un mariage parfait étudiant optimal M contenant des couples (étudiant, parcours)
	'''
	#initialisation
	prochaineProposition = [0 for i in range(len(lPrefEtu))]#indices des prochaines specialites auxquelles l'étudiant i n'a pas encore fait de proposition
	etusLibres = [i for i in range(len(lPrefEtu))]			#étudiants pas encore affectés (chacun d'un unique indice i dans [0,n-1])
	cap = copy.deepcopy(capacites)							#liste de places libre.  Il faut deepcopy pour que la liste en entrée ne soit pas modifiée
	M = []													#Mariage vide

	while len(etusLibres) > 0:
		e = etusLibres.pop()						#étudiant libre
		p = lPrefEtu[e][prochaineProposition[e]] 	#le parcours en question
		if (cap[p] > 0):							#si il y a une place libre dans ce parcours, affectation
			M.append((e,p))
			cap[p] -= 1
		else:							
			dejaAffectes = [etu for (etu,spe) in M if spe==p]		#liste d'étudiants déjà affectés à ce parcours
			permutation = False
			for etu in dejaAffectes:
				if lPrefSpe[p].index(e) < lPrefSpe[p].index(etu):	#si le parcours préfère e à un étudiant déjà affecté, permutation
					M.remove((etu,p))
					etusLibres.append(etu)
					M.append((e,p))
					permutation = True
					break
			if not permutation:			
				etusLibres.append(e)	#il faut remettre l'étudiant rejeté dans la liste
		prochaineProposition[e] += 1

	return M



def GaleShapleyCoteSpe(lPrefEtu: list[list[int]], capacites: list[int], lPrefSpe: list[list[int]]) -> list[tuple[int,int]]:	
	'''
	en entrée :	la matrice lPrefEtu[i,j] des préférences j pour chaque étudiant i
				la liste d'entiers des capacités de chaque parcours
				la matrice lPrefSpe[i,j] des préférences j pour chaque parcours i
	en sortie :	un mariage parfait parcours optimal M contenant des tuples (étudiant, parcours)   ...même ordre dans les tuples pour faciliter la comparaison des mariages plus tard
	'''
	#initialisation
	prochaineProposition = [0 for i in range(len(lPrefSpe))]#indices des prochains étudiants auxquels le parcours i n'a pas encore fait de proposition
	etusLibres = [i for i in range(len(lPrefEtu))]			#étudiants pas encore affectés (chacun d'un unique indice i dans [0,n-1])
	cap = copy.deepcopy(capacites)							#ainsi, aucune des trois listes ne sera modifiée
	M = []													#Mariage vide

	while any(cap):												#tant qu'il reste un parcours dont la capacité est non nulle
		p = cap.index(next(filter(lambda x : x>0, cap)))		#parcours avec au moins une place dispo
		e = lPrefSpe[p][prochaineProposition[p]]				#le prochain étudiant à recevoir une proposition
		if e in etusLibres:
			etusLibres.remove(e)
			M.append((e,p))
			cap[p] -= 1
		else:
			pCourant = next(filter(lambda paire : paire[0]==e, M))[1] #le parcours auquel l'étudiant e a déjà été affecté
			if lPrefEtu[e].index(p) < lPrefEtu[e].index(pCourant):
				M.remove((e,pCourant))
				cap[pCourant] += 1
				M.append((e,p))
				cap[p] -= 1
		prochaineProposition[p] += 1	

	return M

def pairesInstables(M: list[tuple[int,int]], lPrefEtu: list[list[int]], lPrefSpe: list[list[int]]) -> list[tuple[int,int]]:
	'''
	en entrée :	le mariage M représenté par des couples (étudiant, parcours)
				la matrice lPrefEtu[i,j] des préférences j pour chaque étudiant i
				la matrice lPrefSpe[i,j] des préférences j pour chaque parcours i
	en sortie :	une liste de paires instables représentée par des couples (étudiant, parcours)
	'''

	'''
	#version sans compréhension des listes
	paires = []
	for e1,p1 in M:
		for e2,p2 in M:
			if lPrefEtu[e1].index(p2) < lPrefEtu[e1].index(p1) and lPrefSpe[p2].index(e1) < lPrefSpe[p2].index(e2):
				paires.append((e1,p2))
	return paires
	'''
	#version avec compréhension des listes
	return [(e1,p2) for e1,p1 in M for e2,p2 in M if lPrefEtu[e1].index(p2) < lPrefEtu[e1].index(p1) and lPrefSpe[p2].index(e1) < lPrefSpe[p2].index(e2)]


def genererPref(n: int) -> tuple[list[list[int]], list[int], list[list[int]]]:
	'''
	en entrée:	le nombre d'étudiants n
				(le nombre de parcours est constante: 9)
	en sortie:	
				la matrice lPrefEtu[i,j] des préférences j pour chaque étudiant i
				la liste d'entiers des capacités de chacun des 9 parcours, générés de façon détérministe et plus ou moins égaux entre les parcours
				la matrice lPrefSpe[i,j] des préférences j pour chaque parcours i
	'''
	
	lPrefEtu=[]
	for i in range(n):
		prefEtu = [i for i in range(9)]
		random.shuffle(prefEtu)
		lPrefEtu.append(prefEtu)

	lPrefSpe=[]
	for i in range(9):
		prefSpe = [i for i in range(n)]
		random.shuffle(prefSpe)
		lPrefSpe.append(prefSpe)
	#la somme des capacites est de n du faite que le reste est rajoyte a la fins
	cap = [n//9 for i in range(9)]
	reste = n % 9 
	for i in range(reste):
		cap[i] += 1
	return lPrefEtu, cap, lPrefSpe



def temps_execution_gs_cote_etu(binf, bsup , step) :
	temps = []
	for i in range(binf , bsup, step):
		
		lpe,c,lps = genererPref(i)
		tps1 = time.process_time()
		GaleShapleyCoteEtu(lpe,c,lps)
		tps2 = time.process_time()
		temps.append(tps2-tps1)
	return temps

def temps_execution_gs_cote_spe(binf, bsup , step) :
	temps = []
	for i in range(binf , bsup, step):
		
		lpe,c,lps = genererPref(i)
		tps1 = time.process_time()
		GaleShapleyCoteSpe(lpe,c,lps)
		tps2 = time.process_time()
		temps.append(tps2-tps1)
	return temps

def nb_iter_gs_cote_etu(r):
	nb_iter = []
	for i in r:
		#GaleShapleyCoteEtu_nbIter(genererPref[i])[1] represente it retourné par la fonction GS
		M,it = GaleShapleyCoteEtu_nbIter(genererPref(i))
		nb_iter.append(it)
	return nb_iter

def nb_iter_gs_cote_spe(r):
	nb_iter = []
	for i in r:
		#GaleShapleyCoteEtu_nbIter(genererPref[i])[1] represente it retourné par la fonction GS
		M,it = GaleShapleyCoteSpe_nbIter(genererPref(i))
		nb_iter.append(it)
	return nb_iter




def GaleShapleyCoteEtu_nbIter(lPrefEtu: list[list[int]], capacites: list[int], lPrefSpe: list[list[int]]) -> list[tuple[int,int]]:
	'''
	en entrée :	la matrice lPrefEtu[i,j] des préférences j pour chaque étudiant i
				la liste d'entiers des capacités de chaque parcours
				la matrice lPrefSpe[i,j] des préférences j pour chaque parcours i
	en sortie :	un mariage parfait étudiant optimal M contenant des couples (étudiant, parcours)
	'''
	#initialisation
	prochaineProposition = [0 for i in range(len(lPrefEtu))]#indices des prochaines specialites auxquelles l'étudiant i n'a pas encore fait de proposition
	etusLibres = [i for i in range(len(lPrefEtu))]			#étudiants pas encore affectés (chacun d'un unique indice i dans [0,n-1])
	cap = copy.deepcopy(capacites)							#liste de places libre.  Il faut deepcopy pour que la liste en entrée ne soit pas modifiée
	M = []													#Mariage vide

	it = 0
	while len(etusLibres) > 0:
		e = etusLibres.pop()						#étudiant libre
		p = lPrefEtu[e][prochaineProposition[e]] 	#le parcours en question
		if (cap[p] > 0):							#si il y a une place libre dans ce parcours, affectation
			M.append((e,p))
			cap[p] -= 1
		else:							
			dejaAffectes = [etu for (etu,spe) in M if spe==p]		#liste d'étudiants déjà affectés à ce parcours
			permutation = False
			for etu in dejaAffectes:
				if lPrefSpe[p].index(e) < lPrefSpe[p].index(etu):	#si le parcours préfère e à un étudiant déjà affecté, permutation
					M.remove((etu,p))
					etusLibres.append(etu)
					M.append((e,p))
					permutation = True
					break
			if not permutation:			
				etusLibres.append(e)	#il faut remettre l'étudiant rejeté dans la liste
		prochaineProposition[e] += 1
		it += 1

	return M, it



def GaleShapleyCoteSpe_nbIter(lPrefEtu: list[list[int]], capacites: list[int], lPrefSpe: list[list[int]]) -> list[tuple[int,int]]:	
	'''
	en entrée :	la matrice lPrefEtu[i,j] des préférences j pour chaque étudiant i
				la liste d'entiers des capacités de chaque parcours
				la matrice lPrefSpe[i,j] des préférences j pour chaque parcours i
	en sortie :	un mariage parfait parcours optimal M contenant des tuples (étudiant, parcours)   ...même ordre dans les tuples pour faciliter la comparaison des mariages plus tard
	'''
	#initialisation
	prochaineProposition = [0 for i in range(len(lPrefSpe))]#indices des prochains étudiants auxquels le parcours i n'a pas encore fait de proposition
	etusLibres = [i for i in range(len(lPrefEtu))]			#étudiants pas encore affectés (chacun d'un unique indice i dans [0,n-1])
	cap = copy.deepcopy(capacites)							#ainsi, aucune des trois listes ne sera modifiée
	M = []													#Mariage vide

	it = 0
	while any(cap):												#tant qu'il reste un parcours dont la capacité est non nulle
		p = cap.index(next(filter(lambda x : x>0, cap)))		#parcours avec au moins une place dispo
		e = lPrefSpe[p][prochaineProposition[p]]				#le prochain étudiant à recevoir une proposition
		if e in etusLibres:
			etusLibres.remove(e)
			M.append((e,p))
			cap[p] -= 1
		else:
			pCourant = next(filter(lambda paire : paire[0]==e, M))[1] #le parcours auquel l'étudiant e a déjà été affecté
			if lPrefEtu[e].index(p) < lPrefEtu[e].index(pCourant):
				M.remove((e,pCourant))
				cap[pCourant] += 1
				M.append((e,p))
				cap[p] -= 1
		prochaineProposition[p] += 1	
		it += 1

	return M, it


def tracer2courbes(x: list[int], y1: list[float], y1Label:str, y2: list[float], y2Label:str, ylabel:str):
	
	plt.title("Comparaison des temps d'exécution de GS coté étudiant, coté spécialité")
	plt.plot(x,y1,color='green', label=y1Label)
	plt.plot(x,y2,color='blue', label=y2Label)
	plt.xlabel('n')
	plt.ylabel(ylabel)
	plt.legend()
	plt.show()


	

'''
print("bonjour")
maListe=exemple.lectureFichier("test.txt") # Execution de la methode lectureFichier du fichier exemple.
print(maListe)
exemple.createFichierLP(maListe[0][0],int(maListe[1][0])) #Methode int(): transforme la chaine de caracteres en entier
'''

def main():
#Q1
	etuSurSpe = lirePreferencesEtuSurSpe("PrefEtu.txt")
	cap, speSurEtu = lirePreferencesSpeSurEtu("PrefSpe.txt")	#couple (liste des capacités, matrice des préférences)

	print('etuSurSpe:')
	print(etuSurSpe)
	print()
	print('cap')
	print(cap)
	print()
	print('speSurEtu:')
	print(speSurEtu)
	print()
	assert(len(cap) == len(speSurEtu))	

#Q2
	MEtuOpt = GaleShapleyCoteEtu(etuSurSpe, cap, speSurEtu)
	print("Mariage parfait côté étudiant : couples de (étudiant, parcours)")
	print(MEtuOpt)	
	print()

#Q3
	MSpeOpt = GaleShapleyCoteSpe(etuSurSpe, cap, speSurEtu)
	print("Mariage parfait côté parcours : couples de (étudiant, parcours)")
	print(MSpeOpt)
	print()

#Q4
	instablesMEtuOpt = pairesInstables(MEtuOpt, etuSurSpe, speSurEtu)
	print("Paires instables du mariage parfait côté étudiant")
	print(instablesMEtuOpt)
	print()

	instablesMSpeOpt = pairesInstables(MSpeOpt, etuSurSpe, speSurEtu)
	print("Paires instables du mariage parfait côté parcours")
	print(instablesMSpeOpt)
	print()

#Q5
	#cf genererPref qui fait le tout

#Q6
	#lpe,c,lps = genererPref(107)
	#print(lpe)
	#print(c)
	#print(lps)
	abscisse = range(200,3000,100)
	#temps_cote_etu = temps_execution_gs_cote_etu(200,3000,100)
	#temps_cote_spe = temps_execution_gs_cote_spe(200,3000,100)
	#tracer2courbes(abscisse, temps_cote_etu, "côté étudiant",temps_cote_spe, "côté spécialisation", "temps (s)")
#Q6

#Q7

#Q8

	it_cote_etu = nb_iter_gs_cote_etu(abscisse)
	it_cote_spe = nb_iter_gs_cote_spe(abscisse)
	tracer2courbes(list(abscisse), it_cote_etu, "côté étudiant", it_cote_spe, "côté spécialisation", "nombre d'itérations")

if __name__ == "__main__":
	main()


