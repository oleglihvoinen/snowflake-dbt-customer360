import os
import snowflake.connector

class CustomerRepository:
    def _connect(self):
        return snowflake.connector.connect(
            account=os.environ["SNOWFLAKE_ACCOUNT"],
            user=os.environ["SNOWFLAKE_USER"],
            password=os.environ["SNOWFLAKE_PASSWORD"],
            warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
            database="CUSTOMER360",
            schema="ANALYTICS",
        )

    def get_customer(self, customer_key: str):
        with self._connect() as con:
            cur = con.cursor()
            cur.execute(
                """select customer_key, customer_name, email, phone, country_code,
                          surviving_source, updated_at
                   from dim_customer where customer_key = %s""",
                (customer_key,),
            )
            row = cur.fetchone()
            if not row:
                return None
            cols = [c[0].lower() for c in cur.description]
            return dict(zip(cols, row))

    def search(self, email=None, limit=50):
        sql = """select customer_key, customer_name, email, country_code, surviving_source
                 from dim_customer"""
        params = []
        if email:
            sql += " where lower(email) = lower(%s)"
            params.append(email)
        sql += " order by customer_name limit %s"
        params.append(limit)
        with self._connect() as con:
            cur = con.cursor()
            cur.execute(sql, tuple(params))
            cols = [c[0].lower() for c in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

    def quality(self, customer_key: str):
        customer = self.get_customer(customer_key)
        if not customer:
            return {"customer_key": customer_key, "status": "not_found"}
        checks = {
            "email_present": bool(customer.get("email")),
            "country_present": bool(customer.get("country_code")),
            "source_present": bool(customer.get("surviving_source")),
        }
        return {"customer_key": customer_key, "passed": all(checks.values()), "checks": checks}
