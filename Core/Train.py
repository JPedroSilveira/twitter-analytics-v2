import time
import msvcrt
from Data.Dataset import TweetDS, WordDS, WorldDS

DATA_SET_LOCATION = '.\\Dataset\\'


class Train:

    def read_train_data(self, filename: str, enconding: str, n_columns: int, emotion_position: int, text_position: int,
                        init_line: int,
                        negative_emotion_value, consider_only_negative=False):

        with open(DATA_SET_LOCATION + filename, encoding=enconding) as dataset:
            start_time = time.time()
            lines = dataset.readlines()
            data_count = init_line
            world_ds = WorldDS.load(0)

            if world_ds is None:
                world_ds = WorldDS()

            for line in range(init_line, len(lines)):
                print("Lendo linha: " + str(data_count))
                data_count = data_count + 1
                data = lines[line].split(',', n_columns - 1)

                text = data[text_position].replace('"', '')
                negative = data[emotion_position].replace('"', '') == negative_emotion_value
                tweet_ds = TweetDS.load_by_text(data[text_position])

                # Just use new tweets texts
                if tweet_ds is None and (not consider_only_negative or negative):
                    tweet_ds = TweetDS(text, negative)
                    tweet_ds.db_save()

                    if negative:
                        world_ds.add_negative()
                    else:
                        world_ds.add_positive()

                    world_ds.db_save()

                    words = tweet_ds.get_words()

                    for word in words:
                        word_ds = WordDS.load_by_text(word)

                        if word_ds is None:
                            word_ds = WordDS(word)

                        if negative:
                            word_ds.add_negative()
                        else:
                            word_ds.add_positive()

                        word_ds.db_save()

                if self.verify_end_option():
                    break

        end_time = time.time()
        print('Finishing training in: ' + str(end_time - start_time) + ' seconds')

    @staticmethod
    def verify_end_option() -> bool:
        if msvcrt.kbhit():
            if msvcrt.getch() == b'c' or msvcrt.getch() == b'C':
                return True

        return False
