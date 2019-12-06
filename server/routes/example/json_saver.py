from server.routes.complexity_way import ComplexityWay


with open('data.test', 'w') as out_file:
    complexity_way = ComplexityWay.load_complexity_way_from_json('floor_2.png')
