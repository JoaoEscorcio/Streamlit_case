from fastapi import FastAPI, Query
from supabase import create_client
import os
from dotenv import load_dotenv

# Instância principal da aplicação FastAPI
app = FastAPI()

# ---------------------------
# CONFIGURAÇÃO DO SUPABASE
# ---------------------------
# Carrega variáveis de ambiente do arquivo .env (URL e KEY do Supabase)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------
# ROTA DE TESTE
# ---------------------------
@app.get("/")
def root():
    return {"message": "API funcionando!"}

# ---------------------------
# ROTA: /api/houses
# Lista de imóveis com filtros dinâmicos
# ---------------------------
@app.get("/api/houses")
def get_houses(
    min_price: float = Query(None),
    max_price: float = Query(None),
    min_age: int = Query(None),
    max_age: int = Query(None),
    min_area: int = Query(None),
    max_area: int = Query(None),
    structure_quality: int = Query(None),
    avno60plus: int = Query(None),
    max_ocean_dist: int = Query(None),     
    max_hwy_dist: int = Query(None),       
    limit: int = Query(500)
):
    data = []
    page = 0
    page_size = 1000

    # Paginação para buscar todos os registros
    while True:
        query = supabase.table("miami_housing").select("*").range(page * page_size, (page + 1) * page_size - 1)

        # Aplicação dos filtros, se fornecidos
        if min_price:
            query = query.gte("sale_prc", min_price)
        if max_price:
            query = query.lte("sale_prc", max_price)
        if min_age:
            query = query.gte("age", min_age)
        if max_age:
            query = query.lte("age", max_age)
        if min_area:
            query = query.gte("tot_lvg_area", min_area)
        if max_area:
            query = query.lte("tot_lvg_area", max_area)
        if structure_quality:
            query = query.eq("structure_quality", structure_quality)
        if avno60plus is not None:
            query = query.eq("avno60plus", avno60plus)
        if max_ocean_dist is not None:
            query = query.lte("ocean_dist", max_ocean_dist)
        if max_hwy_dist is not None:
            query = query.lte("hwy_dist", max_hwy_dist)

        # Executa a consulta paginada
        response = query.execute().data
        if not response:
            break

        data.extend(response)
        page += 1

    return data

