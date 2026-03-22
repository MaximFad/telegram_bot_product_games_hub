def get_leaderboard_sheet():
    return get_spreadsheet().worksheet("leaderboard_points")


def _find_leaderboard_row(user_id: int) -> Optional[int]:
    sheet = get_leaderboard_sheet()
    user_ids = sheet.col_values(1)

    for index, value in enumerate(user_ids[1:], start=2):
        if value.strip() == str(user_id):
            return index

    return None


def ensure_leaderboard_user(user):
    row = _find_leaderboard_row(user.id)
    sheet = get_leaderboard_sheet()

    if row:
        sheet.update(f"B{row}:F{row}", [[
            user.username or "",
            user.first_name or "",
            user.last_name or "",
            sheet.cell(row, 5).value or "0",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ]])
        return

    sheet.append_row([
        user.id,
        user.username or "",
        user.first_name or "",
        user.last_name or "",
        0,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ])


def increment_comment_count(user) -> int:
    ensure_leaderboard_user(user)

    row = _find_leaderboard_row(user.id)
    sheet = get_leaderboard_sheet()

    current_value = sheet.cell(row, 5).value or "0"
    current_count = int(current_value) if str(current_value).isdigit() else 0
    new_count = current_count + 1

    sheet.update(f"B{row}:F{row}", [[
        user.username or "",
        user.first_name or "",
        user.last_name or "",
        str(new_count),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]])

    return new_count


def _load_users_map() -> dict[int, dict]:
    sheet_users = get_users_sheet()
    rows = sheet_users.get_all_values()

    result = {}
    for row in rows[1:]:
        if not row or not row[0].strip().isdigit():
            continue

        user_id = int(row[0].strip())
        result[user_id] = {
            "username": row[1] if len(row) > 1 else "",
            "first_name": row[2] if len(row) > 2 else "",
            "last_name": row[3] if len(row) > 3 else "",
        }

    return result


def get_leaderboard_data() -> list[dict]:
    users_map = _load_users_map()

    refs_sheet = get_refs_sheet()
    refs_rows = refs_sheet.get_all_values()[1:]

    referrals_map: dict[int, int] = {}
    for row in refs_rows:
        if len(row) < 2:
            continue
        inviter_raw = row[1].strip()
        if inviter_raw.isdigit():
            inviter_id = int(inviter_raw)
            referrals_map[inviter_id] = referrals_map.get(inviter_id, 0) + 1

    leaderboard_sheet = get_leaderboard_sheet()
    leaderboard_rows = leaderboard_sheet.get_all_values()[1:]

    activity_map: dict[int, dict] = {}
    for row in leaderboard_rows:
        if not row or not row[0].strip().isdigit():
            continue

        user_id = int(row[0].strip())
        activity_map[user_id] = {
            "comments_count": int(row[4]) if len(row) > 4 and str(row[4]).isdigit() else 0,
            "username": row[1] if len(row) > 1 else "",
            "first_name": row[2] if len(row) > 2 else "",
            "last_name": row[3] if len(row) > 3 else "",
        }

    all_user_ids = set(users_map.keys()) | set(activity_map.keys()) | set(referrals_map.keys())

    result = []
    for user_id in all_user_ids:
        user_info = users_map.get(user_id, {})
        activity_info = activity_map.get(user_id, {})

        username = activity_info.get("username") or user_info.get("username") or ""
        first_name = activity_info.get("first_name") or user_info.get("first_name") or ""
        last_name = activity_info.get("last_name") or user_info.get("last_name") or ""

        comments_count = activity_info.get("comments_count", 0)
        referrals_count = referrals_map.get(user_id, 0)

        points = comments_count * 20 + referrals_count * 40

        result.append({
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "comments_count": comments_count,
            "referrals_count": referrals_count,
            "points": points,
        })

    result.sort(key=lambda item: (-item["points"], -item["referrals_count"], item["user_id"]))
    return result
