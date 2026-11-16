from orderflow.inventory import Warehouse, allocate_order

def test_duplicate_sku_lines_cannot_overreserve_stock():
    warehouse = Warehouse({"SKU-1": 5})

    items = [
        {"sku": "SKU-1", "quantity": 3},
        {"sku": "SKU-1", "quantity": 3},
    ]

    assert not allocate_order(warehouse, "ORD-OVER", items)
    assert warehouse.available["SKU-1"] == 5
    assert "ORD-OVER" not in warehouse.reserved


def test_repeated_allocation_for_same_order_is_idempotent():
    warehouse = Warehouse({"SKU-1": 5})
    items = [{"sku": "SKU-1", "quantity": 2}]

    assert allocate_order(warehouse, "ORD-1", items)
    assert allocate_order(warehouse, "ORD-1", items)

    assert warehouse.available["SKU-1"] == 3
    assert warehouse.reserved["ORD-1"] == {"SKU-1": 2}


def test_existing_order_reference_cannot_be_reused_for_different_items():
    warehouse = Warehouse({"SKU-1": 5, "SKU-2": 5})

    assert allocate_order(
        warehouse, "ORD-1",
        [{"sku": "SKU-1", "quantity": 2}]
    )

    assert not allocate_order(
        warehouse, "ORD-1",
        [{"sku": "SKU-2", "quantity": 2}]
    )

    assert warehouse.available == {"SKU-1": 3, "SKU-2": 5}
