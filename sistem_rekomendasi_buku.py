# -*- coding: utf-8 -*-
"""sistem_rekomendasi_buku.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QEJ_9bGHFky5YnCGX5ig4AVt836O4ydc

# Proyek Pengembangan Sistem Rekomendasi Buku dengan Collaborative Filtering

Dibuat oleh Sulistyo Chandrianto

## Project Overview
Ilmu pengetahuan sangatlah penting bagi umat manusia. Dari ilmu pengetahuan kita dapat belajar banyak hal dari berbagai sisi kehidupan. Salah satu kunci meningkatkan kualitas hidup kita adalah mengerti akan ilmu pengetahuan tersebut sehingga kita perlu untuk belajar apa ilmu pengetahuan tersebut. Cara mudah untuk mengakses ilmu pengetahuan adalah dengan membaca buku. Dari buku kita dapat membaca tulisan-tulisan gagasan ilmu dari penulis dalam bentuk cerita naratif, cerita bergambar dan lainnya. Kita dapat membaca berbagai hal yang belum pernah kita mengerti sebelumnya.

Sering kita dengar bahwa buku membuka jendela wawasan kita namun sayangnya minat membaca buku di Indonesia sangat kecil. Di tingkat internasional, Indonesia memiliki indeks membaca sebesar 0,001 yang artinya setiap seribu orang hanya satu orang yang memiliki minat baca tinggi [[1](https://journal.unesa.ac.id/index.php/jpi/article/view/140)]. Hal ini berbeda jika dibandingkan dengan negara maju seperti Amerika yang memiliki indeks membaca sebesar 0,45 dan Singapura yang memiliki indeks baca 0,55. Terlihat negara maju memiliki masyrakat dengan minat baca yang tinggi sehingga penting sekali meningkatkan minta membaca ini di Indonesia.

Kesusahan mencari buku yang menarik untuk dibaca merupakan salah satu kendala seseorang untuk memulai membaca buku. Terdapat banyak jenis buku dengan banyak judul yang siap dibaca. Namun seringkali terlewat bigitu saja karena tidak adanya bantuan dalam pemilihan buku tersebut. Hal ini menyebabkan minat seseorang cepat hilang dan menyerah. Maka dari itu kita memerlukan sebuah sistem pendukung untuk mengatasi permasalahan ini.

Sistem pendukung yang bisa digunakan adalah sistem rekomendasi buku. Sistem rekomendasi buku merupakan sistem yang akan merekomendasikan buku sehingga seseorang dapat lebih mudah mendapatkan informasi tentang buku yang akan dibaca [[2](https://ejournal.akprind.ac.id/index.php/technoscientia/article/view/612)]. Sistem rekomendasi ini dibangun berdasarkan sejarah ulasan dari pembaca lainnya sehingga dapat memberikan judul-judul buku yang menarik untuk dibaca. Sistem rekemondasi buku ini diharapkan dapat memberikan bantuan kepada pembaca baru untuk lebih mudah dipertemukan dengan buku yang menarik minta bacanya. Pendekatan yang akan digunakan dalam pengembangan sistem rekemondasi buku adalah *collaborative filtering* yang memerlukan informasi sumber data dari pembaca lainnya.

## Tujuan Proyek
Tujuan dari proyek ini adalah sebagai berikut:

- Mengembangkan sistem rekomendasi buku yang dapat meningkatkan minat baca berdasarkan ulasan pembaca lainnya.
- Memilih metode *collaborative filtering* yang tepat dan akurat untuk pengembangan sistem rekomendasi buku ini.

## Project Startup

* Download library
"""

!pip install scikit-surprise

"""*   Import library"""

import pandas as pd
import numpy as np

from surprise import accuracy,SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import matplotlib.pyplot as plt

"""*   Load Dataset"""

books = pd.read_csv('/content/drive/MyDrive/dataset_book/Books.csv')
users = pd.read_csv('/content/drive/MyDrive/dataset_book/Users.csv')
ratings = pd.read_csv('/content/drive/MyDrive/dataset_book/Ratings.csv')

"""## Data Understanding

### Lihat Dataset
Melihat isi dataset dari data books, users dan ratings

* Data books
"""

books.head()

"""* Data user"""

users.head()

"""* Data rating"""

ratings.head()

"""### Eksplorasi Data

* Bentuk dari dataset
"""

