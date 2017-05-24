#script (python) 

import datetime
import string

from gringo import *

debug = False 
planning = False 
checked = False 
nmax = 1000
heuristic = False
initials_only = False
eiter = False
brave_cautious = False
goal_directed = False

sModels = []               #list of guesses (models)
_sModels = []
braveModel = [] 
cautiousModel = []
_braveModel = [] 
_cautiousModel = []
_braveCheckModel = []
cntWv = 0
badGuesses = []
nModels = 0
#for eiter's semantics
_k0_m1_set = []


inits = [] ## list of initial states
sol_heuristics = [] ## list of solutions, one corresponds to one initial
strHeuristic = ""

def check_brave(m):
   result = [x for x in m.atoms(Model.ATOMS)]
   if debug == True: print result
   _braveCheckModel.append(result) 

def set_brave(m):
   result = [x for x in m.atoms(Model.ATOMS)]
   _braveModel.append(result)

def set_cautious(m):
   result = [x for x in m.atoms(Model.ATOMS)]
   _cautiousModel.append(result)
       
def get_setat(m, prefs):
   atset = []  
   for x in m.atoms(Model.ATOMS): 
      if x.name().find(prefs, 0, 2) == 0:          
         atset.append(x) 
   if debug == True: print atset      
   return atset 

def get_setat_from_string(strList, prefs):
    atset = []
    for x in strList:
        if x.find(prefs, 0, 2) == 0:
            atset.append(x)
    if debug == True: print atset
    return atset

def print_wv(m):

   global  cntWv 

   if debug == True : print m 
   atset = []  
   cntWv = cntWv + 1
   for x in m.atoms(Model.ATOMS): 
      xname = str(x)  
      if  xname.find('k1_', 0, 3) == 0 :  True   
      elif xname.find('k0_', 0, 3) == 0 : True   
      elif xname.find('m1_', 0, 3) == 0: True   
      elif xname.find('m0_', 0, 3) == 0:  True           
      elif xname.find('-k0_', 0, 4) == 0:  True           
      elif xname.find('-k_', 0, 3) == 0:  True           
      else:  atset.append(x)
   
   if debug == True or planning != True:
      print "Belief set of world view:  ",  cntWv, '\n', atset, "\n"
   else:
      print "Belief set of world view:  ",  cntWv, '\n'
#if debug == True : print atset, "\n"
   return 
   
def check_bad(m):
   if debug==True: print "First pass bad ", m
   result = get_setat(m, "bad") 
   badGuesses.append(result) 
   return 
      
    
def collect(m): 
   if debug == True: print "In collecting ..",   m
   answer1 = get_setat(m, "m0")
   answer1 = answer1 + get_setat(m, "k1")
   answer2 = get_setat(m, "m1")
   answer2 = answer2 + get_setat(m, "k0")
   sModels.append(answer1)
   sModels.append(answer2)

def collect_eiter(m):
    global _sModels
    if debug == True: print "In collecting model for eiter's semantics.."
    stable_model = result = [str(x) for x in m.atoms(Model.ATOMS)]
    k0_m1_set = get_setat(m, "m1")
    k0_m1_set = k0_m1_set + get_setat(m, "k0")
    _sModels = [] #reset _sModels to empty set
    _sModels.append(stable_model) #the first set in _sModels is the stable model
    _sModels.append(k0_m1_set) #the second set in _sModels is all k0_, m1_ atoms in the stable model


def getLiteral(atom): 
    kname = str(atom)
    if kname.find('k1_0', 0, 4) == 0: return 'not -'+ kname[4:]
    if kname.find('k0_0', 0, 4) == 0: return 'not -'+ kname[4:]
    if kname.find('k1_', 0, 3) == 0: return 'not '+ kname[3:]
    if kname.find('k0_', 0, 3) == 0: return 'not '+  kname[3:]
    if kname.find('m1_0', 0, 4) == 0: return ' -'+kname[4:]
    if kname.find('m0_0', 0, 4) == 0: return '-'+kname[4:]
    if kname.find('m1_', 0, 3) == 0: return  kname[3:]
    if kname.find('m0_', 0, 3) == 0: return kname[3:]
            
