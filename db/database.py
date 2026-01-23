import psycopg2

conn = psycopg2.connect(
    dbname="trade_signals",
    user="signals_user",
    password="signals_pass",
    host="localhost",
    port="5432"
)

def store_signal(signal):
    if signal.get("signal_score", 0) <= 0:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO signal_history (symbol, score, reasons)
            VALUES (%s, %s, %s)
            """,
            (
                signal["symbol"],
                signal["signal_score"],
                ",".join(signal.get("reasons", []))
            )
        )
        conn.commit()
        cur.close()

    except Exception as e:
        # very importantt if there is some error while taking the input
        conn.rollback()
        print("DB ERROR:", e)