print("Data books memiliki shape :" ,books.shape)
print("Data users memiliki shape :", users.shape)
print("Data ratings memiliki shape :", ratings.shape)

"""Dari bentuk dataset ditemukan informasi yaitu :
1. Data book memiliki 8 kolom dan 271,360 records
2. Data user memiliki 3 kolom dan 278,858 records
3. Data rating memiliki 3 kolom dan 1,149,780 records

* Info fitur Dataset
"""

books.info()

print('Check null value di data books')
books.isnull().sum()

"""Dari informasi dataset books tidak ditemukan fitur numerik"""

users.info()

print('Check null value di data users')
users.isnull().sum()

ratings.info()

print('Check null value di data ratings')
ratings.isnull().sum()

"""* Total record dataset dan relasi"""

n_uniq_book = len(books.ISBN.unique())
n_user = len(users["User-ID"].unique())
n_rating = len(ratings)
n_book_rating = len(ratings["ISBN"].unique())
n_user_rating = len(ratings["User-ID"].unique())

print("Jumlah data buku : ", n_uniq_book)
print("Jumlah data pembaca : ", n_user)
print("Jumlah data rating :", n_rating)
print ("Jumlah pembaca yang memberi rating :", n_user_rating)
print ("Jumlah buku yang diberi rating :", n_book_rating)

"""### Eksplorasi Data Univariate

#### Data books

Dilakukan explorasi data univariate terhadap variabel-variabel di dataset books. Variabel yang dipilih untuk dieksplorasi adalah variabel yang dianggap menggambarkan dataset books.
"""

def get_count_percentage(df):
  count_df = df.value_counts()
  percentage = df.value_counts(normalize=True) * 100
  return pd.DataFrame({'jumlah record':count_df, 'persentase':percentage.round(1)})

"""##### Variabel Year-Of-Publication"""

df_year = books["Year-Of-Publication"]
df_year_int = df_year[df_year.astype(str).str.isdigit() == True].astype(int)

df_year_pub_info = get_count_percentage(df_year_int)
print(df_year_pub_info)


df_year_words = df_year[~df_year.astype(str).str.isdigit() ]
print('Tahun yang memiliki nilai string adalah ', df_year_words.to_numpy())


print('Tahun yang lebih dari 2023 adalah ', df_year_int[df_year_int.gt(2023)].unique())

"""Dari value_count ditemukan informasi sebagai berikut:
* Terdapat tahun terbit yang lebih dari 2023 yaitu tahun terbit 2030,2050,2038,2026,2024,2037
* Terdapat record yang memiliki tahun terbit yang tidak valid yang berisi 'DK Publishing Inc' dan 'Gallimard'

Visualisasi jumlah record terhadap tahun terbit dapat dilihat dibawah ini
"""

year_min = df_year_int.min()
year_max = df_year_int.max()
n_steps = 500
year_ticks = np.arange(year_min, year_max + 1, n_steps)

ax = df_year_pub_info['jumlah record'].sort_index().plot(kind='bar')
ax.set_xticks(ax.get_xticks()[::5])

"""Dari grafik diatas terlihat bahwa tahun terbit buku didominasi nilai dengan rentang tahun 1968-2003. Sedangka untuk tahun terbit 0 menunjukkan buku tersebut tidak memiliki informasi tahun terbit.

##### Variabel Book-Author
"""

df_author = books["Book-Author"]

df_author_info = get_count_percentage(df_author)
print(df_author_info)

df_author_info['jumlah record'].head(10).plot(kind='barh', title='10 Nama Penulis Buku Terbanyak')

"""Dari value_count author dan grafik bar author didapatkan informasi untuk dataset ini adalah sebagai berikut:
* Terdapat 102,023 nama penulis buku
* Persentase penulis buku terbesar adalah 0.2 % sehingga dapat disimpulkan value dari Book-Author memiliki keragaman yang sangat banyak dan tidak didominasi oleh penulis buku tertentu
* 3 Penulis buku terbanyak adalah Agatha Christie, William Shakespeare dan Stephen King

##### Variabel Publisher
"""

df_publisher = books["Publisher"]

df_publisher_info = get_count_percentage(df_publisher)
print(df_publisher_info)

df_publisher_info['jumlah record'].head(10).plot(kind='barh', title='10 Nama Publisher Buku Terbanyak')

