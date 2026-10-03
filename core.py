import re, uuid
from datetime import date, timedelta
import pandas as pd
from integrations import ROOT, save_csv, claude_json

DATA=ROOT/"data"
TASKS=DATA/"tasks.csv"
FIELDS=["id","customer","task","owner","due_date","status","dependency","notes"]
STATUSES=["Not started","In progress","Done"]
FAQ=[
 {"id":"F1","title":"Invite users","keywords":["invite","users","teammate"],"answer":"In this simulated SaaS product, open Settings > Team > Invite, enter a work email, and choose a role. If Invite is unavailable, ask your administrator."},
 {"id":"F2","title":"Import data","keywords":["import","csv","upload"],"answer":"Use a UTF-8 CSV with name and email headers. Validate a five-row sample before importing the full file. This is a simulated workflow."},
 {"id":"F3","title":"Training","keywords":["training","walkthrough","demo"],"answer":"Schedule a 30-minute walkthrough with the customer owner. Cover the main workflow, permissions and where to find help."},
 {"id":"F4","title":"Go-live readiness","keywords":["go-live","launch","readiness"],"answer":"Confirm setup and testing are complete, users have access, training is done, and the customer has approved launch. Record the owner and sign-off date."},
 {"id":"F5","title":"Escalation","keywords":["escalate","bug","error","broken"],"answer":"Record customer impact, reproduction steps, owner and next update time. Route technical issues to engineering. Do not promise an unconfirmed fix date."},
 {"id":"F6","title":"Adoption follow-up","keywords":["adoption","usage","follow-up"],"answer":"Review active users and completion of the main workflow after go-live. Ask about obstacles, offer targeted training, and agree the next follow-up."}
]
def seed_tasks(today=None):
    today=today or date.today()
    rows=[]
    for n in range(1,9):
        previous=""
        for k,name in enumerate(["Kickoff","Requirements","Setup","Testing","Training","Go-live"]):
            task_id=f"C{n:02}-{k+1}"
            status="Done" if k<n%4 else "In progress" if k==n%4 else "Not started"
            rows.append([task_id,f"Demo Customer {n:02}",name,["Asha","Rohan","Meera"][k%3],
                (today+timedelta(days=k*2-n)).isoformat(),status,previous,"Simulated onboarding"])
            previous=task_id
    return pd.DataFrame(rows,columns=FIELDS)

def validate_tasks(frame):
    if not set(FIELDS).issubset(frame.columns):
        raise ValueError("Missing tracker columns.")
    df=frame[FIELDS].fillna("").astype(str).copy()
    if df.id.eq("").any() or df.id.duplicated().any():
        raise ValueError("Task IDs must be present and unique.")
    if df[["customer","task","owner"]].eq("").any().any():
        raise ValueError("Each task needs a customer, description and owner.")
    if not df.status.isin(STATUSES).all():
        raise ValueError("Invalid task status.")
    for value in df.due_date: date.fromisoformat(value)
    parents=dict(zip(df.id,df.dependency))
    customers=dict(zip(df.id,df.customer))
    for task,parent in parents.items():
        if parent and (parent not in parents or customers[parent]!=customers[task]):
            raise ValueError("Dependencies must reference tasks for the same customer.")
        seen,node=set(),task
        while node:
            if node in seen: raise ValueError("Dependency cycle detected.")
            seen.add(node)
            node=parents[node]
    return df

def flags(frame,today=None):
    df=validate_tasks(frame)
    today=today or date.today()
    status=dict(zip(df.id,df.status))
    df["overdue"]=[date.fromisoformat(d)<today and s!="Done" for d,s in zip(df.due_date,df.status)]
    df["blocked"]=[bool(p and status[p]!="Done" and s!="Done") for p,s in zip(df.dependency,df.status)]
    df["flag"]=["Overdue + blocked" if a and b else "Overdue" if a else "Blocked" if b else "On track" for a,b in zip(df.overdue,df.blocked)]
    return df

def load_tasks():
    if not TASKS.exists(): save_csv(seed_tasks(),TASKS)
    return validate_tasks(pd.read_csv(TASKS,dtype=str,keep_default_na=False))

def answer(question,use_ai=False):
    if use_ai:
        result=claude_json('Answer only from the provided FAQ. If unsupported, escalate. JSON keys: answer (string), sources (list of FAQ IDs), escalate (boolean).',{"faq":FAQ,"question":question})
        if not isinstance(result,dict) or not isinstance(result.get("escalate"),bool) or not isinstance(result.get("answer"),str) or not isinstance(result.get("sources"),list):
            raise ValueError("Invalid assistant response.")
        valid={f["id"] for f in FAQ}
        if result["escalate"] or not result["sources"] or not all(isinstance(x,str) and x in valid for x in result["sources"]):
            return {"answer":"This question needs human review.","sources":[],"escalate":True}
        return result
    lower=question.lower()
    matches=[f for f in FAQ if any(re.search(r"\b"+re.escape(k)+r"\b",lower) for k in f["keywords"])]
    if len(matches)==1 and len(lower.split())<=12 and not any(w in lower for w in ["refund","price","security","guarantee","delete","billing"]):
        f=matches[0]
        return {"answer":f["answer"],"sources":[f["id"]],"escalate":False}
    return {"answer":"No single supported FAQ answer was found. A human should review this question.","sources":[],"escalate":True}

def escalate(customer,question):
    path=DATA/"escalations.csv"
    df=pd.read_csv(path,dtype=str,keep_default_na=False) if path.exists() else pd.DataFrame(columns=["id","created","customer","question","status","owner"])
    if not (df.customer.eq(customer)&df.question.eq(question)&df.status.eq("Open")).any():
        df.loc[len(df)]=[uuid.uuid4().hex[:10],date.today().isoformat(),customer,question,"Open","CX team"]
        save_csv(df,path)

def extract_actions(notes,use_ai=False):
    if use_ai:
        result=claude_json('Extract explicit actions only. Do not invent owners or dates. Return {"actions":[{"task":"...","owner":"...","due_date":"YYYY-MM-DD or empty"}]}. Unknown values are empty strings.',{"notes":notes})
        if not isinstance(result,dict) or not isinstance(result.get("actions"),list): raise ValueError("Invalid action response.")
        actions=result["actions"]
    else:
        actions=[]
        for line in notes.splitlines():
            m=re.fullmatch(r"\s*(.+?):\s*(.+?)\s*\|\s*due\s+(\d{4}-\d{2}-\d{2})\s*",line)
            if m: actions.append({"owner":m[1],"task":m[2],"due_date":m[3]})
    for action in actions:
        if not isinstance(action,dict) or not all(isinstance(action.get(k),str) for k in ["task","owner","due_date"]): raise ValueError("Invalid action schema.")
        if action["due_date"]: date.fromisoformat(action["due_date"])
    return pd.DataFrame(actions,columns=["task","owner","due_date"])

def add_actions(frame,customer,actions):
    if customer not in set(frame.customer): raise ValueError("Unknown customer.")
    result=frame.copy()
    for item in actions.fillna("").astype(str).to_dict("records"):
        if not all(item[k].strip() for k in ["task","owner","due_date"]): raise ValueError("Fill task, owner and date before saving.")
        date.fromisoformat(item["due_date"])
        duplicate=result.customer.eq(customer)&result.task.eq(item["task"])&result.owner.eq(item["owner"])&result.due_date.eq(item["due_date"])
        if duplicate.any(): continue
        result.loc[len(result)]=[uuid.uuid4().hex[:10],customer,item["task"],item["owner"],item["due_date"],"Not started","","Reviewed call-note action"]
    return validate_tasks(result)
