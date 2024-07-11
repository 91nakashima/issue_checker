# issue_checker

- 重複した issue を検出することができます。

- root/.env を作成

  ```
  GITHUB_APP_CLIENT_ID=XXXXXX
  OPENAI_KEY=sk-XXXXXX
  ```

- XXXXXX.private-key.pem を作成

# 実行

```bash
$ python main.py --issue 1111

$ python main.py --issue 1111 --repo XXXX
```
