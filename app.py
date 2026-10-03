from datetime import date
import pandas as pd
import streamlit as st
from integrations import save_csv,push_sheet
from core import *

st.set_page_config(page_title="Onboarding copilot",page_icon=":material/rocket_launch:",layout="wide")
st.title("Customer onboarding copilot")
st.caption("Portfolio simulation | Starts with eight fictional customers | Local mode needs no API keys")
use_ai=st.sidebar.radio("Assistant mode",["Local demo","Claude API"])=="Claude API"
if use_ai: st.sidebar.info("Assistant requests send the entered text and FAQ context to Claude; API usage may be billed.")
today=st.sidebar.date_input("Flag calculation date",date.today())
tasks=load_tasks()
view=flags(tasks,today)
with st.container(horizontal=True):
    st.metric("Customers",tasks.customer.nunique(),border=True)
    st.metric("Completed tasks",int(tasks.status.eq("Done").sum()),border=True)
    st.metric("Overdue tasks",int(view.overdue.sum()),border=True)
    st.metric("Blocked tasks",int(view.blocked.sum()),border=True)
tabs=st.tabs(["Tracker","FAQ assistant","Call notes","Escalations","Sheets export"])
with tabs[0]:
    if "customer_created" in st.session_state:
        st.success(st.session_state.pop("customer_created"))
    with st.expander("Start onboarding a customer", expanded=True):
        st.write("Create a six-step onboarding plan, then adjust each task's owner and deadline in the tracker.")
        st.caption("Template deadlines: kickoff day, then +2, +4, +6, +8 and +10 calendar days. Confirm these dates with your customer.")
        with st.form("new_customer"):
            customer_name = st.text_input("Customer name", key="new_customer_name", placeholder="Acme Studio")
            customer_owner = st.text_input("Initial task owner", key="new_customer_owner", placeholder="Abhinandan")
            kickoff_date = st.date_input("Kickoff date", date.today(), key="new_customer_date")
            create_submitted = st.form_submit_button("Create onboarding plan")
        if create_submitted:
            try:
                updated_tasks = create_customer(load_tasks(), customer_name, customer_owner, kickoff_date)
                save_csv(updated_tasks, TASKS)
                st.session_state["customer_created"] = "Customer added with six tasks. Review the owners and deadlines below."
                st.rerun()
            except (ValueError, TypeError, OverflowError) as error:
                st.error(str(error))
            except OSError:
                st.error("The plan could not be saved. Check file permissions and try again.")

    customers=st.multiselect("Filter customers",sorted(tasks.customer.unique()))
    st.dataframe(view[view.customer.isin(customers)] if customers else view,hide_index=True,alt="Customer tasks and delay flags")
    st.bar_chart(pd.crosstab(tasks.customer,tasks.status),alt="Task status by customer")
    st.subheader("Edit the full tracker")
    st.caption("Dates use YYYY-MM-DD. Dependencies reference task IDs. Flags update after saving.")
    with st.form("edit"):
        edited=st.data_editor(tasks,num_rows="fixed",hide_index=True,disabled=["id","customer"],alt="Editable onboarding tracker",
             column_config={"status":st.column_config.SelectboxColumn(options=STATUSES)})
        submit=st.form_submit_button("Save tracker")
    if submit:
        try:
            save_csv(validate_tasks(edited),TASKS)
            st.rerun()
        except (ValueError,TypeError) as e: st.error(str(e))
    st.download_button("Download tracker CSV",view.to_csv(index=False),"onboarding_tracker.csv","text/csv")
with tabs[1]:
    customer=st.selectbox("Customer",sorted(tasks.customer.unique()),key="faq_customer")
    question=st.text_input("Customer question",placeholder="How do I invite users?",key="question")
    if st.button("Answer question",disabled=not question.strip(),key="answer"):
        try:
            result=answer(question,use_ai)
            st.write(result["answer"])
            if result["sources"]: st.caption("FAQ references: "+", ".join(result["sources"]))
            if result["escalate"]:
                escalate(customer,question)
                st.warning("Added to the local human-review queue.")
        except Exception as e: st.error("Request failed; no answer was recorded. "+type(e).__name__)
    with st.expander("Inspect the source FAQ"):
        for f in FAQ:
            st.markdown(f"**{f['id']}: {f['title']}**")
            st.write(f["answer"])
with tabs[2]:
    customer=st.selectbox("Assign actions to",sorted(tasks.customer.unique()),key="notes_customer")
    notes=st.text_area("Call notes",value="Asha: Collect brand requirements | due 2026-10-06\nRohan: Test user access | due 2026-10-07",key="notes")
    st.caption("Local format: Owner: action | due YYYY-MM-DD. Claude supports free-form notes. Review before saving.")
    if st.button("Extract action items",key="extract"):
        try:
            st.session_state["actions"]=extract_actions(notes,use_ai)
            st.session_state["actions_customer"]=customer
        except Exception as e: st.error("Extraction failed: "+type(e).__name__)
    if "actions" in st.session_state:
        st.caption("Preview customer: "+st.session_state["actions_customer"])
        preview=st.data_editor(st.session_state["actions"],num_rows="dynamic",key="preview",alt="Extracted action items awaiting review")
        if st.button("Add reviewed actions to tracker",disabled=preview.empty):
            try:
                save_csv(add_actions(tasks,st.session_state["actions_customer"],preview),TASKS)
                del st.session_state["actions"]
                st.rerun()
            except (ValueError,TypeError) as e: st.error(str(e))
with tabs[3]:
    path=DATA/"escalations.csv"
    if path.exists():
        queue=pd.read_csv(path,dtype=str,keep_default_na=False)
        with st.form("queue"):
            updated=st.data_editor(queue,disabled=["id","created","customer","question"],alt="Human escalation queue",
                column_config={"status":st.column_config.SelectboxColumn(options=["Open","In progress","Resolved"])})
            if st.form_submit_button("Save queue"):
                save_csv(updated,path)
                st.rerun()
    else: st.info("Unsupported FAQ questions will appear here.")
with tabs[4]:
    st.write("Import the downloaded CSV into Google Sheets, or export using a configured service account.")
    name=st.text_input("New worksheet name",value="Onboarding export")
    if st.button("Upload tracker to Google Sheets"):
        try: st.link_button("Open worksheet",push_sheet(view,name))
        except Exception as e: st.error(str(e) if isinstance(e,ValueError) else "Upload failed; check credentials, sharing and connection.")
