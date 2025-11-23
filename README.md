## Mini Cloud Data Pipeline Project (Incremental ETL)

Bu proje, Python + Airflow + MySQL kullanarak mini bir ETL pipeline oluşturur. Google Cloud bağlantısı yorum satırlarında örnek olarak gösterilmiştir; proje local ortamda çalışmaktadır.

## Proje Dosya Yapısı

  etl_main.py → Local ETL (Cloud bağlantısı yorum satırında)

  cloud_etl_dag.py → Airflow DAG

  orders.csv → Raw data

  dataset_generator.py → Sample CSV oluşturucu

  README.md → Dokümantasyon

## Kullanılan Teknolojiler

  Python 3.11, Pandas

  MySQL (Processed Zone)

  Airflow (local)

  Incremental ETL mantığı (MAX(order_date))

  Google Cloud Storage (yorum satırlarında örnek)

## Pipeline Akışı 

  orders.csv okunur

  Airflow DAG çalışır (etl_main.py tetiklenir)

 ## ETL süreci:

  Daha önce işlenmiş son tarihi bulur

  Yeni satırları seçer (incremental load)

  Transform 

  MySQL’e yükler

  Processed Zone güncellenir
  
  ## Incremental ETL Mantığı

  last_date = cursor.execute("SELECT MAX(order_date) FROM orders_processed;")
  df_inc = df_raw[df_raw["order_date"] > last_date]

 ## Cloud Kullanımı (Yorum Satırları)
   from google.cloud import storage
   client = storage.Client()
   bucket = client.bucket(bucket_name)
   blob = bucket.blob(file_name)
   content = blob.download_as_bytes()
   df = pd.read_csv(BytesIO(content))

  ## Airflow DAG
     run_cloud_etl = PythonOperator(
       task_id="run_cloud_etl",
       python_callable=run_etl
    )
# schedule: @daily