"""Dari value_count publisher dan grafik bar publisher didapatkan informasi untuk dataset ini adalah sebagai berikut:
* Terdapat 16,807 nama penerbit
* Persentase penerbit buku terbanyak adalah 2.8 % yaitu Harlequin selisih 1% dengan publisher peringkat kedua yaitu Silhouette
* 3 penerbit buku terbanyak adalah Harlequin, Silhouette dan Pocket

#### Data users
Tidak dilakukan eksplorasi data univariate untuk dataset users karena sistem rekomendasi tidak mempertimbangkan data umur dan demografi user

#### Data ratings

##### Variabel Book-Rating
"""

df_rating = ratings["Book-Rating"]

df_rating_info = get_count_percentage(df_rating)
print(df_rating_info)

df_rating_info['jumlah record'].sort_index().plot(kind='bar', title='Frekuensi jumlah rating')

"""Dari value_count rating dan plot bar frekuensi rating didapatkan informasi sebagai berikut:
* Jumlah pembaca yang belum memberikan penilaian ke buku (rating = 0) masih sangat banyak yaitu sebesar 62%
* Nilai rating yang sering muncul setelah rating 0 adalah rating 8

## Data Preprocessing

Pada tahap Data Preprocessing dilakukan 2 langkah yaitu :
* Penggabungan Data
* Hapus Variabel yang Tidak Digunakan

### Penggabungan Data
Dilakukan penggabungan data books dengan data ratings
"""

books.head()

ratings.head()

merged_book_df = ratings.merge(books, on='ISBN')
merged_book_df.head(5)

"""### Hapus Variabel Yang Tidak Digunakan
Menghapus variabel-variabel yang tidak digunakan di pengembangan proyek dengan motode collaborative filtering yaitu
* Image-URL-S
* Image-URL-M
* Image-URL-L
* Book-Title
* Book-Author
* Year-Of-Publication
* Publisher

"""

from sys import breakpointhook
column_to_drop = ['Image-URL-S','Image-URL-M','Image-URL-L','Book-Title','Book-Author','Year-Of-Publication','Publisher']
book_rating_df = merged_book_df.drop(column_to_drop, axis =1)
book_rating_df.head()

"""## Data Preparation
Pada tahap ini akan dilakukan langkah-langkah sebagai berikut:
* Mengatasi Missing Value
* Encoding Data
* Skala Ulang Variabel Book-Rating
* Pembagian Data Uji dan Data Latih

### Mengatasi Missing Value
"""

book_rating_df.isnull().sum()

"""Tidak ditemukan missing value di dataset

### Encoding Data
Dilakukan encoding ID untuk ISBN dan User-ID ke dalam indeks integer
"""

user_ids = book_rating_df['User-ID'].unique().tolist()
user_encoded = {x: i for i, x in enumerate(user_ids)}
user_to_user_encoded = {i: x for i, x in enumerate(user_ids)}

book_ids = book_rating_df['ISBN'].unique().tolist()
book_encoded = {x: i for i, x in enumerate(book_ids)}
book_to_book_encoded = {i: x for i, x in enumerate(book_ids)}

print('Encoded user-id :', dict(list(user_encoded.items())[0: 10]))
print('Encoded book-id (isbn) :', dict(list(book_encoded.items())[0: 10]))

"""Kemudian memetakan data hasil encode ke dataframe dengan menambahkan kolom baru yaitu kolom user_id dan isbn"""

book_rating_df['user_id'] = book_rating_df['User-ID'].map(user_encoded)
book_rating_df['isbn'] = book_rating_df['ISBN'].map(book_encoded)
book_rating_df.head()

"""### Skala Ulang Variabel Book-Rating
Dilakukan normalisai terhadap variabel Book-Rating yaitu merubah nilai rating menjadi nilai dengan batas skala 0 sampai 1 agar mudah dalam proses training

* Mengubah nilai Book-Rating menjadi float
"""

col_rating = 'Book-Rating'
book_rating_df[col_rating] = book_rating_df[col_rating].values.astype(np.float32)

"""* Mengambil nilai min dan max Book-Rating"""

min_rating = min(book_rating_df[col_rating])
max_rating = max(book_rating_df[col_rating])

"""* Menambahkan variabel baru di dataframe dengan nama rating"""

