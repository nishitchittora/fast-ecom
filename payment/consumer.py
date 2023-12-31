from main import redis, Order
import time

key = "refund_order"
group = "payment-group"

try:
    redis.xgroup_create(key, group)
except Exception as e:
    print(e)
    print("Group already exists!")


while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)

        print(results)
        if results != []:
            for r in results:
                obj = r[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()
    except Exception as e:
        print(str(e))

    time.sleep(1)
