#!/usr/bin/env python3
# Copyright 2024 - Samuele Mancuso (https://github.com/AllWorkNoPlay-95)
# This utility creates a nav structure to use with Max Mega menu starting from product categories
# GPL-3.0 License
import copy
import os
import json
import argparse
from pprint import pprint

# Globals
main_menu_id = "megacategories"
menu_items_cache = []
parents_to_put_in_other = []
args = []
max_order_position = 999990
custom_parents = [  # Parent title: Child slug # TODO: load from external file for modularity
    {
        "name": "Altro",
        "custom_order": max_order_position + 1,
        "children_slugs": [
            "macchine-per-lufficio",
            "catering",
            "sicurezza-e-magazzino",
            "pulizia-e-igiene",
            "elettronica-e-informatica",
            "espositori-e-lavagne",
            "articoli-diversi"
        ]
    }
]
menu_icons = [
    # Make the top level menus have an icon (Font Awesome in this case) # TODO: load from external file for modularity
    {"name": "Archiviazione", "slug": "archiviazione", "icon": "fa-solid fa-cabinet-filing fa6"},
    {"name": "Buste spedizioni ed etichette", "slug": "buste-spedizioni-ed-etichette", "icon": "fas fa-envelope"},
    {"name": "Cancelleria e ufficio", "slug": "cancelleria-e-ufficio", "icon": "fas fa-paperclip"},
    {"name": "Carta e cartoncini", "slug": "carta-e-cartoncini", "icon": "fas fa-copy"},
    {"name": "Cartoleria e scuola", "slug": "cartoleria-e-scuola", "icon": "fas fa-school"},
    {"name": "0", "slug": "0", "icon": "fas fa-ellipsis-h"},
    {"name": "Scrittura e correzione", "slug": "scrittura-e-correzione", "icon": "fas fa-pencil-ruler"},
    {"name": "Macchine per l'ufficio", "slug": "macchine-per-lufficio", "icon": "fas fa-calculator"},
    {"name": "Catering", "slug": "catering", "icon": "fa-solid fa-plate-utensils fa6"},
    {"name": "Sicurezza e magazzino", "slug": "sicurezza-e-magazzino", "icon": "fas fa-hard-hat"},
    {"name": "Elettronica e informatica", "slug": "elettronica-e-informatica", "icon": "fas fa-microchip"},
    {"name": "Espositori e lavagne", "slug": "espositori-e-lavagne", "icon": "fas fa-chalkboard"},
    {"name": "Articoli diversi", "slug": "articoli-diversi", "icon": "fas fa-ellipsis-h"},
    {"name": "Cartelle e cartelline", "slug": "cartelle-e-cartelline", "icon": "far fa-folder-open fa6"},
    {"name": "Buste in plastica", "slug": "buste-in-plastica", "icon": "fas fa-sheet-plastic fa6"},
    {"name": "Buste", "slug": "buste", "icon": "fas fa-envelopes-bulk fa6"},
    {"name": "Carta per fotocopie e stampanti", "slug": "carta-per-fotocopie-e-stampanti", "icon": "fas fa-print fa6"},
    {"name": "Carta e cartoncino colorato", "slug": "carta-e-cartoncino-colorato", "icon": "far fa-file fa6"},
    {"name": "Carta in rotoli e termica", "slug": "carta-in-rotoli-e-termica",
     "icon": "fa-solid fa-toilet-paper-blank fa6"},
    {"name": "Pile, batterie, e torce", "slug": "pile-batterie-e-torce", "icon": "fas fa-car-battery fa6"},
    {"name": "Articoli diversi", "slug": "articoli-diversi-articoli-diversi", "icon": "fas fa-ellipsis fa6"},
    {"name": "Portatessere e braccialetti identificativi", "slug": "portatessere-e-braccialetti-identificativi",
     "icon": "far fa-id-badge fa6"},
    {"name": "Bacheche, pannelli e planning", "slug": "bacheche-pannelli-e-planning", "icon": "fas fa-chalkboard fa6"},
    {"name": "Espositori pubblicitari, portadepliants, portabrochure",
     "slug": "espositori-pubblicitari-portadepliants-portabrochure", "icon": "fa-solid fa-billboard fa6"},
    {"name": "Borse, zaini, trolley, e portafogli", "slug": "borse-zaini-trolley-e-portafogli",
     "icon": "fa-solid fa-backpack fa6"},
    {"name": "Cutter, forbici e taglierine", "slug": "cutter-forbici-e-taglierine", "icon": "fas fa-scissors fa6"},
    {"name": "Nastri adesivi", "slug": "nastri-adesivi-cancelleria-e-ufficio", "icon": "fas fa-tape fa6"},
    {"name": "Modulistica", "slug": "modulistica", "icon": "fa-solid fa-memo-pad fa6"},
    {"name": "Agende e calendari", "slug": "agende-e-calendari", "icon": "far fa-calendar-days fa6"},
    {"name": "Timbri", "slug": "timbri", "icon": "fas fa-stamp fa6"},
    {"name": "Evidenziatori", "slug": "evidenziatori", "icon": "fas fa-highlighter fa6"},
    {"name": "Matite portamine", "slug": "matite-portamine", "icon": "fa-solid fa-pencil-mechanical fa6"},
    {"name": "Gomme e gommini", "slug": "gomme-e-gommini", "icon": "fas fa-eraser fa6"},
    {"name": "Matite e pastelli", "slug": "matite-e-pastelli", "icon": "fas fa-pencil fa6"},
    {"name": "Marcatori e pennarelli indelebili", "slug": "marcatori-e-pennarelli-indelebili",
     "icon": "fa-solid fa-paintbrush-pencil fa6"},
    {"name": "Penne e refil", "slug": "penne-e-refil", "icon": "fas fa-pen-clip fa6"},
    {"name": "Pittura", "slug": "pittura", "icon": "fas fa-palette fa6"},
    {"name": "Registri e rubriche", "slug": "registri-e-rubriche", "icon": "far fa-address-book fa6"},
    {"name": "Cucitrici, pinzatrici e levapunti", "slug": "cucitrici-pinzatrici-e-levapunti",
     "icon": "fas fa-stapler fa6"},
    {"name": "Accessori da scrivania", "slug": "accessori-da-scrivania", "icon": "fas fa-magnifying-glass fa6"},
    {"name": "Elastici, fermagli, puntine e fermacarte", "slug": "elastici-fermagli-puntine-e-fermacarte",
     "icon": "fas fa-thumbtack fa6"},
    {"name": "Composizione creativa", "slug": "composizione-creativa", "icon": "fa-solid fa-hammer-brush fa6"},
    {"name": "Blocchetti memo e segnapagina", "slug": "blocchetti-memo-e-segnapagina",
     "icon": "far fa-note-sticky fa6"},
    {"name": "Carta per il ricalco", "slug": "carta-per-il-ricalco", "icon": "far fa-copy fa6"},
    {"name": "Carta per plotter", "slug": "carta-per-plotter", "icon": "fas fa-tape fa6"},
    {"name": "Articoli da regalo e borse shopper", "slug": "articoli-da-regalo-e-borse-shopper",
     "icon": "fas fa-gift fa6"},
    {"name": "Colle", "slug": "colle", "icon": "fas fa-droplet fa6"},
    {"name": "Portablocchi, block notes e taccuini", "slug": "portablocchi-block-notes-e-taccuini",
     "icon": "fa-solid fa-memo-pad fa6"},
    {"name": "Perforatori", "slug": "perforatori", "icon": "far fa-circle fa6"},
    {"name": "Giochi, musica, e articoli per l'infanzia", "slug": "giochi-musica-e-articoli-per-linfanzia",
     "icon": "fa-solid fa-teddy-bear fa6"},
    {"name": "Quaderni per la scuola", "slug": "quaderni-per-la-scuola", "icon": "fa-solid fa-notebook fa6"},
    {"name": "Album e blocchi da disegno", "slug": "album-e-blocchi-da-disegno", "icon": "fas fa-file-pen fa6"},
    {"name": "Calcolatrici scuola", "slug": "calcolatrici-scuola", "icon": "fas fa-calculator fa6"},
    {"name": "Gomme scolastiche", "slug": "gomme-scolastiche", "icon": "fas fa-eraser fa6"},
    {"name": "Nastri adesivi e dispenser", "slug": "nastri-adesivi-e-dispenser", "icon": "fas fa-tape fa6"},
    {"name": "Quaderni ad anelli e ricambi", "slug": "quaderni-ad-anelli-e-ricambi",
     "icon": "fa-solid fa-notebook fa6"},
    {"name": "Valigette e tubi porta disegni", "slug": "valigette-e-tubi-porta-disegni",
     "icon": "fas fa-briefcase fa6"},
    {"name": "Zaini e astucci", "slug": "zaini-e-astucci", "icon": "fa-solid fa-backpack fa6"},
    {"name": "Blocchetti memo", "slug": "blocchetti-memo", "icon": "far fa-note-sticky fa6"},
    {"name": "Colle stick, glitter e vinavil", "slug": "colle-stick-glitter-e-vinavil", "icon": "fas fa-droplet fa6"},
    {"name": "Didattica", "slug": "didattica", "icon": "fas fa-chalkboard-user fa6"},
    {"name": "Forbici", "slug": "forbici", "icon": "fas fa-scissors fa6"},
    {"name": "Pennarelli scuola", "slug": "pennarelli-scuola", "icon": "fas fa-pen fa6"},
    {"name": "Calcolatrici", "slug": "calcolatrici", "icon": "fas fa-calculator fa6"},
    {"name": "Distruggi documenti", "slug": "distruggi-documenti", "icon": "fa-solid fa-shredder fa6"},
    {"name": "Plastificatrici a caldo e a freddo, Pouches", "slug": "plastificatrici-a-caldo-e-a-freddo-pouches",
     "icon": "fa-solid fa-scanner-image fa6"},
    {"name": "Rilegatrici, dorsi e copertine", "slug": "rilegatrici-dorsi-e-copertine", "icon": "fas fa-book-open fa6"},
    {"name": "Prodotti per il catering", "slug": "prodotti-per-il-catering", "icon": "fas fa-utensils fa6"},
    {"name": "Sicurezza e verifica dei valori", "slug": "sicurezza-e-verifica-dei-valori",
     "icon": "fas fa-shield-halved fa6"},
    {"name": "Articoli per manutenzione", "slug": "articoli-per-manutenzione", "icon": "fa-solid fa-wrench-simple fa6"},
    {"name": "Pistole sparafili e consumabili", "slug": "pistole-sparafili-e-consumabili",
     "icon": "fa-solid fa-gun-squirt fa6"},
    {"name": "Forme e stampi", "slug": "forme-e-stampi", "icon": "fa-solid fa-star-circle fa6"},
    {"name": "Polveri, sabbie, scaglie e bande per il modellaggio",
     "slug": "polveri-sabbie-scaglie-e-bande-per-il-modellaggio", "icon": "fa-solid fa-grid-round-5 fa6"},
    {"name": "Carta e cartoncino", "slug": "carta-e-cartoncino", "icon": "far fa-file fa6"},
    {"name": "Incisione, stampa artistiche e decorazioni", "slug": "incisione-stampa-artistiche-e-decorazioni",
     "icon": "fa-solid fa-sparkles fa6"},
    {"name": "Materiali da disegno e pittura", "slug": "materiali-da-disegno-e-pittura",
     "icon": "fa-solid fa-paintbrush-pencil fa6"},
    {"name": "Matite scolastiche", "slug": "matite-scolastiche", "icon": "fa-solid fa-pencil-mechanical fa6"},
    {"name": "Plastiline modellabili", "slug": "plastiline-modellabili", "icon": "fas fa-disease fa6"},
    {"name": "Penne scolastiche", "slug": "penne-scolastiche", "icon": "fas fa-pen-clip fa6"},
    {"name": "Lavagnette, gessetti e cancellini", "slug": "lavagnette-gessetti-e-cancellini",
     "icon": "fas fa-chalkboard fa6"},
    {"name": "Articoli per il disegno tecnico", "slug": "articoli-per-il-disegno-tecnico",
     "icon": "fas fa-compass-drafting fa6"},
    {"name": "Correttori e sbianchetti", "slug": "correttori-e-sbianchetti", "icon": "fas fa-broom fa6"},
    {"name": "Disegno", "slug": "disegno", "icon": "fas fa-pen-ruler fa6"},
    {"name": "Coloranti", "slug": "coloranti", "icon": "fas fa-eye-dropper fa6"},
    {"name": "Classificatori per ufficio", "slug": "classificatori-per-ufficio", "icon": "fas fa-inbox fa6"},
    {"name": "Evidenziatori", "slug": "evidenziatori-cartoleria-e-scuola", "icon": "fas fa-highlighter fa6"},
    {"name": "Correttori e bianchetti", "slug": "correttori-e-bianchetti", "icon": "fas fa-broom fa6"},
    {"name": "Articoli per l'imballaggio", "slug": "articoli-per-limballaggio",
     "icon": "fa-solid fa-box-open-full fa6"},
    {"name": "Articoli per la spedizione", "slug": "articoli-per-la-spedizione", "icon": "fas fa-boxes-packing fa6"},
    {"name": "Accessori per l'archiviazione", "slug": "accessori-per-larchiviazione",
     "icon": "fa-solid fa-shelves fa6"},
    {"name": "Portabiglietti da visita", "slug": "portabiglietti-da-visita", "icon": "fas fa-table-cells-large fa6"},
    {"name": "Pennarelli colorati", "slug": "pennarelli-colorati-scrittura-e-correzione", "icon": "fas fa-pen fa6"},
    {"name": "Portalistini, portamenù e album fotografici", "slug": "portalistini-portamenu-e-album-fotografici",
     "icon": "fa-solid fa-book-open-cover fa6"},
    {"name": "Raccoglitori per documenti", "slug": "raccoglitori-per-documenti", "icon": "fas fa-box-archive fa6"},
    {"name": "Etichette", "slug": "etichette", "icon": "far fa-note-sticky fa6"}
]

