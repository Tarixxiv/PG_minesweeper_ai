from QLearningAgent import QLearningAgent
from MineSweeper import MineSweeper
from matplotlib import pyplot as plt

if __name__ == '__main__':
    q = QLearningAgent()


    ##Jak na szybko dostać wykresy
    ##1)zmodyfikuj output z q.agent_loop(5, 30000) by zwracał ci co potrzebujesz
    ##2)

    # arr = q.agent_loop(5, 30000)
    #
    #
    # plt.plot(arr)
    # plt.xlabel("Numer episodu")
    # plt.ylabel("Ilość zwycięstw")
    # plt.title("Ilość zwycięstw w danym episodzie dla planszy 5x5")
    # plt.show()


    ##poniższe służy do sprawdzania ilości

    # checked_dimensions = [5,10,15,20,25]
    # results = []
    # for i in checked_dimensions:
    #     q = QLearningAgent()
    #     results.append(q.agent_loop(i, 10000)[-1])
    #
    # plt.plot(checked_dimensions, results, linestyle="None")
    # plt.yscale("log")
    # plt.xlabel("Rozmiar boku planszy")
    # plt.ylabel("Współczynnik zwycięstwa")
    # plt.title("Współczynnik zwycięstwa wedle rozmiaru planszy dla 10k episodów")
    # plt.show()




    arr, arr2 = q.agent_loop(8, 30000)


    plt.plot(arr,label = "zwycięstwa")
    plt.plot(arr2,label = "porażki")
    plt.legend()
    plt.xlabel("Numer episodu")
    plt.ylabel("Ilość")
    plt.title("Ilość zwycięstw i porażek w danym episodzie dla planszy 8x8")
    plt.show()