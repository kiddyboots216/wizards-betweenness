from Numberjack import *
import sys

def numberjack_20(input1, number, seconds=-1):
    model = Model()
    inputfile = open(input1 + ".in", "r")
    inputfile = inputfile.readlines()[2:]
    storage = []
    constraints = []
    wizardlist = set()
    for line in inputfile:
        newcomp = line.replace(" \n", "").replace("\n", "").split(" ")
        storage.append(newcomp)
    for i in range (len(storage)):
        for wizard in storage[i]:
            wizardlist.add(wizard)
        comparison = [[storage[i][2] + ">" + storage[i][1], storage[i][2] + ">" + storage[i][0]], [storage[i][2] + "<" + storage[i][1], storage[i][2] + "<" + storage[i][0]]]
        constraints.append(comparison)
    for wizard in wizardlist:
        exec(wizard + " = Variable(" + number[:-2] + ", wizard)") in globals(), locals()
    for constraint in constraints:
        model.add(Disjunction([Conjunction([eval(constraint[0][0]), eval(constraint[0][1])]), Conjunction([eval(constraint[1][0]), eval(constraint[1][1])])]))
    wizardlist = [eval(wizard) for wizard in wizardlist]
    #model.add(AllDiff(wizardlist))
    solver = model.load('MiniSat')
    print("number of wizards: " + str(len(wizardlist)))
    print("number of variables: " + str(solver.getNumVariables()))
    print("number of constraints: " + str(solver.getNumConstraints()))
    if seconds != -1:
        solver.setTimeLimit(seconds)
    solver.solve()
    dictionary = {}
    for wizard in wizardlist:
        dictionary[wizard.name()] = wizard.get_value()
    names = [wizard.name() for wizard in wizardlist]
    names.sort(key=lambda s: dictionary[s])
    wizardages = [name + ": " + str(dictionary[name]) for name in names]
    names = " ".join(names)
    wizardages = " ".join(wizardages)
    print("completed for " + number + " in " + str(solver.getTime()) + " seconds")
    print(names)
    return ["completed for " + number + " in " + str(solver.getTime()) + " seconds", "\n", wizardages, "\n", names, "\n\n"]

def testStudentInputs():
    textfile = open("170output.txt", "w")
    for i in range(0, 10):
        textfile.writelines(numberjack_20("inputs/input20_" + str(i), "20_" + str(i), 1200))
    for i in range(0, 10):
        textfile.writelines(numberjack_20("inputs/input35_" + str(i), "35_" + str(i), 3000))
    for i in range(0, 10):
        textfile.writelines(numberjack_20("inputs/input50_" + str(i), "50_" + str(i), 6000))
    textfile.close()

def testStaffInputs(num):
    result = numberjack_20("staff_" + str(num), str(num) + "_0")
    textfile = open("StaffOutput" + str(num) + ".txt", "w")
    textfile.writelines(result)
    textfile.close()

if __name__ == '__main__':
    if (sys.argv[1:]):
        testStaffInputs(sys.argv[1])
    else:
        testStudentInputs()