def check_k1_m0(prg, cur_model ):
     wv_chek1 = ''
     count_1 = 0

     if debug == True : print "***** Checking for first condition (k1_ and m0_) ********"
     
     model1 = sModels[cur_model]
     if len(model1) == 0 : 
          if debug == True : print "Nothing to be checked for first pass!"
          return False

     for i in range(0, len(model1)) :
          atom = getLiteral(model1[i])
          wv_chek1 = wv_chek1 + 'bad_'+str(cur_model)+ '(' +  str(count_1) + ') :-  ' + str(model1[i])+ ',  '+atom+ ',  _check1(' + str(cur_model) +').\n '
          count_1 = count_1 + 1 
           
     for i in range(0, count_1) :
          wv_chek1 = wv_chek1 + 'nok_'+str(cur_model)+ ' :- bad_'+str(cur_model)+ '('+str(i)+')' + ',  _check1(' + str(cur_model) +').\n ' 
     
     wv_chek1 = wv_chek1 + ' :- not nok_'+str(cur_model)+ ',  _check1(' + str(cur_model) +').\n '
     if debug == True: print "Check for first condition  \n ", wv_chek1  
     prg.assign_external(Fun("_check1", [cur_model]), True)

     m_name = "check1("+  str(cur_model)   +")"    
     prg.add(m_name, [], wv_chek1)
     prg.ground([(m_name, [])])
     
     retValidity = prg.solve(None, on_model = check_bad)
     if retValidity ==  SolveResult.SAT: 
          if debug == True : print 'First check does not pass!', cur_model
          
          retVal = True
     else:      
          if debug == True : print 'Passed first check ===================!', cur_model
          retVal = False

     prg.assign_external(Fun("_check1", [cur_model]), False)
     
     return retVal

def check_k0_m1(prg, cur_model ):

     global  cntWv 

     wv_chek2 = ''
     count_2 = 0
     model2 = sModels[cur_model+1]

     if debug == True : print "***** Checking for second condition (k0_ and m1_) ********"

     if len(model2) == 0: 
          if debug == True : print "Nothing to be checked for second pass!"
          return False
     
     for i in range(0, len(model2)) :
          atom = getLiteral(model2[i])
          wv_chek2 = wv_chek2 + 'ok_'+str(cur_model)+ '(' +  str(count_2) + ') :-  ' + str(model2[i])+ ',  '+atom+ ',  _check2(' + str(cur_model) +').\n '
          count_2 = count_2 + 1 
     
     # for i in range(0, count_2) :      
     #     wv_chek2 = wv_chek2 + 'n2ok_'+str(cur_model)+ ' :- not ok_'+str(cur_model)+ '(' + str(i) +')' + ',  _check2(' + str(cur_model) +').\n ' 
     # wv_chek2 = wv_chek2 + ' :- not n2ok_'+str(cur_model)+ ',  _check2(' + str(cur_model) +').\n '
     
     if debug == True: print "Check for second condition  \n ", wv_chek2  
       
     prg.assign_external(Fun("_check2", [cur_model]), True)

     m_name = "check2("+  str(cur_model)   +")"    
     prg.add(m_name, [], wv_chek2)
     prg.ground([(m_name, [])])

     prg.conf.solve.enum_mode = "brave"
     prg.conf.solve.models = 0
     
     retValidity = prg.solve(None, on_model = check_brave)
    
     if debug == True : print _braveCheckModel[::-1][0]
     
     valueCheck = [str(x) for x in _braveCheckModel[::-1][0]]  
     
     if debug == True : 
          print "************\n",valueCheck,"\n****************\n"  
     
     prg.conf.solve.enum_mode = "auto"

     prg.assign_external(Fun("_check2", [cur_model]), False)
 
     retVal = False 
     
     for i in range(0, count_2) :      
          need =  str('ok_'+str(cur_model)+ '(' + str(i) +')')  
          if debug == True : print need 
          if (need in valueCheck) == False: 
               if debug == True : print 'Second check does not pass!', cur_model
               retVal = True
               break 
          else: 
               if debug == True : 
                    print "Index >>>   ", valueCheck.index(need)   
     
     if retVal == False:
         if debug == True: print 'Passed second check ===================!', cur_model
         if debug == True or planning != True:
            prg.conf.solve.models = 0
            cntWv = 0
            prg.solve(None, on_model =  print_wv)
            prg.conf.solve.models = 1
            retVal = False
     return retVal

