import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv('/app/.env')

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def log(message):
    print(f"[LOG]: {message}")

def connect_to_supabase():
    try:
        log("Tentando conectar ao Supabase...")
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        log("Conectado ao Supabase com sucesso!")
        return supabase
    except Exception as e:
        log(f"Erro ao conectar ao Supabase: {e}")
        return None

def clean_data(file_path):
    try:
        log(f"Carregando dados do arquivo: {file_path}")
        df = pd.read_csv(file_path)
        log(f"Dados carregados: {df.shape[0]} registros")

        # RENOMEAR explicitamente as colunas para minúsculas
        df.columns = [
            'latitude', 'longitude', 'parcelno', 'sale_prc', 'lnd_sqfoot', 
            'tot_lvg_area', 'spec_feat_val', 'rail_dist', 'ocean_dist',
            'water_dist', 'cntr_dist', 'subcntr_di', 'hwy_dist', 'age',
            'avno60plus', 'month_sold', 'structure_quality'
        ]

        log("Colunas após padronização para minúsculas:")
        for col in df.columns:
            log(f" - {col}")

        # Remover duplicatas
        df = df.drop_duplicates(subset=['parcelno'], keep='first')
        log(f"Dados após remoção de duplicatas: {df.shape[0]} registros")

        return df
    except Exception as e:
        log(f"Erro ao limpar os dados: {e}")
        return None

def load_to_supabase(df, supabase):
    try:
        table_name = "miami_housing"
        log(f"Tentando carregar dados na tabela: {table_name}")
        data = df.to_dict(orient="records")
        response = supabase.table(table_name).upsert(data).execute()
        log("Dados carregados no Supabase com sucesso!")
        log(f"Resposta do Supabase: {response}")
    except Exception as e:
        log(f"Erro ao carregar no Supabase: {e}")

if __name__ == "__main__":
    file_path = '/app/miami-housing.csv'
    supabase = connect_to_supabase()

    if supabase:
        df = clean_data(file_path)
        if df is not None:
            load_to_supabase(df, supabase)