# menuItemsSlugsToSkip = ['altro']  # Grandparents
categorySlugsToSkip = ['senza-categoria']


def init_parser():
    global args
    parser = argparse.ArgumentParser(
        description="Create Menu structure from product categories."
    )
    parser.add_argument("-u", "--update-existing",
                        help="update existing menu items by setting parents and order",
                        action="store_true")
    parser.add_argument("--delete-all",
                        help="delete all menu items and start fresh",
                        action="store_true")
    parser.add_argument("--delete-orphans",
                        help="delete menu items not present in the product categories",
                        action="store_true"
                        )
    parser.add_argument("-C", "--with-count",
                        help="add count to the last level",
                        action="store_true")
    parser.add_argument("-v",
                        help="add verbosity",
                        action="store_true")

    args = parser.parse_args()


def flatten_structure(struct):
    flat_struct = []

    def this_loop(array_of_children):
        if array_of_children["children"]:
            for c in array_of_children["children"]:
                this_loop(c)

        flat_struct.insert(0, array_of_children)

    for p in struct:  # First level
        this_loop(p)
    # flat_struct = sorted(flat_struct, reverse=True, key=lambda s: s["count"])  # Sort again
    # for fs in flat_struct:
    #     print("{} {} {} {}".format(fs["name"], fs["term_id"], fs["parent"], fs["count"]))

    return flat_struct