def  model_constraints(prg, model, cur_model) :

     str_not_model = ':- '
     m_name = str(cur_model)    
     
     for i in range(0, len(model)) :
           str_not_model =  str_not_model  + str(model[i]) 
           if i < len(model) -1 : str_not_model = str_not_model +','

     str_not_model = str_not_model +'.'

     if debug == True: print "Constraints on model    ++++\n", cur_model, str_not_model 
                 
     no_m_name = "nomodel("+ m_name +")"
     prg.add(no_m_name, [], str_not_model)
     prg.ground([(no_m_name, [])])    

     return  

def  model_requirement(prg, model, cur_model) :

     str_model = ''
     m_name = str(cur_model)    
     
     for i in range(0, len(model)) :
            str_model = str_model + ':- not ' + str(model[i])+ ',  _model(' + str(cur_model) +').\n '
            
     if debug == True: print "Model needs to contain ++++\n", str_model
     m_name = "model("+ m_name +")"    
     prg.add(m_name, [], str_model)
     prg.ground([(m_name, [])])

     return  

   
def compute_wv(prg, cur_model):  
        
     if debug == True: 
          print "****************************************"
          print sModels[cur_model], sModels[cur_model+1] 
          print "****************************************"
                    
     m_name = str(cur_model)
     prg.ground([("volatile",[cur_model])])

     model1 = sModels[cur_model]
     model2 = sModels[cur_model+1]
     model = model1 + model2
      
     model_requirement(prg, model, cur_model) 
     prg.assign_external(Fun("_model", [cur_model]), True)
     
     if planning == True:     prg.assign_external(Fun("_goal", []), False)
     
     # checking k1 and m0 
     
     retValidity = check_k1_m0(prg, cur_model)
     
     if debug == True: print "Return from check k1 & m0: ", retValidity
     
     if retValidity == False:  retValidity = check_k0_m1(prg, cur_model) 
        
     if planning == True:      prg.assign_external(Fun("_goal", []), True)
    
     prg.assign_external(Fun("_model", [cur_model]), False)
    
     model_constraints(prg, model, cur_model)
          
     return not retValidity

def is_k_or_m(atom): 
     strAtom = str(atom) 
     if (strAtom.find('k1_', 0) == 0) or  (strAtom.find('k0_', 0) == 0) or   (strAtom.find('m0_', 0) == 0) or  (strAtom.find('m1_', 0) == 0) : return True 
     return False

def set_brave_cautious(prg):
    
    prg.conf.solve.enum_mode = "brave"
    ret = prg.solve(None, on_model = set_brave)
    if ret == SolveResult.UNSAT: return ret

    prg.conf.solve.enum_mode = "cautious"
    ret = prg.solve(None, on_model = set_cautious)
    if ret == SolveResult.UNSAT: return ret
    
    prg.conf.solve.enum_mode = "auto"

    braveModel = [str(x) for x in _braveModel[::-1][0]]
    cautiousModel = [str(x) for x in _cautiousModel[::-1][0]]
    
    if debug == True   : 
       print 'Brave consequences: \n', braveModel  
       print 'Cautious consequences: \n', cautiousModel

    # set cautious consequence
    c_str = ''

    for lit in cautiousModel: 
          s_lit = 'k1_'+lit 
          if (s_lit in braveModel) == True: 
              c_str = c_str + ':- not '+s_lit+'. \n' #T: in cautious model and k1_lit in braveModel means it is an epistemic atom
          if is_k_or_m(lit) == True :
               c_str = c_str + ':- not '+str(lit)+'. \n'          
      
    if debug == True: print 'c_str is \n', c_str

    prg.add("constraints", [], c_str)
    prg.ground([("constraints", [])])    
        
    return ret 
    
def get(val, default):
    return val if val != None else default

def read_params(prg):
    global debug
    global planning 
    global checked 
    global nmax
    global heuristic
    global initials_only
    global eiter
    global brave_cautious
    global goal_directed

    
    debug_id    = get(prg.get_const("debug"), 0) 
    planning_id = get(prg.get_const("planning"), 0)
    checked_id = get(prg.get_const("checked"), 0)
    nmax = get(prg.get_const("nmax"), 1000)
    heuristic_id = get(prg.get_const("heuristic"),1)
    initials_only_id = get(prg.get_const("initials_only"),0)
    eiter_id = get(prg.get_const("max"),0)
    brave_cautious_id = get(prg.get_const("pre"),0)
    if planning_id != 1:
        goal_directed_id = get(prg.get_const("goal_directed"),0)
    else:
        goal_directed_id = 0
    

    if debug_id==1 : debug = True 
    if planning_id ==1 : planning = True 
    if checked_id ==1 : checked = True
    if heuristic_id == 1: heuristic = True
    if initials_only_id == 1: initials_only = True
    if eiter_id == 1: eiter = True
    if brave_cautious_id == 1: brave_cautious = True
    if goal_directed_id == 1: goal_directed = True
    
    print "Parameters: debug = ",debug, " planning = ", planning, "heuristic = ", heuristic , "initials_only = ", initials_only, " eiter = ", eiter, " brave_cautious = ", brave_cautious," goal_directed_mode = ", goal_directed," and nmax = ", nmax

