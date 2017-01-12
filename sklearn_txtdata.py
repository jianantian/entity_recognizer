from sklearn.feature_extraction.text import CountVectorizer
import os
path = 'E:/病例特点_2'
file_list = [open(os.path.join(path, name), 'r', encoding='utf8').read()
             for name in os.listdir(path)]
word_counter = CountVectorizer(analyzer='char')
x_train_counts = word_counter.fit_transform(file_list)
print(word_counter.get_feature_names())
