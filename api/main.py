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
    query = supabase.table("miami_housing").select("*")

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

    response = query.limit(limit).execute()

    return response.data


@app.get("/api/houses/price-stats")
def price_stats():
    data = supabase.table("miami_housing").select("sale_prc", "lnd_sqfoot", "tot_lvg_area", "structure_quality").execute().data

    prices = [d['sale_prc'] for d in data]
    land_area = [d['lnd_sqfoot'] for d in data]
    living_area = [d['tot_lvg_area'] for d in data]

    stats = {
        "price_avg": sum(prices) / len(prices),
        "price_min": min(prices),
        "price_max": max(prices),
        "land_area_avg": sum(land_area) / len(land_area),
        "living_area_avg": sum(living_area) / len(living_area),
    }

    return stats


@app.get("/api/houses/distance-impact")
def distance_impact():
    data = supabase.table("miami_housing").select("sale_prc", "ocean_dist", "hwy_dist", "avno60plus").execute().data

    near_ocean = [d['sale_prc'] for d in data if d['ocean_dist'] <= 15000]
    far_ocean = [d['sale_prc'] for d in data if d['ocean_dist'] > 15000]

    near_hwy = [d['sale_prc'] for d in data if d['hwy_dist'] <= 5000]
    far_hwy = [d['sale_prc'] for d in data if d['hwy_dist'] > 5000]

    airport_noise = [d['sale_prc'] for d in data if d['avno60plus'] == 1]
    no_airport_noise = [d['sale_prc'] for d in data if d['avno60plus'] == 0]

    return {
        "avg_price_near_ocean": sum(near_ocean) / len(near_ocean) if near_ocean else None,
        "avg_price_far_from_ocean": sum(far_ocean) / len(far_ocean) if far_ocean else None,
        "avg_price_near_highway": sum(near_hwy) / len(near_hwy) if near_hwy else None,
        "avg_price_far_from_highway": sum(far_hwy) / len(far_hwy) if far_hwy else None,
        "avg_price_airport_noise": sum(airport_noise) / len(airport_noise) if airport_noise else None,
        "avg_price_no_airport_noise": sum(no_airport_noise) / len(no_airport_noise) if no_airport_noise else None
    }



@app.get("/api/houses/sales-time")
def sales_time():
    data = supabase.table("miami_housing").select("month_sold", "sale_prc").execute().data

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
