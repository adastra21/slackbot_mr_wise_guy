from sqlalchemy.sql import select
import create_db
import get_answer

def prepare_answer(result):
    """
    Prepare answer from data available
    # result format: name, committee, committeeRole, company, job, tag
    """
    answer = ""
    if result:
        clean_result = [x for t in result for x in t]

        name = clean_result[0].title()
        committee = clean_result[1].title()
        role = clean_result[2].title()
        company = clean_result[3].title()
        job = clean_result[4].title()
        tag = clean_result[5]

        # to avoid duplicate value in committe
        if committee == "Chapter Co-Chairs":
            role = committee.replace("s","")
            committee = ""

        # answer = "%s is a %s on %s who rocks hard %s %s at %s during the day"
        if name:
            answer += name
        if role:
            answer += " is a "+role
        if committee:
            answer += " on "+committee
        if company != "None":
            answer += " who rocks hard at "+company
        if job:
            if tag == "in":
                answer += " in "+job+" during the day!"
            else:
                answer += " as a "+job+" during the day!"

    if answer:
        return answer
    else:
        return "I didn't find anyone"


def handle_question(command):
    """
    columns: name, email, phone, committee, committeeRole, dayjob
    """
    create_db.create_db()

    if "whois" in command:
        result = get_answer.run_query(command, "who")
        answer = prepare_answer(result)
        return answer

    elif "getme" in command:
        result = get_answer.run_query(command, "get")
        if result:
            clean_result = [x for t in result for x in t]
            # format: name, email, phone, gender
            if clean_result[3] == "f":
                pronoun = "her"
            elif clean_result[3] == "m":
                pronoun = "him"
            answer = clean_result[0].title()+" can be reached at "+clean_result[1].lower()+" or "+clean_result[2]+". Tell "+pronoun+" I said 'hello'."
            return answer
        else:
            return "Are you sure they exist?"