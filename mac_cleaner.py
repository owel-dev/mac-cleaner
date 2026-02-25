import utils


def main():
    items = utils.load_config()

    all_dirs = [d["dir"] for item in items for d in item["dirs"]]
    total = utils.get_dirs_usage(all_dirs)

    utils.print_header("캐시 사용량", total)

    for i, item in enumerate(items, 1):
        dirs = [d["dir"] for d in item["dirs"]]
        usage = utils.get_dir_usage(dirs[0]) if len(dirs) == 1 else utils.get_dirs_usage(dirs)
        utils.print_item(i, item["name"], usage)

        for j, d in enumerate(item["dirs"], 1):
            if not d["name"]:
                continue
            utils.print_subitem(i, j, d["name"], utils.get_dir_usage(d["dir"]), d["description"])

    if utils.confirm(utils.colored("모두 삭제하시겠습니까?", "yellow")):
        utils.delete_dirs(all_dirs)
        print(utils.colored("\n=== 삭제 완료! ===\n", "cyan"))
    else:
        print(utils.colored("\n=== 작업 취소 ===\n", "gray"))


if __name__ == "__main__":
    main()