def get_menu_item_id_from_object(needle, object_type="product_cat"):
    global main_menu_id
    global menu_items_cache

    if needle == 0:
        return 0

    def extract_db_id():
        for m in menu_items_cache:
            this_object_id = False
            if object_type == "product_cat":
                this_object_id = int(m['object_id'])
            elif object_type == "custom":
                this_object_id = m["title"]
            if this_object_id:  # Has Object ID
                if this_object_id == needle:  # Found
                    return m['db_id']
        return False

    res = extract_db_id()
    if res:
        return res
    # Cache miss, reload meta and update cache
    print("Cache miss: Needle {}".format(needle))
    load_menu_items()
    res = extract_db_id()
    if res:
        return res
    raise Exception("Non è stato trovato il menu item per il term_id {}".format(needle))


def load_menu_items():
    global main_menu_id
    global menu_items_cache
    # Find the menu item id using the term id (object_id)
    cmd = os.popen(
        "wp menu item list {} --format=json --fields=db_id,title,position,object,object_id,menu_item_parent"
        .format(main_menu_id))
    read = cmd.read()
    cmd.close()
    menu_items_cache = json.loads(read)
    return menu_items_cache


def add_menu_item(term_id_or_name, name, parent_menu_item_id, position=1, object_type="product_cat"):
    global main_menu_id
    name = name.replace("'", "\\'")
    if object_type == "product_cat":
        cmd = os.popen(
            "wp menu item add-term {menu_id} product_cat {term_id} --title=\"{name}\" --parent-id={parent_id} --position={pos};".format(
                menu_id=main_menu_id,
                term_id=term_id_or_name,
                parent_id=parent_menu_item_id,
                name=name,
                pos=position)
        )
    elif object_type == "custom":
        cmd = os.popen(
            "wp menu item add-custom {menu_id} \"{title}\" \"{link}\" --parent-id={parent_id} --position={pos};".format(
                menu_id=main_menu_id,
                title=name,
                link="#",
                parent_id=parent_menu_item_id,
                pos=position)
        )
    result = cmd.read()
    cmd.close()
    return result