book_rating_df['rating'] = book_rating_df[col_rating].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
book_rating_df.head()

"""### Pembagian Data Latih dan Data Uji

Membagi data menjadi data uji dan data latih dengan perbandingan 80% data latih dan 20% data uji.

Pembagian data uji dan data latih ini akan dilakukan dengan 2 cara yang berbeda. Hal ini dikarenakan untuk teknik SVD pembagian data uji dan data latih menggunakan modul train_test_split dari library suprise. Berikut masing-masing cara pembagian data uji dan lati.

* Pembagian data uji dan latih untuk teknik SVD

> Di library Surprise terdapat class bernama Reader yang berfungsi untuk membaca file rating. Struktur file rating ini harus mengikuti struktur seperti dibawah ini


  ```
       user ; item ; rating ; [timestamp]
  ```


>  dengan nilai timestamp adalah optional.
 Di class [Reader](https://surprise.readthedocs.io/en/stable/reader.html?highlight=reader) juga terdapat parameter rating_scale yang berfungsi sebagai skala rating dengan default nilai (1,5). Di proyek ini rating_scale akan menggunakan (0,1)
"""

reader_svd = Reader(rating_scale=(0,1))
data_svd = Dataset.load_from_df(book_rating_df[['user_id', 'isbn', 'rating']], reader_svd)
trainset_svd, testset_svd = train_test_split(data_svd, test_size=0.2)

"""* Pembagian data uji dan latih untuk teknik Neural Network"""

x = book_rating_df[['user_id','isbn']].values
y = book_rating_df['rating'].values

n_train = 0.8
train_indices = int(n_train * book_rating_df.shape[0])
x_train, x_val, y_train, y_val = (
    x[:train_indices],
    x[train_indices:],
    y[:train_indices],
    y[train_indices:]
)

print(x, y)

"""## Modelling

Dalam proyek ini sistem rekomendasi dikembangkan dengan menggunakan metode collaborative filtering. Dari metode ini digunakan dua teknik pendekatan yaitu
* Collaborative filtering dengan teknik SVD
* Collaborative filtering dengan teknik Neural Network

> Untuk keperluan uji coba model dibuat data test buku yang belum dibaca oleh user sesuai dengan nilai User-ID
"""

test_user_id = 276729
read_books = ratings[ratings['User-ID'] == test_user_id]
unread_books =  ratings[~ratings['ISBN'].isin(read_books.ISBN.values)]['ISBN']

"""### Collaborative Filtering dengan Teknik SVD

SVD (Singular Value Decomposition) merupakan teknik aljabar linear yang digunakan untuk mengurangi dimensi dari matrix. Dengan SVD kita dapat menemukan relasi antar anggota di dalam matrix

Library yang digunakan untuk mengimplementasikan SVD adalah Suprise
"""

svd = SVD()

svd.fit(trainset_svd)

"""Hasil prediksi model teknik SVD untuk 8 buku yang disarankan"""

df_svd_predict = unread_books.to_frame(name='ISBN')
df_svd_predict = df_svd_predict.merge(books[['ISBN','Book-Title','Book-Author']], left_on='ISBN', right_on='ISBN', how='left')
df_svd_predict['prediction_rate'] = unread_books.apply(lambda x: svd.predict(test_user_id, x).est)

n_top = 8
df_svd_predict.sort_values(by='prediction_rate',ascending=False).head(n_top)

"""### Collaborative Filtering dengan Teknik Neural Network

Collaborative filtering dengan teknik Neural Network ini terinspirasi dari siturs [Keras](https://keras.io/examples/structured_data/collaborative_filtering_movielens/) yang menggunakan class RecommenderNet.

* Pertama buat class RecommenderNet dengan keras Model class
  Class ini akan menghitung match score antara user dan book menggunakan dot product kemudian hasil ini ditambahkan dengan bias user dan bias book. Terakhir nilai match score di skala ulang menjadi 0 sampai 1 menggunakan sigmoid activation
"""