def all_model(m) :
    global nModels
    nModels = nModels +1 
    return 
    
def main(prg):

    global nModels
    
    
    # read the parameters
    read_params(prg)
    
    start_time = datetime.datetime.now()

    if planning == True: #this needs to follow the planning format
        if heuristic == True:
            add_volatile_init(prg)
            compute_heuristic(prg)
            add_heuristic(prg)
        else:
            prg.ground([("initial",[])])
            prg.ground([("problem",[])])
            add_planning(prg)
            prg.ground([("planning", [])])
            prg.assign_external(Fun("_goal", []), True)
    else:
        prg.ground([("base", [])])
                   
    #print "----------DONE GROUNDING---------"

    if initials_only == True:
        end_time = datetime.datetime.now()
        elapsed = end_time - start_time
        print "Elapsed time: ", elapsed
        return
    
   
    # calculate brace and cautious consequences
    if brave_cautious == True:
        ret = set_brave_cautious(prg)
        if ret == SolveResult.UNSAT:
            print "Program unsolvable!!!"
            return
    else:
        ret = SolveResult.SAT

    #add volatile_optimizing program if computing eiter's semantics
    if eiter == 1: add_volatile_optimizing(prg)
    
    if goal_directed == 1: add_goal_directed(prg)


    #start pick an answer set and check whether it is a world view
    #add volatile program
    add_volatie(prg)

    cur_model = 0
    while ret == SolveResult.SAT:
        
        if checked == True:
              prg.conf.solve.models = 0
              prg.solve(None, on_model = all_model)
              print "No of models = ", nModels
              nModels = 0
    
        # compute a model
        if debug == True: print "----------Start Pick One Answer Set---------"
        if goal_directed == 1:
              prg.assign_external(Fun("_goal", []), True)
                  
        if eiter == 1:
              ret = compute_optimize_answerset(prg, cur_model)
        else:
              prg.conf.solve.models = 1
              ret = prg.solve(None, on_model = collect)

        if goal_directed == 1:
              prg.assign_external(Fun("_goal", []), False)

        if debug == True: print "----------Done Pick One Answer Set with Optimization---------"

        if ret == SolveResult.UNSAT:
              wv_ok = False 
              break  
         
        # check for being world view 
        # need to modify if all world views need to be computed 
        wv_ok = compute_wv(prg,  cur_model) 
        if wv_ok == True : break 

        if (cur_model > 2*nmax) and (nmax > 0): 
               print "Exceed the number of maximal guesses!" 
               break  
        # next index in list of models sModels 
        cur_model = cur_model + 2

    print "Number of guesses checked: ",  cur_model/2
    
    if debug == True:  print sModels
    
    if wv_ok :
        if planning == True:
            if debug == True: print "K & M atoms: ", sModels[cur_model], sModels[cur_model+1]
            if debug == False: print "K & M atoms: ", sModels[cur_model+1]
        else: print "K & M atoms: ", sModels[cur_model], sModels[cur_model+1]
    elif (cur_model < 2*nmax):
         print "Program has no world view!"     

    end_time = datetime.datetime.now()
    
    elapsed = end_time - start_time
    
    print "Elapsed time: ", elapsed



def set_initials(m):
    global inits
    result = []
    for x in m.atoms(Model.ATOMS):
        xname = str(x)
        if xname.find('holds(',0,6) != -1 and xname.find(',0)',len(xname)-3) != -1: result.append(x)
        if xname.find('-holds(',0,7) != -1 and xname.find(',0)',len(xname)-3) != -1: result.append(x)
        if xname.find('noholds(',0,8) != -1 and xname.find(',0)',len(xname)-3) != -1: result.append(x)
    
    if debug == True:
        print result
    inits.append(result)


