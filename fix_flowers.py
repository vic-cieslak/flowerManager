import json 
kwiaty = Kwiat.objects.all()

for kwiat in kwiaty:
    kk = kwiat.kategorie_i_kolory 
    kk_json = json.loads(kk)  
    kwiat.kategorie_i_kolory = kk_json
    kwiat.save()
    print(kk_json)
    print(type(kk_json))