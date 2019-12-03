from Core.Error import AnalyzeError
from Data.Dataset import WorldDS, WordDS
from Database.Index.BTree.BTree import BTree
from Database.Index.BTree.BTreeNode import BTreeNode50String


# Classes: positivo, negativo
# True for negative and False for positive
# Using Naive Bayes algorithm
def infer_emotion(tweet: object) -> (bool, float, float):
    world_ds = WorldDS.load(0)

    if world_ds is not None and world_ds.total_positive != 0 and world_ds.total_negative != 0:
        words = tweet.get_filtered_words()
        word_dataset_text_id = BTree('word_dataset_text_id', BTreeNode50String, WordDS, WordDS)

        mult_sum_pos = 1
        mult_sum_neg = 1

        # Calcula probabilidade de cada palavra ser negativa ou positiva
        for word in words:
            word_ds = word_dataset_text_id.find_first_or_default(word)

            # Apenas considera palavras com aparições
            if word_ds is not None:
                # Probabilidade da palavra (positivo e negativo): Vezes que apareceu sobre total de frases analisadas
                p_positive = word_ds.n_positive/world_ds.total_positive
                p_negative = word_ds.n_negative/world_ds.total_negative

                # Produtório das probabilidades
                if p_positive != 0 and p_negative != 0:
                    mult_sum_pos = mult_sum_pos * p_positive
                    mult_sum_neg = mult_sum_neg * p_negative

        # Finally multiply with the total probability
        world_total = world_ds.total_positive + world_ds.total_negative
        mult_sum_pos = mult_sum_pos * (world_ds.total_positive/world_total)
        mult_sum_neg = mult_sum_neg * (world_ds.total_negative/world_total)

        if mult_sum_pos >= mult_sum_neg:
            return False, mult_sum_pos, mult_sum_neg
        else:
            return True, mult_sum_pos, mult_sum_neg

    else:
        raise AnalyzeError.TryingToInferWithoutWorldData("World dataset without any data!")