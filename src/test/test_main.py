from src.main import GitHubApp
from src.embedding import get_embedding, find_embeddings

owner = 'CodeLic'
repo = 'repo'


def test_get_issues():
    app = GitHubApp(
        owner=owner,
        repo=repo
    )
    res = app.get_issues()

    target_issue = app.get_issue(3298)
    target_issue_embedding = get_embedding(f'{target_issue.title} / {target_issue.body}')

    res = list(filter(lambda x: x.id != target_issue.id, res))

    embeddings = []
    ids = []
    for issue in res:
        # get_embeddingは、データベースに保存すべきです。
        embeddings.append(get_embedding(f'{issue.title} / {issue.body}'))
        ids.append(issue.id)

    data = find_embeddings(target_issue_embedding, embeddings, ids, 0.6)

    for issue_id in data:
        print(issue_id['val'])
        find_data = next(filter(lambda x: x.id == issue_id['id'], res), None)
        if find_data:
            print(find_data.number)
            print(find_data.title)


def test_get_issue():
    app = GitHubApp(
        owner=owner,
        repo=repo
    )
    res = app.get_issue(3298)

    print(len(res.comments))


def test_send_comment():
    app = GitHubApp(
        owner=owner,
        repo=repo
    )
    res = app.send_comment(3298, 'Hello, world!')
    print(res)
