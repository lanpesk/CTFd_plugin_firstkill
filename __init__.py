from sqlalchemy.sql import and_
from CTFd.models import Challenges
from CTFd.utils.modes import get_model
from CTFd.models import Solves
import requests

# TODO: 可能存在竞态条件
def check_solve_place(challenge_id):

    # get challenge name
    chal = Challenges.query.filter(
        Challenges.id == challenge_id,
        and_(Challenges.state != "hidden", Challenges.state != "locked"),
    ).first_or_404()
    chal_name = chal.name

    # get solve
    Model = get_model()
    solves = (
        Solves.query.add_columns(Model.name.label("account_name"))
            .join(Model, Solves.account_id == Model.id)
            .filter(
            Solves.challenge_id == challenge_id,
            Model.banned == False,
            Model.hidden == False,
        )
            .order_by(Solves.date.asc())
    )

    if solves.count() > 3: return

    solve, account_name = solves[-1]
    send_kill_msg(account_name, chal_name, solves.count())

    return

def send_kill_msg(account_name, chall_name, index):
    try:
        requests.post("http://127.0.0.1:5000/first_kill", json={"user":account_name, "chall":chall_name, "place":index},timeout=1)
    except:
        pass

def load(app):
    pass

