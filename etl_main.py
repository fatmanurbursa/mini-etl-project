import os
#import google.cloud import stroage
#from io import BytesIO
import pandas as pd
import mysql.connector


#config area


#------google cloud--------
# bucket_name="mini-data-pipeline-bucket"
# credential_path="etl-service-account.json"

file_name="/Users/fatmanurbursa/Desktop/orders.csv"

mysql_host = os.getenv("MYSQL_HOST", "localhost")
mysql_user = os.getenv("MYSQL_USER", "root")
mysql_pass = os.getenv("MYSQL_PASS", "")
mysql_db   = os.getenv("MYSQL_DB", "etl_project")



def extract_from_gcp():
    ##-----google cloud------
    #os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=credential_path
    #client=storage.Client()
    #bucket=bucket.blob(file_name)
    #content=blob.download_as_bytes()
    #df=pd.read_csv(BytesIO(content))

    df=pd.read_csv(file_name)
    df["order_date"]=pd.to_datetime(df["order_date"])
    return df


#incremental control

def get_last_date():
    conn=mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_pass,
        database=mysql_db
    )

    cursor=conn.cursor()
    cursor.execute("SELECT MAX(order_date) FROM orders_processed")
    result=cursor.fetchone()[0]

    conn.close()
    return result if result else pd.to_datetime("1900-01-01")

#transform

def transform(df):
    df["quantity"]=df["quantity"].astype(float)
    df["price"]=df["price"].astype(float)
    df["category"]=df["category"].str.capitalize()
    return df

#load into mysql

def load_to_mysql(df):
    conn=mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_pass,
        database=mysql_db
    )

    cursor=conn.cursor()

    query="""
    INSERT INTO orders_processed 
    (order_id,category,customer_id,price,quantity,city,payment_method,order_date)
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """


    for _,row in df.iterrows():
        cursor.execute(query, (
            row["order_id"],
            row["category"],
            row["customer_id"],
            row["price"],
            row["quantity"],
            row["city"],
            row["payment_method"],
            row["order_date"]
        ))

    conn.commit()
    cursor.close()
    conn.close()



def main():
    print("Cloud extract başlıyor...")
    df_raw=extract_from_gcp()

    print("Son yüklenen tarihi sorguluyorum")
    last_date=get_last_date()

    print("incremental filtre uygulanıyor")
    df_inc=df_raw[df_raw["order_date"]>last_date]


    if df_inc.empty:
        print("Yeni veri yok. ETL durduruldu")
        return

    print(f"Yüklenecek yeni satır sayısı : {len(df_inc)}")

    print("Transform aşamasında")
    df_transformed=transform(df_inc)
    df_inc = df_inc.reset_index(drop=True)

    print("Mysqle yükleniyor")
    load_to_mysql(df_transformed)

    print("ETL başarıyla tamamlandı")


if __name__ == "__main__":
    main()
    
    
            




