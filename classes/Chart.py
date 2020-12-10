import matplotlib.pyplot as plt

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