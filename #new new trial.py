#new new trial
import pandas as pd
from sympy import symbols, solve, sympify


############################################# input
# Define some input variables
streams = []
components = []
components_short = []
fraction = "y" # y for mole fraction, x for mass fraction


while 1>0:
    tem=input("input components and input 'x' to quit")
    if tem.lower()=="x":
        break
    else:
        tem=tem.upper()
        components.append(tem)

I=1
while 1>0:
    print("input 'in' or 'out' for stream",I,"and input 'x' to quit")
    tem=input()
    if tem.lower()=="x":
        break
    else:
        tem=tem.lower()
        streams.append(tem)
    I+=1

for count in range(len(components)):
    components_short.append(components[count][:1])
print(components)
print(streams)
print(components_short)
################################################
# Create stream and component (with flow rate) labels for the table
stream_labels = [f"{i+1}-{item}" for i, item in enumerate(streams)]
component_labels = ["Flow rate"]+components
################################################
# Create a pandas DataFrame with the dimensions of the number of streams by the number of components
df1 = pd.DataFrame(index=stream_labels, columns=component_labels)

# Loop through every cell of the DataFrame and fill it with a sympy symbol
for i in range(df1.shape[0]):
    for j in range(df1.shape[1]):
        # If the column index is 0, the symbol is given a label that consists of the first letter of "Flow rate"
        # and the index of the row
        if j == 0:
            df1.iloc[i,j] = symbols(f"{component_labels[0][0]}{i+1}")
        # Otherwise, the symbol is given a label that consists of the fraction type (mass or mole),
        # the index of the row, and the abbreviation of the component name
        else:
            df1.iloc[i,j] = symbols(f"{fraction}{i+1}{components_short[j-1]}")

# Display the resulting DataFrame
print(df1)
##################################################
# Define a dictionary of given variable values
given_variables={}
given_zeros={}
while 1>0:
    Tem1,Tem2=input("input given components and value(split by space) and input'x' to quit").split()
    if "x" in Tem1 or "x" in Tem2:
        print("break")
        break
    else:
        if Tem2=="0":
            given_zeros[Tem1]=float(Tem2)
        given_variables[Tem1]=float(Tem2)
    
print(given_variables)
# If no process equations, just let process_eqs = 0
process_eqs = []
print("givenzero=",given_zeros)


# Define a function that loops through every cell of a DataFrame and returns a list of tuples
# representing each cell along with its indices
def loop_table(df):
    cells = []
    for i, row in enumerate(df.values):
        for j, value in enumerate(row):
            cells.append( (i, j, value) )
    return cells

# Create a copy of the original DataFrame
df2 = df1.copy()

# Loop through every cell in the original DataFrame and check if the string representation of the value
# in that cell is a key in the given_variables dictionary. If it is, replace the value in the corresponding
# cell of the copied DataFrame with the value from the dictionary.
for i, j, value in loop_table(df1):
    if str(value) in given_variables:
        df2.iloc[i,j] = given_variables[ str(value) ]

# Display the resulting DataFrame
print(df2)
#######################################
while 1>0:
    compoA,compoB,ratio=input("input the relationship in presented dataframe and input any 'x' to quit").split()
    if "x" in compoA or "x" in compoB or "x" in ratio:
        break
    else:
        process_eqs.append("{0}-{1}*{2}".format(compoA,compoB,ratio))

print(process_eqs)
#######################################
#################varaibles analysis########################
Nz=len(given_zeros)
Ns=len(streams)
Nc=len(components)
Np=len(process_eqs)
Nv=Ns*(Nc+1)-Nz
print("Nv=",Nv)
Ne=Ns+Nc+Np                                                                        
print("Ne=",Ne)
Nd=Nv-Ne

motsu=len(given_variables)+Np
if motsu>=Nd:
    print("this can be solved!!")
else:
    print("nope!!")


##############################################
# Create an empty list to store all the simutaneous equations that will be solved later
indep_eqs = []

# Loop through each component and create a raw equation for each one
for i, label in enumerate(components):
    raw_eq = 0
    
    # Loop through each stream and add or subtract the flow rate multiplied by the mole or mass fraction
    # of the current component, depending on whether the stream is incoming or outgoing
    for j, direction in enumerate(streams):
        
        if direction == "in":
            raw_eq = raw_eq + df2.iloc[j,0]*df2.iloc[j, i+1]
            
        if direction == "out":
            raw_eq = raw_eq - df2.iloc[j,0]*df2.iloc[j, i+1]
            
    # Append the raw equation to the list of independent equations
    indep_eqs.append(raw_eq)

# Loop through each stream and add a mass or mole balance equation
for i in df2.iloc[:,1:].sum(axis=1):
    indep_eqs.append(i-1)

# If additional process equations were provided, add them to the list of independent equations
if process_eqs != 0:
    for i in process_eqs:
        # Convert the string equation to a sympy expression and substitute given variables
        i = sympify(i).subs(given_variables)
        indep_eqs.append(i)

# Print the resulting simultaneous equations
#print ("The simuteneous equations are:")
#print(indep_eqs) 

# Solve the system of equations and print the solutions
solutions = solve(indep_eqs)
print ("The solutions are:")
print(solutions)



dic_solution_key=[]
dic_solution_value=[]
for sol_key,sol_value in solutions[0].items():
    dic_solution_key.append(sol_key)
    dic_solution_value.append(sol_value)
dic_=solutions[0]


e=0
for i, j, value in loop_table(df2):
    for lenghth in range(len(dic_solution_key)):
        if value==dic_solution_key[lenghth]:
            df2.iloc[i,j]=round(dic_solution_value[lenghth],3)
            
print(df2)
