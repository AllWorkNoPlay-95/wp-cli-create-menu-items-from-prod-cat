#!/usr/bin/env python3
# Copyright 2024 - Samuele Mancuso (https://github.com/AllWorkNoPlay-95)
# This utility creates a nav structure to use with Max Mega menu starting from product categories
# GPL-3.0 License
import copy
import os
import json
import argparse
from pprint import pprint
from config import main_menu_id, max_order_position, custom_parents, menu_icons, category_slugs_to_skip

# Globals
menu_items_cache = []
parents_to_put_in_other = []
args = []


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
        if c['slug'] in category_slugs_to_skip:
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
