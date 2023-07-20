import re
import file_io
import text_normalizer
# import syllables
import syllapy

RU_ALPHABET = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о", "п", "р", "с", "т", "у",
               "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]


FLESCH_GLOBAL_CONST = 206.835
RU_FLESCH_ASL_CONST = 1.3
RU_FLESCH_ASW_CONST = 60.1
EN_FLESCH_ASL_CONST = 1.015
EN_FLESCH_ASW_CONST = 84.6
EN_GUNNING_FOX_CONST = 0.4


def split_text_into_sentence_list(text):
    sentence_list = re.split(r"(\.{1,3}|[?!])\s?", text)
    del sentence_list[-1]
    sentence_list = [sentence for sentence in sentence_list if re.match(r"(\.{1,3}|[?!]|\W)", sentence) is None]
    return sentence_list


def split_text_into_word_list(text):
    word_list = re.split(r"(\.{1,3}|[-?!),:;\"\'\]]*)(\s|\b)[\[(\"]?", text)
    word_list = [word for word in word_list if re.match(r"(\s*$)|\bs\b|[-,)(\[\]:;\"\'’.!?]+", word) is None]
    return word_list


def count_average_sentences_length(sentence_list):
    sum_of_sentences_lengths = 0
    for sentence in sentence_list:
        sum_of_sentences_lengths += len(split_text_into_word_list(sentence))
    mean_sentence_length = sum_of_sentences_lengths/len(sentence_list)
    return mean_sentence_length


def count_average_word_length(word_list):
    sum_of_word_lengths = 0
    for word in word_list:
        sum_of_word_lengths += len(word)
    mean_word_length = sum_of_word_lengths/len(word_list)
    return mean_word_length


def count_ru_word_syllables(word):
    num_of_syllables = 0
    for letter in word.lower():
        if re.match(r"[аеёиоуыэюя]", letter) is not None:
            num_of_syllables += 1
    return num_of_syllables


def count_en_word_syllables(word):
    # my own realization - it's just poop
    # num_of_syllables = len(re.findall(r"([aeyuio]{1,2})|([^aeyuio]le\b)", word.lower()))
    # if (re.search(r"([ayuioe]le\b)|([^tdayuioe]ed\b)", word) is not None) and (len(word) > 3):
    #     num_of_syllables -= 1
    # not sa accurate counting of syllables
    # num_of_syllables = syllables.estimate(word)
    num_of_syllables = syllapy.count(word)
    return num_of_syllables


def count_en_complex_words(word_list):
    num_of_complex_words = 0
    for word in word_list:
        if count_en_word_syllables(word) > 2:
            num_of_complex_words += 1
    return num_of_complex_words


def count_average_word_list_syllables(word_list, count_syllables_func):
    num_of_word_list_syllables = 0
    for word in word_list:
        num_of_word_list_syllables += count_syllables_func(word)
    mean_word_list_syllables = num_of_word_list_syllables/len(word_list)
    return mean_word_list_syllables


def find_ru_fre(text):
    sentence_list = split_text_into_sentence_list(text)
    avg_sentence_length = count_average_sentences_length(sentence_list)
    word_list = split_text_into_word_list(text)
    avg_syllables = count_average_word_list_syllables(word_list, count_ru_word_syllables)
    fre_score = FLESCH_GLOBAL_CONST - RU_FLESCH_ASL_CONST * avg_sentence_length - RU_FLESCH_ASW_CONST * avg_syllables
    return fre_score


def find_en_fre(text):
    sentence_list = split_text_into_sentence_list(text)
    avg_sentence_length = count_average_sentences_length(sentence_list)
    word_list = split_text_into_word_list(text)
    avg_syllables = count_average_word_list_syllables(word_list, count_en_word_syllables)
    fre_score = FLESCH_GLOBAL_CONST - EN_FLESCH_ASL_CONST * avg_sentence_length - EN_FLESCH_ASW_CONST * avg_syllables
    return fre_score


def find_en_gfi(text):
    sentences_list = split_text_into_sentence_list(text)
    avg_sentence_length = count_average_sentences_length(sentences_list)
    words_list = split_text_into_word_list(text)
    avg_num_of_complex_words = count_en_complex_words(words_list)/len(words_list)
    gfi_score = EN_GUNNING_FOX_CONST*(avg_sentence_length+avg_num_of_complex_words*100)
    return gfi_score


if __name__ == "__main__":
    user_text = file_io.read_txt_file(r"..\data\neg_fre_text.txt")
    user_text = text_normalizer.normalize_text(user_text)
    # print(split_text_into_sentence_list(user_text))
    user_words = split_text_into_word_list(user_text)
    # print(f"evacuate - {count_en_word_syllables('evacuate')}")
    # sum_of_syllables = 0
    for user_word in user_words:
        print(f"{user_word} - {count_en_word_syllables(user_word)}")
    #     sum_of_syllables += count_en_word_syllables(user_word)
    # print(sum_of_syllables)
    # TODO:
    #   make another ways to find reading-ease of text
    #   add Flesch-Kincaid index
    #   add list from set of chars (don't know how to use for now)
    # print(f"For your text flesch reading-ease score = {find_ru_fre(user_text)}")
    # print(f"For your text flesch reading-ease score = {find_en_fre(user_text)}")
    # print(f"For your text Gunning fog index = {find_en_gfi(user_text)}")
    # print(f"Number of complex words = {count_en_complex_words(user_words)}, {len(user_words)}")