def update_menu_item(menu_item_id, name, parent_item_id, position=0):
    name = "{}".format(name)  # Use unicode
    name = name.replace("'", "\\'")
    cmd = "wp menu item update {} --title=\"{}\" --parent-id={} --position={}".format(menu_item_id,
                                                                                      name,
                                                                                      parent_item_id,
                                                                                      position)
    if args.v:
        print("> {}".format(cmd))
    cmd = os.popen(
        cmd
    )
    result = cmd.read()
    cmd.close()
    return result


def delete_menu_items(menu_item_ids):
    items_list = " ".join(str(mi) for mi in menu_item_ids)
    cmd = 'wp menu item delete {}'.format(items_list)
    print('> {}'.format(cmd))
    cmd = os.popen(cmd)
    read = cmd.read()
    cmd.close()
    return read


def list_all_product_cats():
    # Get all product category ids
    cmd = os.popen('wp term list product_cat --format=json --fields=term_id,name,slug,description,count,parent')
    cats = json.loads(cmd.read())
    for i, c in enumerate(cats):
        cats[i]['object'] = "product_cat"
    cmd.close()
    return cats


def make_structure_from_cats(cats):
    # Create a structure from the wp-cli obtained categories meta
    struct = []
    # [
    #   {
    #   term_id,
    #   name,
    #   slug,
    #   description,
    #   count,
    #   parent, #del
    #   children: [
    #       {...},
    #       ...
    #       ]
    #   },
    #   ...
    # ]

    # Step 1 - Find parents
    # Fill struct with parents
    for c in cats:
        if c['slug'] in categorySlugsToSkip:
            continue
        if c["parent"] == 0:
            c["children"] = []  # Init children here
            struct.append(c)

    # Step 2 - Find children
    for i, p in enumerate(struct):
        for c in cats:
            if c["parent"] == p["term_id"]:
                c["children"] = []  # Init nephews here
                struct[i]["children"].append(c)

    # Step 3 - Find nephews
    for ip, p in enumerate(struct):
        for ic, c in enumerate(p["children"]):
            for cat in cats:
                if cat["parent"] == c["term_id"]:
                    # Last level
                    cat["children"] = []  # Init nephews2 here
                    if args.with_count:  # Append count in last level links
                        cat["name"] = "{} ({})".format(cat["name"], cat["count"])
                    struct[ip]["children"][ic]["children"].append(cat)

    # Step 4 - Sort by count
    struct = sorted(struct, key=lambda s: s["count"], reverse=True)  # Sort parents
    for ip, p in enumerate(struct):
        struct[ip]["children"] = sorted(p["children"], key=lambda c: c["count"], reverse=True)  # Sort children
        for ic, c in enumerate(struct[ip]["children"]):
            struct[ip]["children"][ic]["children"] = sorted(c["children"], key=lambda n: n["count"],
                                                            reverse=True)  # Sort nephews

    # Step 5 - Handle exceptions
    # Step 5A - Custom parents
    for cparent in custom_parents:  # Custom parent, parent slug
        this_custom_parent = {
            "term_id": 0,
            "name": cparent["name"],
            "children": [],
            "count": 0,
            "parent": 0,
            "description": "",
            "slug": "",
            "object": "custom",
            "custom_order": cparent["custom_order"]
        }

        indexes_to_del = []
        for ip, p in enumerate(struct):
            if p["slug"] in cparent["children_slugs"]:
                this_custom_parent['count'] += p["count"]  # Update count on custom parent
                p["custom_parent"] = cparent["name"]
                this_custom_parent['children'].append(p)
                indexes_to_del.append(ip)  # We don't want duplicates
        for i in sorted(indexes_to_del, reverse=True):  # Delete duplicates
            del struct[i]
        struct.append(this_custom_parent)
    if args.v:
        # "Structure:"
        print("##### STRUCTURE #####")
        for s1 in struct:
            print("")
            print("{} ({})".format(s1["name"], s1['slug']))
            for s2 in s1['children']:
                print("-- {} ({})".format(s2['name'], s2['slug']))
                for s3 in s2["children"]:
                    print("---- {} ({})".format(s3["name"], s3['slug']))
                    for s4 in s3["children"]:
                        print("------ {} ({})".format(s4['name'], s4['slug']))
        print("#####################")
    return struct


