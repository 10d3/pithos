import kuzu

def main():
    db = kuzu.Database("./pandora_db")
    conn = kuzu.Connection(db)

    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS Company(
            name STRING,
            ticker STRING,
            country STRING,
            PRIMARY KEY (name)
        )
    """)

    conn.execute("""
        CREATE NODE TABLE IF NOT EXISTS WeaponSystem(
            name STRING,
            category STRING,
            PRIMARY KEY (name)
        )
    """)

    conn.execute("""
        MERGE (c:Company {name: 'Lockheed Martin',
        ticker: 'LMT', country: 'USA'
        })
    """)

    conn.execute("""
        MERGE (
            c:WeaponSystem {
                name: "F35 Raptor",
                category: "Fighter Jet"
            }
        )
    """)

    conn.execute("""
        CREATE REL TABLE IF NOT EXISTS MANUFACTURES(
            FROM Company TO WeaponSystem
        )
    """)

    conn.execute("""
        MATCH (c: Company {name: 'Lockheed Martin'}),
            (w: WeaponSystem {name: 'F35 Raptor'})
        MERGE (c)-[:MANUFACTURES]->(w)
    """)

    result = conn.execute("MATCH (c:Company)-[MANUFACTURES]->(w:WeaponSystem) RETURN c.name, c.ticker, w.name")

    while result.has_next():
        print("Found in graph:", result.get_next())

    print("Kuzu connected successfully")


if __name__ == "__main__":
    main()
