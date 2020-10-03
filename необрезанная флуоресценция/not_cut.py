import csv

from numpy import exp, loadtxt, pi, sqrt
from lmfit import Model
import matplotlib.pyplot as plt
from matplotlib import rc

def exponential(t, a=1,  tau1=1,  c=0.01):
    e1 = 2.718 ** (-t / tau1)
    return a * e1  + c


class outputs:
    par_out = False
    def param_out(self, inf_src, titles_arr, iter_num=0, head="------"):
        if iter_num != 0:
            iter_num_in_func = iter_num
        else:
            iter_num_in_func = len(inf_src)

        if outputs.par_out:  # определение способа вывода данныцх  в файл
            par_out_mode = 'a'
        else:
            par_out_mode = 'w'

        with open('parameters.csv', par_out_mode) as myfile:
            myfile.write(head + '\n')
            for x in range(iter_num_in_func):
                myfile.write(titles_arr[x])
                for key, value in inf_src[x].best_values.items():
                    str_to_file = "{0} = {1:.2f}, ".format(key, value)
                    myfile.write(str_to_file)
                myfile.write("redchi = {0:.2f}".format(inf_src[x].redchi))
                myfile.write('\n')
            outputs.par_out = True  # если в ходе программы данная функция была выхвана хоть один раз, и при этом был создан файл с параметрами, то в дальнейшем параметры будут вноситься в этот файл с концеа, а не перезаписываться
        myfile.close()


fileNames = [ 'data_for_plotting2.csv' ]
fileColNums = {'data_for_plotting2.csv' : (0 , 8) }
X_data = []
Y_data = []

NUM_Of_COL = 8

for i in range(4):
    X_data.append([])
    Y_data.append([])

for filename in fileNames:
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=';')

        #чтение CSV файла в массив
        rowNum = 1
        for row in readCSV:
            if rowNum > 2:

                X_dataVar = row[0 : fileColNums[filename][1] : 2]
                Y_dataVar = row[1 : fileColNums[filename][1] : 2]

                for i in range(len(X_data)):
                    if X_dataVar[i] != '': # обработка пустых значений в CSV файле
                        X_data[i].append(float(X_dataVar[i]))
                        Y_data[i].append(float(Y_dataVar[i]))


            rowNum += 1


Y_max = []
for i in range(len(Y_data)):
    Y_max.append(max(Y_data[i]))


for j in range(len(Y_data)):
    for i in range(len(Y_data[j])):
        Y_data[j][i] = (Y_data[j][i]) / Y_max[j]


sing_exp_model = Model(exponential)
resultDelFluor = sing_exp_model.fit(Y_data[0],
                                    t=X_data[0],
                                    a=1,
                                    tau1=1)


resultPhos = sing_exp_model.fit(Y_data[1],
                                    t=X_data[1],
                                    a=1,
                                    tau1=1)




plt.figure(111)

#rc('text', usetex = True)

fig = plt.figure()
ax = fig.add_subplot(111)


ax.text(1.5, 0.2, '1', style='italic')
ax.text(3.5, 0.2, '2', style='italic')
ax.text(0, 1.05, "I, отн. ед.", style='italic')
#ax.text(10.3, 0,  "t, с", style='italic')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

#plt.title('         Кинетические кривые затухания фосфоресценции  ' + '\n' + '     и замедленной  флуоресценции тройных комплексов')
plt.plot(X_data[0], Y_data[0]) #флуоресценция
plt.plot(X_data[1], Y_data[1]) #фосфоресценция
plt.axis([0, 10, 0, 1])
plt.xlabel("t, с", style='italic')
#plt.ylabel("I, отн. ед.")
plt.plot(X_data[0], resultDelFluor.best_fit, linewidth=0.5)
plt.plot(X_data[1], resultPhos.best_fit, linewidth=0.5)
plt.legend(loc='best')
filename = "Phos_and_fluor_lifetimes" + ".png"
plt.savefig(filename)




plt.figure(2)
fig2 = plt.figure()
axe = fig2.add_subplot(111)
axe.text(355, 0.65, '1', style='italic')
axe.text(550, 0.55, '2', style='italic')

axe.text(300, 1.05, "I, отн. ед.",style='italic' )
#axe.text(720, 0,  r'$\lambda$, нм', style='italic')

axe.spines['right'].set_visible(False)
axe.spines['top'].set_visible(False)
axe.yaxis.set_ticks_position('left')
axe.xaxis.set_ticks_position('bottom')

plt.axis([300, 700, 0, 1])
plt.xlabel(r'$\lambda$, нм', style='italic')
#plt.ylabel("I, отн. ед.")
#plt.title('Спектры фосфоресценции и замедленной ' + '\n' + 'флуоресценции')
plt.plot(X_data[2], Y_data[2], 'g-') #флуоресценция
plt.plot(X_data[3], Y_data[3], 'b-') #фосфоресценция
#plt.legend(loc='best')
filename = "Phos_and_fluor" + ".png"
plt.savefig(filename)




paramInf = []
nameInf = ["Delayed Fluorescence","Phosphorescence"]
paramInf.append(resultDelFluor)
paramInf.append(resultPhos)

out_obj = outputs()
out_obj.param_out(paramInf,
                  nameInf,
                  2,
                  )
