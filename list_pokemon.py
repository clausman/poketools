from pgoapi import PGoApi

def get_api(username, password, service):
    api = PGoApi()
    api.set_position(42.3598142, -71.0647737, 0.0)
    api.login(service, username, password)
    return api

def get_pokemon(api):
    resp = api.get_inventory()

    pd = [p['inventory_item_data']['pokemon_data'] for p in resp['responses']['GET_INVENTORY']['inventory_delta']['inventory_items'] if 'pokemon_data' in p['inventory_item_data']]
    pd = [p for p in pd if 'pokemon_id' in p]
    for p in pd:
        p['individual_attack'] = p.get('individual_attack', 0)
        p['individual_defense'] = p.get('individual_defense', 0)
        p['individual_stamina'] = p.get('individual_stamina', 0)
        p['perfection'] = (p['individual_attack']+p['individual_defense']+p['individual_stamina'])/(15.0*3)

    return pd

def to_s(poke):
    return "id=%(pokemon_id)s\tcp=%(cp)s\tper=%(perfection)f\tia=%(individual_attack)s\tid=%(individual_defense)s\tis=%(individual_stamina)s" % poke
        

def main(args):
    api = get_api(args.username, args.password, args.service)
    pokes = get_pokemon(api)

    pokes = [p for p in pokes if p['perfection'] >= args.threshold ]
    if args.ids:
        pokes = [p for p in pokes if p['pokemon_id'] in args.ids]

    pokes.sort(key=lambda p: p[args.sort], reverse=True)

    print "\n".join([to_s(p) for p in pokes])


if __name__ == "__main__":
    from argparse import ArgumentParser    
    parser = ArgumentParser(description='list your pokemon')
    parser.add_argument('username', help='account username')
    parser.add_argument('password', help='account password')
    parser.add_argument('ids', metavar='ID', type=int, nargs='*', help='filter to only these pokemon ids')
    parser.add_argument('--service', help='authorization service', default='ptc', choices=['ptc', 'google'])
    parser.add_argument('--threshold', help='only show pokemon with pefection greather than threshold', default=0.0, type=float)
    parser.add_argument('--sort', help='sort the results', default='creation_time_ms', choices=['creation_time_ms', 'perfection', 'cp', 'pokemon_id'])
    args = parser.parse_args()
    main(args)
