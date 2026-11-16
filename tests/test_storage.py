from orderflow.storage import connect_database, find_orders_by_email, save_order


def test_storage_roundtrip():
    with connect_database() as conn:
        save_order(conn, "student@example.test", 500)
        assert len(find_orders_by_email(conn, "student@example.test")) == 1

def test_storage_search_treats_input_as_data_not_sql():
    with connect_database() as conn:
        save_order(conn, "student@example.test", 500)

        assert find_orders_by_email(conn, "' OR 1=1 --") == []