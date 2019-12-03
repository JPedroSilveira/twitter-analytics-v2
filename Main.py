from Data.Twitter import Tweet
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNode50String, BTreeNode50IntString, BTreeNodeFloat
from Twitter.TwitterCore import TwitterCore
from Core.Train import Train


def start_twitter_stream(key_word):
    twitter_core = TwitterCore()

    twitter_core.start_with(key_word)

    twitter_core.stream(key_word, 'en')


def start_train(file_name, n_columns, emotion_position, text_position, init_line, negative_emotion_value,
                consider_only_negative=False):
    train = Train()

    train.read_train_data(file_name, "utf-8", n_columns, emotion_position, text_position, init_line,
                          negative_emotion_value, consider_only_negative)


def line_separator():
    print("...........................................................................................................")


def load_dataset():
    print("Primeiramente verifique se você salvou seu dataset no diretório Dataset deste projeto.")
    line_separator()
    print("Iremos fazer algumas perguntas sobre o padrão do dataset.")
    print("Ele deve ser um CSV contendo uma coluna classificando o texto como ruim ou bom e uma outra coluna com o "
          "texto completo.")
    print("Assim que a leitura começar você poderá pressionar \"C\" para finaliza-lá a qualquer momento.")
    line_separator()
    class_column = int(input("Digite o número da coluna com a classificação: "))
    text_column = int(input("Digite o número da coluna com o texto: "))
    columns = int(input("Digite o número total de colunas do arquivo: "))
    init = int(input("Digite o número da linha onde a leitura deve começar: "))
    negative_value = input("Digite o valor da classificação negativa: ")
    file_name = input("Digite o nome do arquivo (sem o .csv): ") + ".csv"
    line_separator()
    print("Iremos começar o treinamento agora...")
    print("Lembre-se: para finalizar aperte enter!")
    start_train(file_name, columns, class_column, text_column, init, negative_value)


def search_tweets():
    line_separator()
    key = input("Digite uma palavra para fazer a pesquisa por tweets: ")

    start_twitter_stream(key)

    analize_data(key)


def analize_data(key):
    continue_analyze = True
    while continue_analyze:
        line_separator()
        print("Bem vindo ao menu de analise de resultado! \n")
        print("Selecione uma das opções abaixos para continuar:")
        line_separator()
        print("1) Número de tweets negativos e positivos analisalidos.")
        print("2) Palavras mais citadas nos textos negativos.")
        print("3) Palavras mais citadas nos textos positivos.")
        print("4) Carrega os Tweets mais negativos.")
        print("5) Carrega os Tweets mais positivos.")
        print("6) Encerrar.")
        line_separator()
        option = input("Digite sua opção: ")
        line_separator()

        if not start_analize_action(key, option):
            continue_analyze = False


def start_analize_action(key, input):
    if input == "1":
        load_number_of_positive_and_negative_tweets(key)
    elif input == "2":
        load_most_used_negative_words(key)
    elif input == "3":
        load_most_used_positive_words(key)
    elif input == "4":
        load_most_negative_tweets(key)
    elif input == "5":
        load_most_positive_tweets(key)
    elif input == "6":
        return False
    else:
        print("Entrada inválida. Tente novamente...")

    return True


def load_number_of_positive_and_negative_tweets(key):
    bt_data_name = BTree('twitter_core_data_name', BTreeNode50String, TwitterCore, TwitterCore)
    core = bt_data_name.find_first_or_default(key)

    line_separator()
    print("Foram analizados: " + str(core.tweets) + " tweets com a chave \"" + key + "\".")
    print("Total de: ")
    print(" -" + str(core.negative_count) + " negativos;")
    print(" -" +str(core.positive_count) + " positivos;")
    line_separator()
    input("Aperte enter para continuar...")


def load_most_negative_tweets(key):
    line_separator()
    n = int(input("Digite o número de tweets que deseja buscar (máximo de 50): "))
    if n > 50:
        n = 50

    bt_core_most_negative = BTree('twitter_core_most_negative_' + key, BTreeNodeFloat, TwitterCore, Tweet)
    tweets = bt_core_most_negative.find_n_biggest(n)

    line_separator()
    print("Listagem dos tweets mais negativos: ")
    for tweet in tweets:
        print("Tweet: " + tweet.text)
    line_separator()
    input("Aperte enter para continuar...")


def load_most_positive_tweets(key):
    line_separator()
    n = int(input("Digite o número de tweets que deseja buscar (máximo de 50): "))
    if n > 50:
        n = 50

    bt_core_most_positive = BTree('twitter_core_most_positive_' + key, BTreeNodeFloat, TwitterCore, Tweet)
    tweets = bt_core_most_positive.find_n_biggest(n)

    line_separator()
    print("Listagem dos tweets mais positivos: ")
    for tweet in tweets:
        print("Tweet: " + tweet.text)
    line_separator()
    input("Aperte enter para continuar...")


def load_most_used_negative_words(key):
    line_separator()
    n = int(input("Digite o número de palavras que deseja buscar (máximo de 50): "))
    if n > 50:
        n = 50

    bt_core_most_negative_words = BTree('bt_core_most_negative_words' + key, BTreeNode50IntString, TwitterCore)
    bt_core_most_negative_words_main = BTree('bt_core_most_negative_words_main_' + key, BTreeNode50String, TwitterCore)
    words = bt_core_most_negative_words.find_n_biggest(n)

    line_separator()
    print("Listagem das palavras mais usadas em textos negativos: ")
    for word in words:
        number = bt_core_most_negative_words_main.find_first_or_default(word)
        print("Palavra: " + word + " com " + str(number) + " usos.")
    line_separator()
    input("Aperte enter para continuar...")


def load_most_used_positive_words(key):
    line_separator()
    n = int(input("Digite o número de palavras que deseja buscar (máximo de 50): "))
    if n > 50:
        n = 50

    bt_core_most_positive_words = BTree('bt_core_most_positive_words' + key, BTreeNode50IntString, TwitterCore)
    bt_core_most_positive_words_main = BTree('bt_core_most_positive_words_main_' + key, BTreeNode50String, TwitterCore)
    words = bt_core_most_positive_words.find_n_biggest(n)

    line_separator()
    print("Listagem das palavras mais usadas em textos positivos: ")
    for word in words:
        number = bt_core_most_positive_words_main.find_first_or_default(word)
        print("Palavra: " + word + " com " + str(number) + " usos.")
    line_separator()
    input("Aperte enter para continuar...")


def start_action(input) -> bool:
    if input == "1":
        load_dataset()
    elif input == "2":
        search_tweets()
    elif input == "3":
        return False
    else:
        print("Entrada inválida. Tente novamente...")

    return True


def menu():
    continue_program = True

    while continue_program:
        line_separator()
        print("Bem vindo ao menu do Twitter Analytics V2.0 \n")
        print("Selecione uma das opções abaixos para continuar:")
        line_separator()
        print("1) Carregar dataset")
        print("2) Busca e classificação de tweets")
        print("3) Encerrar")
        line_separator()
        option = input("Digite sua opção: ")
        line_separator()
        continue_program = start_action(option)

    print("Encerrando programa...")
    print("Até mais!")


def main():
    # start_twitter_stream('Trump')

    # start_train("KazAnove_dataset.csv", 6, 0, 5, 810004, "0")
    menu()


main()
