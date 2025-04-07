from fastapi import FastAPI, Query
from supabase import create_client
import os
from dotenv import load_dotenv

app = FastAPI()

# Carregar variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def root():
    return {"message": "API funcionando!"}


@app.get("/api/houses")
def get_houses(
    min_price: float = Query(None),
    max_price: float = Query(None),
    min_age: int = Query(None),
    max_age: int = Query(None),
    structure_quality: int = Query(None),
    avno60plus: int = Query(None),
    limit: int = Query(500)
):
    data = []
    page = 0
    page_size = 1000  # Ajuste conforme necessário

    # Loop para buscar todas as páginas de registros
    while True:
        query = supabase.table("miami_housing").select("*").range(page * page_size, (page + 1) * page_size - 1)

        if min_price:
            query = query.gte("sale_prc", min_price)
        if max_price:
            query = query.lte("sale_prc", max_price)
        if min_age:
            query = query.gte("age", min_age)
        if max_age:
            query = query.lte("age", max_age)
        if structure_quality:
            query = query.eq("structure_quality", structure_quality)
        if avno60plus is not None:
            query = query.eq("avno60plus", avno60plus)

        response = query.execute().data

        if not response:
            break

        data.extend(response)
        page += 1

    return data


@app.get("/api/houses/price-stats")
def price_stats():
    data = []
    page = 0
    page_size = 1000

    while True:
        response = supabase.table("miami_housing").select(
            "sale_prc", "lnd_sqfoot", "tot_lvg_area", "structure_quality"
        ).range(page * page_size, (page + 1) * page_size - 1).execute().data

        if not response:
            break

        data.extend(response)
        page += 1

    prices = [d['sale_prc'] for d in data]
    land_area = [d['lnd_sqfoot'] for d in data]
    living_area = [d['tot_lvg_area'] for d in data]
    structure_quality = [d['structure_quality'] for d in data]

    price_avg = sum(prices) / len(prices) if prices else 0
    price_min = min(prices) if prices else 0
    price_max = max(prices) if prices else 0
    price_median = sorted(prices)[len(prices) // 2] if prices else 0
    price_stddev = (sum((x - price_avg) ** 2 for x in prices) / len(prices)) ** 0.5 if prices else 0
    price_iqr = sorted(prices)[int(0.75 * len(prices))] - sorted(prices)[int(0.25 * len(prices))] if prices else 0

    quality_price_avg = {}
    for quality in set(structure_quality):
        quality_prices = [p for p, q in zip(prices, structure_quality) if q == quality]
        if quality_prices:
            quality_price_avg[str(quality)] = sum(quality_prices) / len(quality_prices)

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
        "living_area_distribution": living_area
    }

    return stats


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

    monthly_data = {}

    for d in data:
        month = d['month_sold']
        price = d['sale_prc']

        if month not in monthly_data:
            monthly_data[month] = []

        monthly_data[month].append(price)

    result = []
    for month in sorted(monthly_data):
        prices = monthly_data[month]
        result.append({
            "month": month,
            "total_sales": len(prices),
            "average_price": sum(prices) / len(prices)
        })

    return result

@app.get("/api/houses/distance-impact")
def distance_impact():
    data = []
    page = 0
    page_size = 1000  # Ajuste conforme necessário

    # Loop para buscar todas as páginas de registros
    while True:
        # Busca paginada no Supabase
        response = supabase.table("miami_housing").select(
            "sale_prc", "ocean_dist", "hwy_dist", "avno60plus"
        ).range(page * page_size, (page + 1) * page_size - 1).execute().data

        # Verifica se a página está vazia (fim dos registros)
        if not response:
            break
        
        # Adiciona os registros obtidos
        data.extend(response)
        page += 1

    # Distância ao Oceano
    near_ocean = [d['sale_prc'] for d in data if d.get('ocean_dist', 0) <= 15000]
    far_ocean = [d['sale_prc'] for d in data if d.get('ocean_dist', 0) > 15000]

    # Distância à Rodovia
    near_hwy = [d['sale_prc'] for d in data if d.get('hwy_dist', 0) <= 5000]
    far_hwy = [d['sale_prc'] for d in data if d.get('hwy_dist', 0) > 5000]

    # Ruído Aéreo
    airport_noise = [d['sale_prc'] for d in data if d.get('avno60plus') == 1]
    no_airport_noise = [d['sale_prc'] for d in data if d.get('avno60plus') == 0]

    # Contagens
    count_near_ocean = len(near_ocean)
    count_near_hwy = len(near_hwy)
    count_airport_noise = len(airport_noise)

    return {
        "avg_price_near_ocean": sum(near_ocean) / len(near_ocean) if near_ocean else None,
        "avg_price_far_from_ocean": sum(far_ocean) / len(far_ocean) if far_ocean else None,
        "avg_price_near_highway": sum(near_hwy) / len(near_hwy) if near_hwy else None,
        "avg_price_far_from_highway": sum(far_hwy) / len(far_hwy) if far_hwy else None,
        "avg_price_airport_noise": sum(airport_noise) / len(airport_noise) if airport_noise else None,
        "avg_price_no_airport_noise": sum(no_airport_noise) / len(no_airport_noise) if no_airport_noise else None,
        "count_near_ocean": count_near_ocean,
        "count_near_highway": count_near_hwy,
        "count_airport_noise": count_airport_noise,
        "prices_near_ocean": near_ocean,
        "prices_far_ocean": far_ocean,
        "prices_near_highway": near_hwy,
        "prices_far_highway": far_hwy,
        "prices_airport_noise": airport_noise,
        "prices_no_airport_noise": no_airport_noise
    }