def set_solutions_heuristic(m):
    global strHeuristic
    global sol_heuristics
    result = []
    for x in m.atoms(Model.ATOMS):
        xname = str(x)
        if xname.find('occurs(',0,7) != -1:
            result.append(x)
            strHeuristic = strHeuristic + ':- not 1 {m1_' + xname[:-3] + ',T) : step(T)}.\n'
            #strHeuristic = strHeuristic + ':- not 1 {' + xname[:-3] + ',T) : step(T)}.\n'
    if debug == True:
        print strHeuristic
    sol_heuristics.append(result)



def compute_heuristic(prg):
    
    
    #calculate initial states
    prg.ground([("initial",[])])
    prg.assign_external(Fun("_heuristic", []), True)
    prg.conf.solve.enum_mode= "auto"
    prg.conf.solve.models = 0
    prg.solve(None, on_model = set_initials)
    
    if debug == 1:
        print "####################################"
        print "initial states include following atoms:"
        print inits
        print "####################################"
    
    
    prg.ground([("problem",[])])
    add_planning(prg)
    prg.ground([("planning", [])])

    prg.assign_external(Fun("_goal", []), True)
    cur_init = 1
    for x in inits:
        prg.ground([("volatile_init",[cur_init])])
        prg.assign_external(Fun("_init",[cur_init]),True)
        strCons = ''
        for y in x:
            strCons = strCons + ':- _useheuristic, not ' + str(y) + ', _init(' + str(cur_init) + ').\n'
        
        if debug == 1:
            print "strCons is "
            print strCons
            print '--------------'
        strAddedProg = 'cons' + str(cur_init)
        prg.add(strAddedProg, [], strCons)
        prg.ground([(strAddedProg, [])])
        prg.conf.solve.models = 1
        prg.assign_external(Fun("_useheuristic", []), True)
        prg.solve(None, on_model = set_solutions_heuristic)
        prg.assign_external(Fun("_useheuristic", []), False)
        prg.release_external(Fun("_init",[cur_init]))
        cur_init = cur_init + 1

    prg.release_external(Fun("_heuristic", []))
    if debug == True:
        print "--------strHeuristic is: --------------"
        print strHeuristic
        print "----------------------"
    prg.conf.solve.models = 0


def add_heuristic(prg):
    global strHeuristic
    prg.add("heuristic_part",[],strHeuristic)
    prg.ground([("heuristic_part",[])])

def print_model(m):
    print "%%%%%%%%%%%%%%%%%%"
    print m
    print "%%%%%%%%%%%%%%%%%%"

def is_k0_or_m1(atom):
    strAtom = str(atom)
    if (strAtom.find('k0_', 0) == 0) or (strAtom.find('m1_', 0) == 0) : return True
    return False

def get_k0m1_atom_signatures(prg):
    signatures = []    
    for (name, arity) in prg.domains.signatures():
        if is_k0_or_m1(name):
            temp = (name, arity)
            signatures.append(temp)
    return signatures


def compute_optimize_answerset(prg, cur_model):
    global sModels
    global _k0_m1_set
    prg.conf.solve.models = 1
    ret = prg.solve(None, on_model = collect_eiter)
    if ret == SolveResult.UNSAT:
        return ret
    
    
    _k0_m1_set = get_k0m1_atom_signatures(prg)
    cnt = 0

    while ret != SolveResult.UNSAT:
        prg.ground([("volatile_optimizing",[cur_model,cnt])])
        prg.assign_external(Fun("_model_optimizing", [cur_model,cnt]), True)
        stable_model = [str(x) for x in _sModels[0]]
        k0_m1_set = [str(x) for x in _sModels[1]]

        s = set(k0_m1_set)
        not_k0_m1_set = [(x,y) for (x,y) in _k0_m1_set if x not in s]

        if debug == True:
            print "stable model is ", stable_model
            print "k0_m1_set is ", k0_m1_set
            print "not k0_m1_set is", not_k0_m1_set
        
        #compute the answer set which is optimized superset of k0_m1_set
        if not_k0_m1_set == []:
            if debug == True: print 'not_k0_m1_set is empty!!!! Then it is maximal subset!!!!!'
            answer1 = get_setat_from_string(stable_model, "m0")
            answer1 = answer1 + get_setat_from_string(stable_model, "k1")
            answer2 = get_setat_from_string(stable_model, "m1")
            answer2 = answer2 + get_setat_from_string(stable_model, "k0")
            sModels.append(answer1)
            sModels.append(answer2)
            prg.assign_external(Fun("_model_optimizing", [cur_model,cnt]), False)
            return SolveResult.SAT
        
        #checking if the current set of k0_m1_set is the optimized w.r.t maximal subset of k0_, m1_ atoms
        model_requirement_optimizing(prg,k0_m1_set,cur_model,cnt)
        add_rule_optimizing(prg, not_k0_m1_set,cur_model,cnt)

        prg.conf.solve.models = 1
        ret = prg.solve(None, on_model = collect_eiter)
        prg.assign_external(Fun("_model_optimizing", [cur_model,cnt]), False)
        if ret == SolveResult.UNSAT:
            if debug == True: print "--------->optimal stable model"
            answer1 = get_setat_from_string(stable_model, "m0")
            answer1 = answer1 + get_setat_from_string(stable_model, "k1")
            answer2 = get_setat_from_string(stable_model, "m1")
            answer2 = answer2 + get_setat_from_string(stable_model, "k0")
            sModels.append(answer1)
            sModels.append(answer2)
            return SolveResult.SAT
        cnt = cnt + 1
        if debug == True: print "---------->not optimal stable model"
    return SolveResult.SAT

