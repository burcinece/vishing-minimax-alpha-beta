# vishing-minimax-alpha-beta

DOSYA LISTESI
-------------
solution_code.ipynb    : Calisan notebook (tum analiz, metrik ve grafik uretimi)
raw_llm_solution.py     : LLM'den alinan ham kod (3 hata icerir)
fixed_solution.py       : Ogrenci tarafindan duzeltilmis kod
results.csv             : Tum metrikler
llm_error_log.xlsx      : LLM hata kayit formu (3 hata, etki ve duzeltme aciklamali)
readme.txt               : Bu dosya

GEREKSINIMLER
-------------
Python 3.9 veya uzeri
Gerekli paketler: pandas, matplotlib, openpyxl (notebook ve yardimci scriptler icin)

kurulum:
    pip install pandas matplotlib openpyxl

CALISTIRMA SIRASI
------------------
1) Ham (hatali) kodu tek basina calistirmak icin:
       python3 raw_llm_solution.py

2) Duzeltilmis kodu tek basina calistirmak icin:
       python3 fixed_solution.py

   Her iki komut da baslangic durumundan alpha-beta ile secilen ilk eylemi ve
   ziyaret edilen dugum sayisini ekrana yazdirir.

3) Tum analizi (heuristik karsilastirmasi, dugum sayisi karsilastirmasi,
   BUG-1/BUG-2/BUG-3 etkisi, somuru senaryosu, results.csv okuma) adim adim
   gormek icin solution_code.ipynb dosyasini Jupyter Notebook veya
   JupyterLab ile acin ve hucreleri sirasiyla calistirin:
       jupyter notebook solution_code.ipynb

   Notebook, raw_llm_solution.py ve fixed_solution.py dosyalarini modul
   olarak ice aktardigi icin bu iki dosyanin notebook ile ayni klasorde
   olmasi gerekir.


4) results.csv, tum sayisal metrikleri (heuristik karsilastirmasi, BUG-2 ve
   BUG-3 etkisi, dugum sayisi karsilastirmasi, somuru senaryosu adimlari)
   tek bir tabloda toplar; Excel veya pandas ile acilabilir.

6) llm_error_log.xlsx, raw_llm_solution.py icinde tespit edilen uc hatanin
   (BUG-1, BUG-2, BUG-3) konumunu, aciklamasini, sayisal etkisini, onem
   derecesini ve fixed_solution.py icinde uygulanan duzeltmeyi listeler.

NOT
---
raw_llm_solution.py ve fixed_solution.py ayni fonksiyon isimlerini
(baslangic_durumu, saldirgan_uygula, savunucu_uygula, terminal_kontrol,
heuristik, minimax, alpha_beta) kullanir; bu nedenle ikisi de ayni anda
"import raw_llm_solution as ham" / "import fixed_solution as duzeltilmis"
seklinde takma isimle ice aktarilmalidir (solution_code.ipynb icinde bu
sekilde yapilmistir).
