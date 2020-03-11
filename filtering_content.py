import json
import googletrans

def main():
    with open('all.json', 'r') as fd:
        all_c = json.load(fd)

    domains = { item['name'] : item['alpha2Code'] for item in all_c}
    with open('domains.json', 'w') as fd:
        fd.write(json.dumps(domains, indent=4, ensure_ascii=False))

    with open('raw_data.json', 'r') as fd:
        data = json.load(fd)
    

    newd = {}
    bad = []
    gs = googletrans.Translator()
    
    for country in data:
        try:
            dom = domains[country]
        except:
            bad.append(country)
            dom = country
        newd[dom] = {}

        try:
            newd[dom]['name'] = data[country]['Flag bearer'].strip()
        except:
            bad.append(country)
        try:
            newd[dom]['gender'] = data[country]['Sex'].strip().lower()
        except:
            newd[dom]['gender'] = ''
        try:
            translation = gs.translate(data[country]['Sport\n'].strip(), 'es', 'en')
            newd[dom]['sport'] = translation.text
        except:
            try:
                translation = gs.translate(data[country]['Sport'].strip(), 'es', 'en')
                newd[dom]['sport'] = translation.text
            except:
                bad.append(country)
        newd[dom]['colective'] = False
        newd[dom]['role'] = 'Deportista'
        newd[dom]['best_result'] = 'Participante'


    final_dic = {}
    final_dic['1968'] = newd
    with open('flag-bearers.json', 'w') as fd:
        fd.write(json.dumps(final_dic, indent=4, ensure_ascii=False))

    with open('bad.json', 'w') as fd:
        fd.write(json.dumps(bad, indent=4, ensure_ascii=False))



if __name__ == "__main__":
    main()