def generate_abstract_atom(name,arity):
    strAtom = name
    if arity == 0:
        return strAtom
    else:
        strAtom = strAtom + '('
        for i in range(1,int(arity)+1):
            strAtom = strAtom + "Z" + str(i)
            if i != arity: strAtom = strAtom + ','
        strAtom = strAtom + ')'
        return strAtom

def model_requirement_optimizing(prg, model, cur_model,cnt) :
    str_model = ''
    m_name = str(cur_model)
    for i in range(0, len(model)) :
        str_model = str_model + ':- not ' + str(model[i])+ ',  _model_optimizing(' + str(cur_model) + ',' + str(cnt) + ').\n'
        str_model = str_model + 'before(' + str(cur_model) + ',' + str(cnt) + ',' + str(model[i])+ ') :-  _model_optimizing(' + str(cur_model) + ',' + str(cnt) +  ').\n'
    if debug == True: print "Model needs to contain ++++\n", str_model
    m_name = "model_optimizing("+ m_name +"," + str(cnt)+ ")"
    prg.add(m_name, [], str_model)
    prg.ground([(m_name, [])])
    return

def add_rule_optimizing(prg, not_k0_m1_set,cur_model,cnt):
    strRules = ''
    for (x,y) in not_k0_m1_set:
        temp = generate_abstract_atom(x,y)
        strRules = strRules + 'better(' + str(cur_model) + ',' + str(cnt) + ') :- ' + temp + ', not before(' + str(cur_model) + ','+ str(cnt) + ', '+ temp + ')' + ',  _model_optimizing(' + str(cur_model) + ',' + str(cnt) + ').\n'

    strRules = strRules + ':- not better(' + str(cur_model) + ',' + str(cnt) + ')' + ',  _model_optimizing(' + str(cur_model) + ',' + str(cnt) + ').\n'
    if debug == True: print 'strRules are: \n', strRules
    m_name = "model_optimize("+ str(cur_model) +"," + str(cnt)+ ")"
    prg.add(m_name, [], strRules)
    prg.ground([(m_name, [])])
    return

def add_volatile_optimizing(prg):
    prg.add("volatile_optimizing",["t","c"],"#external _model_optimizing(t,c).")
    return

def add_volatie(prg):
    strRules = "#external _model(t).\n"
    strRules = strRules + "#external _check1(t).\n"
    strRules = strRules + "#external _check2(t).\n"
    prg.add("volatile",["t"],strRules)
    return

def add_volatile_init(prg):
    strRules = "#external _init(t).\n"
    prg.add("volatile_init",["t"],strRules)
    return

def add_planning(prg):
    strRules = "#external _goal.\n"
    strRules = strRules + "#external _useheuristic.\n"
    strRules = strRules + ":- not goal, _goal.\n"
    strRules = strRules + "1{occurs(A,S) : action(A), executable(A,S)} 1 :- stepless(S), _goal.\n"
    prg.add("planning",[],strRules)
    return

def add_goal_directed(prg):
    strRules = "#external _goal.\n"
    strRules = strRules + ":- not goal, _goal.\n"
    prg.add("goal_directed",[],strRules)
    return

#end.