# ---------------------------
# ROTA: /api/houses/price-stats
# Estatísticas gerais de preço e clusterização
# ---------------------------
@app.get("/api/houses/price-stats")
def price_stats():
    data = []
    page = 0
    page_size = 1000

    # Paginação da tabela
    while True:
        response = supabase.table("miami_housing").select(
            "sale_prc", "lnd_sqfoot", "tot_lvg_area", "structure_quality", "latitude", "longitude"
        ).range(page * page_size, (page + 1) * page_size - 1).execute().data

        if not response:
            break

        data.extend(response)
        page += 1

    # Coleta e validação dos campos principais
    prices = [d['sale_prc'] for d in data if 'sale_prc' in d]
    land_area = [d['lnd_sqfoot'] for d in data if 'lnd_sqfoot' in d]
    living_area = [d['tot_lvg_area'] for d in data if 'tot_lvg_area' in d]
    structure_quality = [d['structure_quality'] for d in data if 'structure_quality' in d]

    # Estatísticas descritivas de preço
    price_avg = sum(prices) / len(prices) if prices else 0
    price_min = min(prices) if prices else 0
    price_max = max(prices) if prices else 0
    price_median = sorted(prices)[len(prices) // 2] if prices else 0
    price_stddev = (sum((x - price_avg) ** 2 for x in prices) / len(prices)) ** 0.5 if prices else 0
    price_iqr = sorted(prices)[int(0.75 * len(prices))] - sorted(prices)[int(0.25 * len(prices))] if prices else 0

    # Preço médio por qualidade da estrutura
    quality_price_avg = {}
    for quality in set(structure_quality):
        quality_prices = [p for p, q in zip(prices, structure_quality) if q == quality]
        if quality_prices:
            quality_price_avg[str(quality)] = sum(quality_prices) / len(quality_prices)

    # Clusterização simples por faixas de preço (baixo, médio, alto)
    q1 = sorted(prices)[int(len(prices) * 0.33)]
    q2 = sorted(prices)[int(len(prices) * 0.66)]

    price_cluster = []
    for d in data:
        if all(k in d for k in ["latitude", "longitude", "sale_prc"]):
            sale = d["sale_prc"]
            range_label = "Low" if sale <= q1 else "Medium" if sale <= q2 else "High"
            price_cluster.append({
                "latitude": d["latitude"],
                "longitude": d["longitude"],
                "sale_prc": sale,
                "Price Range": range_label
            })


    # Resultado final retornado à API
    stats = {
        "price_avg": price_avg,
        "price_min": price_min,
        "price_max": price_max,
        "price_median": price_median,
        "price_stddev": price_stddev,
        "price_iqr": price_iqr,
        "land_area_avg": sum(land_area) / len(land_area) if land_area else 0,
        "living_area_avg": sum(living_area) / len(living_area) if living_area else 0,
        "quality_price_avg": quality_price_avg,
        "price_distribution": prices,
        "living_area_distribution": living_area,
        "price_cluster": price_cluster
    }

    return stats

# ---------------------------
# ROTA: /api/houses/sales-time
# Estatísticas mensais de venda
# ---------------------------
@app.get("/api/houses/sales-time")
def sales_time():
    data = []
    page = 0
    page_size = 1000

    while True:
        response = supabase.table("miami_housing").select("month_sold", "sale_prc").range(
            page * page_size, (page + 1) * page_size - 1).execute().data

        if not response:
            break

        data.extend(response)
        page += 1

    # Agrupamento dos preços por mês
    monthly_data = {}
    for d in data:
        month = d['month_sold']
        price = d['sale_prc']
        monthly_data.setdefault(month, []).append(price)

    # Constrói resposta com volume de vendas e preço médio
    result = []
    for month in sorted(monthly_data):
        prices = monthly_data[month]
        result.append({
            "month": month,
            "total_sales": len(prices),
            "average_price": sum(prices) / len(prices)
        })

    return result

# ---------------------------
# ROTA: /api/houses/distance-impact
# Analisa impacto de distâncias e ruído no preço
# ---------------------------
@app.get("/api/houses/distance-impact")
def distance_impact():
    data = []
    page = 0
    page_size = 1000

    while True:
        response = supabase.table("miami_housing").select(
            "sale_prc", "ocean_dist", "hwy_dist", "avno60plus"
        ).range(page * page_size, (page + 1) * page_size - 1).execute().data

        if not response:
            break
        data.extend(response)
        page += 1

    # Inicializa agrupamentos por categoria
    near_ocean, far_ocean = [], []
    near_hwy, far_hwy = [], []
    airport_noise, no_airport_noise = [], []

    dist_ocean, dist_ocean_price = [], []
    dist_hwy, dist_hwy_price = [], []

    # Classificação das distâncias e ruído
    for d in data:
        price = d.get("sale_prc")
        ocean_dist = d.get("ocean_dist", 0)
        hwy_dist = d.get("hwy_dist", 0)
        ruido = d.get("avno60plus")

        if price is None:
            continue

        if ocean_dist <= 15000:
            near_ocean.append(price)
        else:
            far_ocean.append(price)

        if hwy_dist <= 5000:
            near_hwy.append(price)
        else:
            far_hwy.append(price)

        if ruido == 1:
            airport_noise.append(price)
        elif ruido == 0:
            no_airport_noise.append(price)

        dist_ocean.append(ocean_dist)
        dist_ocean_price.append(price)
        dist_hwy.append(hwy_dist)
        dist_hwy_price.append(price)

    return {
        "avg_price_near_ocean": sum(near_ocean) / len(near_ocean) if near_ocean else None,
        "avg_price_far_from_ocean": sum(far_ocean) / len(far_ocean) if far_ocean else None,
        "avg_price_near_highway": sum(near_hwy) / len(near_hwy) if near_hwy else None,
        "avg_price_far_from_highway": sum(far_hwy) / len(far_hwy) if far_hwy else None,
        "avg_price_airport_noise": sum(airport_noise) / len(airport_noise) if airport_noise else None,
        "avg_price_no_airport_noise": sum(no_airport_noise) / len(no_airport_noise) if no_airport_noise else None,
        "count_near_ocean": len(near_ocean),
        "count_near_highway": len(near_hwy),
        "count_airport_noise": len(airport_noise),
        "prices_near_ocean": near_ocean,
        "prices_far_ocean": far_ocean,
        "prices_near_highway": near_hwy,
        "prices_far_highway": far_hwy,
        "prices_airport_noise": airport_noise,
        "prices_no_airport_noise": no_airport_noise,
        "dist_ocean": dist_ocean,
        "dist_ocean_price": dist_ocean_price,
        "dist_hwy": dist_hwy,
        "dist_hwy_price": dist_hwy_price
    }

# ---------------------------
# ROTA: /api/houses/filters-range
# Gera os limites dos filtros com base nos dados reais
# ---------------------------
@app.get("/api/houses/filters-range")
def get_filters_range():
    response = supabase.table("miami_housing").select(
        "sale_prc", "age", "tot_lvg_area", "structure_quality"
    ).limit(10000).execute()

    data = response.data

    if not data:
        return {
            "price_min": 50000,
            "price_max": 3000000,
            "age_min": 0,
            "age_max": 100,
            "area_min": 500,
            "area_max": 5000,
            "qualities": list(range(1, 10)),
        }

    prices = [d["sale_prc"] for d in data if d.get("sale_prc") is not None]
    ages = [d["age"] for d in data if d.get("age") is not None]
    areas = [d["tot_lvg_area"] for d in data if d.get("tot_lvg_area") is not None]
    qualities = sorted(set(d["structure_quality"] for d in data if d.get("structure_quality") is not None))

    return {
        "price_min": int(min(prices)) if prices else 50000,
        "price_max": int(max(prices)) if prices else 3000000,
        "age_min": int(min(ages)) if ages else 0,
        "age_max": int(max(ages)) if ages else 100,
        "area_min": int(min(areas)) if areas else 500,
        "area_max": int(max(areas)) if areas else 5000,
        "qualities": qualities if qualities else list(range(1, 10)),
    }
