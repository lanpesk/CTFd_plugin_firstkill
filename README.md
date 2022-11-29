# Usage

## First:

You can download this program in "CTFd/plugin"

```shell
cd CTFd/plugins/
git clone https://github.com/lanpesk/CTFd_plugin_firstkill.git
```

Or download this program under any path of the CTFd project.



## Second：

Add the import code in "CTFd/api/v1/challenges.py"

```python
from CTFd.plugins.CTFd_plugin_firstkill import check_solve_place
```

If you download the file in other path, the import path should be change.

Then add this code in function `ChallengeAttempt.post` which is in "CTFd/api/v1/challenges.py":

```python
try:
	check_solve_place(challenge_id)
except:
	pass
```

```python
origin:
            status, message = chal_class.attempt(challenge, request)
            if status:  # The challenge plugin says the input is right
                if ctftime() or current_user.is_admin():
                    chal_class.solve(
                        user=user, team=team, challenge=challenge, request=request
                    )
                    clear_standings()

                log(
                    "submissions",
                    "[{date}] {name} submitted {submission} on {challenge_id} with kpm {kpm} [CORRECT]",
                    name=user.name,
                    submission=request_data.get("submission", "").encode("utf-8"),
                    challenge_id=challenge_id,
                    kpm=kpm,
                )
                
                return {
                    "success": True,
                    "data": {"status": "correct", "message": message},
                }
    
after:
            status, message = chal_class.attempt(challenge, request)
            if status:  # The challenge plugin says the input is right
                if ctftime() or current_user.is_admin():
                    chal_class.solve(
                        user=user, team=team, challenge=challenge, request=request
                    )
                    clear_standings()

                log(
                    "submissions",
                    "[{date}] {name} submitted {submission} on {challenge_id} with kpm {kpm} [CORRECT]",
                    name=user.name,
                    submission=request_data.get("submission", "").encode("utf-8"),
                    challenge_id=challenge_id,
                    kpm=kpm,
                )

                try:
                    check_solve_place(challenge_id)
                except:
                    pass

                return {
                    "success": True,
                    "data": {"status": "correct", "message": message},
                }
```



## Third:

Change the target url in "\_\_init\_\_.py":

```python
def send_kill_msg(account_name, chall_name, index):
    try:
        requests.post(target_url, json={"user":account_name, "chall":chall_name, "place":index},timeout=1)
    except:
        pass
```

Now if there a new solve in top three solves, CTFd will send a message to the target url. And you can receive the message and do more operation.
