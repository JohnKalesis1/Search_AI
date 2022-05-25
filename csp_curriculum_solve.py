import time
import pandas as pd
import csp


def AC3(s_csp, queue=None, removals=None, arc_heuristic=csp.dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in s_csp.variables for Xk in s_csp.neighbors[Xi]}
    s_csp.support_pruning()
    queue = arc_heuristic(s_csp, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = csp.revise(s_csp, Xi, Xj, removals, checks)
        if revised:
            if not s_csp.curr_domains[Xi]:
                s_csp.wipeout=+1
                s_csp.weights[(Xi,Xk)]=+1
                s_csp.weights[(Xk,Xi)]=+1
                return False, checks  # CSP is inconsistent
            for Xk in s_csp.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable

def mac(csp, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)



def FC_dom_deg(csp, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    csp.support_pruning()
    for B in csp.neighbors[var]:
        if B not in assignment:
            for b in csp.curr_domains[B][:]:
                if not csp.constraints(var, value, B, b):
                    csp.prune(B, b, removals)
            if not csp.curr_domains[B]:
                csp.wipeout=+1
                csp.weights[(var,B)]=+1
                csp.weights[(B,var)]=+1
                return False
    return True


def dom_deg_weight(csp,assingment,variable):
    a_weight=1
    for neighbor_var in csp.neighbors[variable]:
        if (neighbor_var not in assingment):
            a_weight+=csp.weights[(variable,neighbor_var)]
    return a_weight

def confilict_directed_variable_ordering(assingment,csp):
    min=[99999,None]
    for variable in csp.variables:
        if (variable not in assingment):
            order_value=len(csp.domains[variable])/dom_deg_weight(csp,assingment,variable)
            if (order_value<min[0]):
                min[0]=order_value
                min[1]=variable
    return min[1]


class Schedule_CSP(csp.CSP):

    def __init__(self,csv_file):
        TIME_SLOTS=3*21
        self.variables=[]
        self.domains=dict()
        self.neighbors=dict()

        self.weights=dict()
        
        self.nconstraints_checked=0
        self.wipeouts=0
        
        
        records=self.read_classes(csv_file)
        NUM_OF_VARIABLES=len(records)
        for i in range(NUM_OF_VARIABLES):
            self.variables.append(tuple(records[i]))
            self.weights[tuple(records[i])]=list
            self.neighbors[self.variables[i]]=[]
        values=[]
        no_first_hours=[]
        no_last_hours=[]
        for i in range(TIME_SLOTS):
            values.append((int(i/3),i%3))
            if (i%3!=0):
                no_first_hours.append((int(i/3),i%3))
            elif (i%3!=2):
                no_last_hours.append((int(i/3),i%3))

        for i in range(NUM_OF_VARIABLES):
            if (self.variables[i][4]==True):
                self.domains[self.variables[i]]=no_last_hours#a class that should be followed by the lab related to it cannot be the in the last time slot
            elif (self.variables[i][2][-11:]=="Εργαστήριο"):
                self.domains[self.variables[i]]=no_first_hours#a lab that should be after the class related to the lab cannot be in the first timeslot
            else:
                self.domains[self.variables[i]]=values
            for j in range(NUM_OF_VARIABLES):
                if (i!=j):
                    self.weights[self.variables[i],self.variables[j]]=1
                    self.neighbors[self.variables[i]].append(self.variables[j])

        super().__init__(self.variables,self.domains,self.neighbors,self.var_constraints)
            
            
    def var_constraints(self,A,a,B,b):
        self.nconstraints_checked+=1
        if (a==b):#no same timeslot can be used in two classes
            return False
        if (a[0]==b[0]):#if we are on the same day
            if ((a[1]-b[1])==1 and B[4]==True and A[1]!=(B[1]+" Εργαστήριο")):#consecutive exams where A should contain the lab exam of the previous exam, but does not
                return False
            elif ((b[1]-a[1])==1 and A[4]==True and B[1]!=(A[1]+" Εργαστήριο")):#consecutive exams where B should contain the lab exam of the previous exam, but does not
                return False
            elif (A[2]==B[2] and B[1]!=(A[1]+" Εργαστήριο") and A[1]!=(B[1]+" Εργαστήριο")):#different classes of the same proffesor cannot be in the same day
                return False
            elif (B[0]==A[0] and B[1]!=(A[1]+" Εργαστήριο") and A[1]!=(B[1]+" Εργαστήριο")):#classes of the same semester cannot be in the same day
                return False
            elif ((B[1]==(A[1]+" Εργαστήριο") or A[1]==(B[1]+" Εργαστήριο")) and (abs(a[1]-b[1])!=1)):#lab examination must follow the examination of the class related
                return False
        if (A[3]==True and B[3]==True and abs(a[0]-b[0])<2):#there needs to be a one day interval between difficult classes
            return False
        if (a[0]!=b[0] and (B[1]==(A[1]+" Εργαστήριο") or A[1]==(B[1]+" Εργαστήριο"))):#lab of class cannot be in a different day of the class
            return False
        if ((A[1][-11:]=="Εργαστήριο" and B[1]!=(A[1]+" Εργαστήριο")) or (B[1][-11:]=="Εργαστήριο" and A[1]!=(B[1]+" Εργαστήριο"))):#a lab can only be placed after the exam of the class related to it
            return False
        return True
        
    def read_classes(self,csv_file): 
        df=pd.read_csv(csv_file)
        records=df.to_numpy().tolist()
        classes_with_lab=df[df["Εργαστήριο (TRUE/FALSE)"]==True]
        labs=classes_with_lab.to_numpy().tolist()
        for i in range(len(labs)):
            labs[i][1]=labs[i][1]+" Εργαστήριο"
            labs[i][3]=False
            labs[i][4]=False
            records.append(labs[i])
        return records

obj=Schedule_CSP("Classes.csv")


start=time.time()
assingment=csp.backtracking_search(obj,select_unassigned_variable=csp.mrv,order_domain_values=csp.lcv,inference=csp.forward_checking)
end=time.time()
time_df=end-start
print(f"FC+MRV+LCV took: {time_df}")
print(f"{obj.nassigns} times constraints were checked, {obj.nassigns} assingments were made, and {obj.wipeouts} wipeouts occured")
#for i in range(len(assingment)):
    #print(assingment[i]+'\n')

print("\n\n")


obj=Schedule_CSP("Classes.csv")

start=time.time()
assingment=csp.backtracking_search(obj,select_unassigned_variable=confilict_directed_variable_ordering,order_domain_values=csp.lcv,inference=FC_dom_deg)
end=time.time()
time_df=end-start
print(f"FC+dom/deg+LCV took: {time_df}")
print(f"{obj.nassigns} times constraints were checked, {obj.nassigns} assingments were made, and {obj.wipeouts} wipeouts occured")
#for i in range(len(assingment)):
    #print(assingment[i]+'\n')

print("\n\n")



obj=Schedule_CSP("Classes.csv")

start=time.time()
assingment=csp.backtracking_search(obj,select_unassigned_variable=csp.mrv,order_domain_values=csp.lcv,inference=mac)
end=time.time()
time_df=end-start
print(f"MAC+MRV+LCV took: {time_df}")
print(f"{obj.nassigns} times constraints were checked, {obj.nassigns} assingments were made, and {obj.wipeouts} wipeouts occured")
#for i in range(len(assingment)):
    #print(assingment[i]+'\n')

print("\n\n")

obj=Schedule_CSP("Classes.csv")

start=time.time()
assingment=csp.backtracking_search(obj,select_unassigned_variable=confilict_directed_variable_ordering,order_domain_values=csp.lcv,inference=mac)
end=time.time()
time_df=end-start
print(f"MAC+dom/deg+LCV took: {time_df}")
print(f"{obj.nassigns} times constraints were checked, {obj.nassigns} assingments were made, and {obj.wipeouts} wipeouts occured")
#for i in range(len(assingment)):
    #print(assingment[i]+'\n')

print("\n\n")





obj=Schedule_CSP("Classes.csv")


start=time.time()
assingment=csp.min_conflicts(obj,max_steps=10000)
end=time.time()
time_df=end-start
print(f"MIN CONFLICTS took: {time_df}")
print(f"{obj.nassigns} times constraints were checked, {obj.nassigns} assingments were made, and {obj.wipeouts} wipeouts occured")
#for i in range(len(assingment)):
    #print(assingment[i]+'\n')

print("\n\n")
