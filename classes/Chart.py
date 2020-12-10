import matplotlib.pyplot as plt
import numpy as np

class Chart :

    @staticmethod
    def createPieChart(title, datas, labels, explode, autopct = '%1.2f%%') :
        '''Create Pie chart with matplotlib'''
        fig, ax = plt.subplots()

        fig.patch.set_facecolor('white')

        ax.pie(datas, explode=explode, labels=labels, autopct=autopct,
                shadow=True, startangle=90)
        ax.axis('equal')

        plt.title(title)

        plt.show()

    @staticmethod
    def createBarHChart(title, datas, labels, colors = ['blue']) :
        '''Create Bar Horizontal chart with matplotlib'''
        barWidth = 0.7

        plt.figure().patch.set_facecolor('white')

        r = range(len(datas))

        plt.yticks(range(len(datas)), labels)

        plt.title(title)

        plt.barh(r, datas, height = barWidth, color = colors)

    @staticmethod
    def histGraph(labelsBar, heightBar, garphTitile, xAxeTitle, yAxeTitle):
        plt.bar(labelsBar, heightBar)
        plt.title(garphTitile)
        plt.xlabel(xAxeTitle)
        plt.ylabel(yAxeTitle)
        plt.show()

    @staticmethod
    def drawHorizontalThreeBarsChart(keys, vals, labels, height=0.8):
        plt.figure(figsize=(20,15))

        # trick to display bars in descending order
        Y = list(reversed(keys))
        for idx,val in enumerate(vals):
            vals[idx] = list(reversed(val))


        n = len(vals) # n = 3
        _Y = np.arange(len(Y)) # _Y = array([0, 1, 2, ...])

        # ajout des bard de graph
        for i in range(n):
            # _Y - 0.8/2. = array([-0.4,  0.6,  1.6])
            plt.barh(_Y - height/2. + i / float(n)*height, vals[i],
                    height=height/float(n), align="edge", label=labels[i])

        # placement des ticks sur l'axe Y
        plt.yticks(_Y, Y)
        # placement de la légende
        plt.legend()

        plt.show()
