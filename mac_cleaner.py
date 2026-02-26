import utils


def main():
    categories = utils.load_config()

    all_paths = [d["path"] for cat in categories for item in cat["items"] for d in item["paths"]]

    item_num = 1
    for cat in categories:
        cat_paths = [d["path"] for item in cat["items"] for d in item["paths"]]
        cat_total = utils.get_dirs_usage(cat_paths)
        utils.print_header(cat["name"], cat_total)
        for item in cat["items"]:
            paths = [d["path"] for d in item["paths"]]
            usage = utils.get_dir_usage(paths[0]) if len(paths) == 1 else utils.get_dirs_usage(paths)
            utils.print_item(item_num, item["name"], usage)

            for j, d in enumerate(item["paths"], 1):
                if not d["name"]:
                    continue
                utils.print_subitem(item_num, j, d["name"], utils.get_dir_usage(d["path"]), d["note"])

            item_num += 1

    if utils.confirm(utils.colored("모두 삭제하시겠습니까?", "yellow")):
        utils.delete_dirs(all_paths)
        print(utils.colored("\n=== 삭제 완료! ===\n", "cyan"))
    else:
        print(utils.colored("\n=== 작업 취소 ===\n", "gray"))


if __name__ == "__main__":
    main()
