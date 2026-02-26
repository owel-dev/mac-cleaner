import utils


def main():
    categories = utils.load_config()

    all_dirs = [d["dir"] for cat in categories for item in cat["apps"] for d in item["dirs"]]

    item_num = 1
    for cat in categories:
        cat_dirs = [d["dir"] for item in cat["apps"] for d in item["dirs"]]
        cat_total = utils.get_dirs_usage(cat_dirs)
        utils.print_header(cat["name"], cat_total)
        for item in cat["apps"]:
            dirs = [d["dir"] for d in item["dirs"]]
            usage = utils.get_dir_usage(dirs[0]) if len(dirs) == 1 else utils.get_dirs_usage(dirs)
            utils.print_item(item_num, item["name"], usage)

            for j, d in enumerate(item["dirs"], 1):
                if not d["name"]:
                    continue
                utils.print_subitem(item_num, j, d["name"], utils.get_dir_usage(d["dir"]), d["description"])

            item_num += 1

    if utils.confirm(utils.colored("모두 삭제하시겠습니까?", "yellow")):
        utils.delete_dirs(all_dirs)
        print(utils.colored("\n=== 삭제 완료! ===\n", "cyan"))
    else:
        print(utils.colored("\n=== 작업 취소 ===\n", "gray"))


if __name__ == "__main__":
    main()