def update_wp_menu_items(struct):
    global menu_items_cache
    orphan_actual_menu_item_ids = set(
        [i["db_id"] for i in menu_items_cache])  # Track orphanated items for future deletion
    flat_struct = flatten_structure(struct)

    order_counter = max_order_position
    for si, s in enumerate(flat_struct):
        this_menu_item_id = 0
        si = order_counter - si
        for mic in menu_items_cache:  # Find this_menu_item_id
            if s["object"] == "product_cat":
                if int(mic["object_id"]) == s["term_id"]:
                    this_menu_item_id = int(mic["db_id"])
                    break
            elif s["object"] == "custom":
                if mic["title"] == s["name"]:
                    this_menu_item_id = int(mic["db_id"])
                    break

        if this_menu_item_id in orphan_actual_menu_item_ids:  # Remove orphan
            orphan_actual_menu_item_ids.remove(this_menu_item_id)

        if s["count"] > 0:
            this_parent_menu_item_id = 0  # Init parent menu item id
            if "custom_parent" not in s:  # If parent is not custom proceed with a product_cat
                if s["object"] == "product_cat":
                    this_parent_menu_item_id = get_menu_item_id_from_object(s["parent"])
                elif s["object"] == "custom":
                    this_parent_menu_item_id = 0  # Take as granted that there will be no parents
            else:
                this_parent_menu_item_id = get_menu_item_id_from_object(s["custom_parent"], 'custom')

            if args.v:
                print("Processing {name} ({slug}) TID:{tid} PID:{pid} CNT:{c}"
                      .format(name=s["name"],
                              slug=s["slug"],
                              tid=s["term_id"],
                              mid=this_menu_item_id,
                              pid=this_parent_menu_item_id,
                              c=s["count"]
                              )
                      )

            if not this_menu_item_id:  # Item doesn't exist
                if s["object"] == "product_cat":  # Add menu item by product cat
                    print("Adding menu {} (TID:{} #{})...".format(s["name"], s["term_id"],
                                                                  si if "custom_order" not in s else s[
                                                                      "custom_order"]))
                    print(add_menu_item(s["term_id"], s["name"], this_parent_menu_item_id,
                                        si if "custom_order" not in s else s["custom_order"]))
                elif s["object"] == "custom":  # Add menu item by custom item
                    print("Adding menu {} (Name:{} #{})...".format(s["name"], "custom",
                                                                   si if "custom_order" not in s else s[
                                                                       "custom_order"]))
                    print(add_menu_item(s["name"], s["name"], this_parent_menu_item_id,
                                        si if "custom_order" not in s else s["custom_order"], "custom"))

            else:
                if args.update_existing:
                    this_menu_item_id = 0
                    if s["object"] == "product_cat":
                        this_menu_item_id = get_menu_item_id_from_object(s["term_id"])
                    elif s["object"] == "custom":
                        this_menu_item_id = get_menu_item_id_from_object(s["name"], 'custom')
                    print("Item exists, updating {} (TID:{} -> MID:{} #{})...".format(s["name"], s["term_id"],
                                                                                      this_menu_item_id,
                                                                                      si if "custom_order" not in s
                                                                                      else s["custom_order"]))
                    print(
                        update_menu_item(
                            this_menu_item_id,
                            s['name'],
                            this_parent_menu_item_id,
                            si if "custom_order" not in s else s["custom_order"])
                    )
        else:
            if this_menu_item_id:  # Delete menu item only if exists and count == 0
                print("Deleting menu {} (MID:{})...".format(s["name"], this_menu_item_id))
                print(delete_menu_items([this_menu_item_id]))
    if args.delete_orphans:
        for o in orphan_actual_menu_item_ids:
            print("Deleting orphan {}...".format(o))
        print(delete_menu_items([o for o in orphan_actual_menu_item_ids]))


def launch():
    init_parser()  # Get args
    cats = list_all_product_cats()  # Load categories
    struct = make_structure_from_cats(cats)  # Prepare structure (cats)
    load_menu_items()  # Load existing menu items in cache
    if args.delete_all:  # Delete all for fresh start
        for m in menu_items_cache:
            print("Deleting {} (MID:{})".format(m['title'], m['db_id']))
        delete_menu_items([m["db_id"] for m in menu_items_cache])
        load_menu_items()  # Load existing menu items again after deletion
    update_wp_menu_items(struct)  # Main execution here


launch()