class RecommenderNet(tf.keras.Model):

  def __init__(self, num_users, num_books, embedding_size, **kwargs):
    super(RecommenderNet, self).__init__(**kwargs)
    self.num_users = num_users
    self.num_books = num_books
    self.embedding_size = embedding_size
    self.user_embedding = layers.Embedding( # layer embedding user
        num_users,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.user_bias = layers.Embedding(num_users, 1) # layer embedding user bias
    self.book_embedding = layers.Embedding( # layer embeddings book
        num_books,
        embedding_size,
        embeddings_initializer = 'he_normal',
        embeddings_regularizer = keras.regularizers.l2(1e-6)
    )
    self.book_bias = layers.Embedding(num_books, 1) # layer embedding book bias

  def call(self, inputs):
    user_vector = self.user_embedding(inputs[:,0]) # memanggil layer embedding 1
    user_bias = self.user_bias(inputs[:, 0]) # memanggil layer embedding 2
    book_vector = self.book_embedding(inputs[:, 1]) # memanggil layer embedding 3
    book_bias = self.book_bias(inputs[:, 1]) # memanggil layer embedding 4

    dot_user_resto = tf.tensordot(user_vector, book_vector, 2)

    x = dot_user_resto + user_bias + book_bias

    return tf.nn.sigmoid(x) # activation sigmoid

"""* Buat model
  Membuat model menggunakan BinaryCrossentropy untuk hitung loss function, Adam (Adaptive Momment Estimation) untuk optimizer dan RMSE sebagai metriks evaluasi
"""

embedding_size = 50
num_users = len(book_rating_df['user_id'])
num_books = len(book_rating_df['isbn'])

model_nn = RecommenderNet(num_users, num_books, embedding_size)
model_nn.compile(
    loss=tf.keras.losses.BinaryCrossentropy(),
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    metrics=[tf.keras.metrics.RootMeanSquaredError()]
)

"""Hasil prediksi model teknik Neural Network untuk 8 buku yang disarankan"""

unread_isbns = list(set(unread_books).intersection(set(book_encoded.keys())))
unread_isbns_encode = [[(book_encoded.get(x))] for x in unread_isbns]

user_encoder = user_encoded.get(test_user_id)
user_book_array =  np.hstack(([[user_encoder]] * len(unread_isbns_encode), unread_isbns_encode))

pred_ratings = model_nn.predict(user_book_array).flatten()

top_ratings_indices = pred_ratings.argsort()[-n_top:][::-1]
recommended_book_isbns = [book_to_book_encoded.get(unread_isbns_encode[x][0]) for x in top_ratings_indices]
df_nn_predict = books[books['ISBN'].isin(recommended_book_isbns)]
df_nn_predict[['ISBN','Book-Title','Book-Author']]

"""## Evaluation

Evaluasi model menggunakan metriks RMSE (Root Mean Square Error)
"""

rmse = pd.DataFrame(columns=['test'], index=['SVD','NeuralNetwork'])

"""* Evaluasi collaborative filtering untuk teknik SVD


> Evaluasi menggunakan modul accuracy dari library Surprise


"""

predictions = svd.test(testset_svd)
rmse.loc['SVD','test'] = accuracy.rmse(predictions)

"""* Evaluasi collaborative filtering untuk teknik Neural Network"""

history = model_nn.fit(
    x = x_train,
    y = y_train,
    batch_size = 500,
    epochs = 8,
    validation_data = (x_val, y_val)
)

plt.plot(history.history['root_mean_squared_error'])
plt.plot(history.history['val_root_mean_squared_error'])
plt.title('model_metrics')
plt.ylabel('root_mean_squared_error')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

"""Mengambil nilai RMSE terkahir dari val_root_mean_squared_error"""

rmse.loc['NeuralNetwork','test'] = history.history['val_root_mean_squared_error'][-1]

rmse

"""Dilihat dari tabel diatas terlihat bahwa nilai RMSE dengan menggunakan teknik NeuralNetwork lebih kecil. Meskipun hanya memiliki selisih sedikit tetapi di teknik Neural Network masih dapat di tingkatkan lagi dengan mengatur hyperparameter yang lebih baik.

Sehingga teknik Neural Network untuk metode collaborative filtering dipilih sebagai algoritma sistem rekomendasi buku.

## Conclusion

Sistem rekomendasi buku sudah berhasil dibuat dengan metode collaborative filtering dengan teknik Neural Network. Pemilihan teknik Neural Network dipilih berdasarkan parameter RMSE yang lebih kecil.

Meskipun demikian proyek ini kedepannya masih perlu perbaikan dari sisi dataset dan hyperparameter untuk teknik Neural Network.
"""