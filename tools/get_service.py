# Tools/

import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_engine(DB_URL)


def get_service(location: str, filter_tags: str = None):
    """
    location: tên địa điểm (giữ nguyên dấu)
    filter_tags: từ khóa dịch vụ (vd: lặn biển, cano, tour...) hoặc None
    """

    with engine.connect() as conn:

        # 1️⃣ Lấy destination_id từ bảng destination
        dest_query = text("""
            SELECT id
            FROM destination
            WHERE name ILIKE :location
            LIMIT 1
        """)

        dest_result = conn.execute(dest_query, {
            "location": f"%{location}%"
        }).fetchone()

        if not dest_result:
            return {
                "status": "not_found",
                "message": f"Không tìm thấy địa điểm '{location}'."
            }

        destination_id = dest_result[0]

        # 2️⃣ Lấy dịch vụ theo destination_id
        if filter_tags:
            service_query = text("""
                SELECT name, description, price, type
                FROM service
                WHERE destination_id = :destination_id
                AND (
                    name ILIKE :tag OR
                    description ILIKE :tag OR
                    type ILIKE :tag
                )
            """)

            services = conn.execute(service_query, {
                "destination_id": destination_id,
                "tag": f"%{filter_tags}%"
            }).fetchall()

        else:
            service_query = text("""
                SELECT name, description, price, type
                FROM service
                WHERE destination_id = :destination_id
            """)

            services = conn.execute(service_query, {
                "destination_id": destination_id
            }).fetchall()

        if not services:
            return {
                "status": "empty",
                "message": "Không tìm thấy dịch vụ phù hợp."
            }

        result = []
        for s in services:
            result.append({
                "name": s[0],
                "description": s[1],
                "price": s[2],
                "type": s[3]
            })

        return {
            "status": "success",
            "location": location,
            "services": result
        }