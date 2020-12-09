import matplotlib.pyplot as plt

class Chart :

    @staticmethod
    def createPieChart(title, datas, labels, explode, autopct = '%1.2f%%') :
        fig, ax = plt.subplots()
        
        ax.pie(datas, explode=explode, labels=labels, autopct=autopct,
                shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        plt.title(title)

        plt.show()