"""
$ python main.py --issue 1111

$ python main.py --issue 1111 --repo XXXX
"""


from src.main import GitHubApp
from src.embedding import get_embedding, find_embeddings

import os
import pickle
import argparse

# 適宜変更してください
owner = 'CodeLic'
repo = 'repo'

# ローカルでの高速化のため、pklを使う
use_pkl = True


def send_messege_to_issue(issue_number: int):
    app = GitHubApp(
        owner=owner,
        repo=repo
    )
    res = app.get_issues()

    target_issue = app.get_issue(issue_number)
    target_issue_embedding = get_embedding(f'{target_issue.title} / {target_issue.body}')

    res = list(filter(lambda x: x.id != target_issue.id, res))

    pkl_data = {
        "embeddings": [],
        "ids": [],
        "res": []
    }
    if use_pkl:
        path = f'./{repo}.pkl'
        # pathの存在を確認
        if os.path.exists(path):
            with open(path, 'rb') as f:
                pkl_data = pickle.load(f)

    format_res = []

    embeddings = []
    ids = []

    for issue in res:
        # get_embeddingは、データベースに保存すべきです。
        # pkl_dataから見つける
        find_data = next(filter(lambda x: x['id'] == issue.id, pkl_data['res']), None)
        if find_data:
            find_data = find_data['embedding']
        else:
            find_data = get_embedding(f'{issue.title} / {issue.body}')

        embeddings.append(find_data)
        ids.append(issue.id)
        format_res.append({
            "id": issue.id,
            "title": issue.title,
            "embedding": find_data
        })

    if use_pkl:
        path = f'./{repo}.pkl'
        with open(path, 'wb') as f:
            pickle.dump({
                "embeddings": embeddings,
                "ids": ids,
                "res": format_res
            }, f)

    data = find_embeddings(target_issue_embedding, embeddings, ids, 0.7)
    data = data[:3]

    if not len(data):
        return

    send_text = '重複を検出しました。\n\n'

    for issue_id in data:
        find_data = next(filter(lambda x: x.id == issue_id['id'], res), None)
        if find_data:
            print(find_data.number)
            print(find_data.title)
            send_text += f'#{find_data.number} {find_data.title}\n'

    app.send_comment(issue_number, send_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", type=int, required=True)
    parser.add_argument("--repo", type=str, default=None)

    if parser.parse_args().repo:
        repo = parser.parse_args().repo

    opt = parser.parse_args()

    issue_number = opt.issue

    send_messege_to_issue(issue_number)
